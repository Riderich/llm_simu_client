#!/usr/bin/env python3
"""
Pilot: extract MI-aligned final profiles from whole-dialogue profile inputs.

API 密钥：固定读取仓库根 `.env`（override=False）。

Usage (repo root):
  python3 data_scripts/extract_mi_profile_pilot.py --dry-run
  python3 data_scripts/extract_mi_profile_pilot.py --max-dialogues 10
  python3 data_scripts/extract_mi_profile_pilot.py --resume
  python3 data_scripts/extract_mi_profile_pilot.py --all --workers 8 --resume --out-dir workspace/results/profiles/recap_mi_full

``--workers`` 默认 4；checkpoint 中未完成槽位为 JSON ``null``，``--resume`` 会重试 ``null``、``parse_error`` 或缺少 ``mi_profile`` 的条目。

产出文件名随数据源变化：默认取 ``--dialogues`` 的文件 stem，例如
``profile_inputs/recap.json`` → ``recap_profiles.json`` / ``recap_selection.json``；
``profile_inputs/annomi.json`` → ``annomi_profiles.json`` / ``annomi_selection.json``。
可用 ``--source-name`` 覆盖 stem。
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]

# 固定使用仓库根 `.env`（OPENAI_API_KEY / QWEN_API_KEY / OPENAI_BASE_URL 等）
from dotenv import load_dotenv

load_dotenv(REPO / ".env", override=False)

sys.path.insert(0, str(REPO / "workspace" / "src"))

from llm_client import LLMClient  # noqa: E402


def _extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", text, re.IGNORECASE)
    if fence:
        try:
            return json.loads(fence.group(1).strip())
        except json.JSONDecodeError:
            pass
    start = text.find("{")
    if start >= 0:
        depth = 0
        for i, ch in enumerate(text[start:], start):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start : i + 1])
                    except json.JSONDecodeError:
                        break
    raise ValueError(f"无法解析 JSON: {text[:400]}...")


def _client_turns(dlg: dict[str, Any]) -> int:
    return sum(1 for t in dlg.get("dialogue", []) if t.get("speaker") == "client")


def _render_transcript(dlg: dict[str, Any]) -> str:
    raw_turns = list(dlg.get("dialogue", []))
    if raw_turns and all(t.get("turn_pos") is not None for t in raw_turns):
        try:
            turns = sorted(raw_turns, key=lambda t: t["turn_pos"])
        except TypeError:
            turns = raw_turns
    else:
        turns = raw_turns
    lines: list[str] = []
    for t in turns:
        spk = t.get("speaker", "")
        text = str(t.get("text", "")).strip()
        if not text:
            continue
        who = "咨询师" if spk == "therapist" else "来访者" if spk == "client" else str(spk)
        lines.append(f"{who}：{text}")
    return "\n".join(lines)


def _validate_mi_profile(obj: Any) -> list[str]:
    errs: list[str] = []
    try:
        if not isinstance(obj, dict):
            return ["root 不是 object"]
        top = {"demographics", "focus_of_change", "mi_core", "style"}
        if set(obj.keys()) != top:
            errs.append(f"顶层键应为 {sorted(top)}，实际 {sorted(obj.keys())}")
            return errs
        demo = obj["demographics"]
        ab = obj["mi_core"]["ambivalence"]
        if len(ab.get("sustain_talk_themes") or []) < 2:
            errs.append("sustain_talk_themes 至少 2 条")
        if len(ab.get("change_talk_themes") or []) < 1:
            errs.append("change_talk_themes 至少 1 条")
        tags = demo.get("social_situation_tags") or []
        if not (2 <= len(tags) <= 5):
            errs.append("social_situation_tags 应为 2～5 个")
        disc = obj["mi_core"]["discord_profile"]
        st = disc.get("sensitive_triggers") or []
        if len(st) < 2:
            errs.append("sensitive_triggers 至少 2 条")
    except (KeyError, TypeError) as e:
        errs.append(f"结构不完整: {e!r}")
    return errs


def _load_system_prompt() -> str:
    p = REPO / "workspace/prompts/mi_profile_extract_zh_system.md"
    return p.read_text(encoding="utf-8").strip()


def _item_extraction_ok(it: Any) -> bool:
    return (
        isinstance(it, dict)
        and not it.get("parse_error")
        and it.get("mi_profile") is not None
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="MI Profile pilot on whole-dialogue profile inputs; 使用仓库根 .env")
    ap.add_argument(
        "--dialogues",
        "--recap-dialogues",
        dest="dialogues",
        type=Path,
        default=REPO / "workspace/results/profile_inputs/recap.json",
        help=(
            "整段对话 JSON（列表）；默认 profile_inputs/recap.json。"
            "注意：profile_inputs 中 RECAP 为中文，annomi/esconv/mesc 目前为英文原文；"
            "--recap-dialogues 为兼容旧参数。"
        ),
    )
    ap.add_argument("--max-dialogues", type=int, default=10)
    ap.add_argument(
        "--all",
        action="store_true",
        help="处理筛选后 pool 中的全部对话（等价于 --max-dialogues=len(pool)，覆盖 --max-dialogues）",
    )
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--min-client-turns", type=int, default=2)
    ap.add_argument("--model", default="deepseek-v4-flash")
    ap.add_argument("--sleep", type=float, default=0.35)
    ap.add_argument(
        "--source-name",
        default=None,
        help="输出文件前缀；默认取 --dialogues 的文件 stem（如 recap、annomi）",
    )
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=REPO / "workspace/results/profiles/pilot_mi",
        help="试点产出目录；默认 results/profiles/pilot_mi/",
    )
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument(
        "--workers",
        type=int,
        default=4,
        help="并行线程数（I/O 型 API 调用）；1 等价于顺序执行",
    )
    ap.add_argument(
        "--checkpoint-every",
        type=int,
        default=1,
        metavar="N",
        help="每完成 N 条对话写盘一次 checkpoint（含 null 占位）",
    )
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(line_buffering=True)  # type: ignore[attr-defined]
    except (AttributeError, OSError):
        pass

    out_dir = args.out_dir.expanduser()
    if not out_dir.is_absolute():
        out_dir = (REPO / out_dir).resolve()
    else:
        out_dir = out_dir.resolve()

    dlg_path = args.dialogues.resolve()
    source_name = (args.source_name or dlg_path.stem or "profiles").strip()
    if not source_name:
        source_name = "profiles"
    dialogues = json.loads(dlg_path.read_text(encoding="utf-8"))
    source_meta: dict[str, Any] = {
        "kind": "profile_input_dialogues",
        "path": str(dlg_path.relative_to(REPO)),
        "source_name": source_name,
        "dialogues_total": len(dialogues),
    }

    pool = [d for d in dialogues if _client_turns(d) >= args.min_client_turns]
    rnd = random.Random(args.seed)
    rnd.shuffle(pool)
    max_take = len(pool) if args.all else args.max_dialogues
    chosen = pool[:max_take]

    out_dir.mkdir(parents=True, exist_ok=True)
    selection = {
        "env_file": str((REPO / ".env").resolve()),
        "source_name": source_name,
        "dialogues_source": source_meta,
        "seed": args.seed,
        "all": args.all,
        "max_dialogues": args.max_dialogues,
        "max_take_applied": len(chosen),
        "min_client_turns": args.min_client_turns,
        "chosen_count": len(chosen),
        "character_ids": [d.get("character_id") for d in chosen],
        "dialogue_ids": [d.get("dialogue_id") for d in chosen],
        "output_profiles": f"{source_name}_profiles.json",
        "output_selection": f"{source_name}_selection.json",
    }
    sel_path = out_dir / f"{source_name}_selection.json"
    sel_path.write_text(json.dumps(selection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[pilot] wrote {sel_path.relative_to(REPO)} ({len(chosen)} dialogues)", flush=True)

    out_path = out_dir / f"{source_name}_profiles.json"
    n = len(chosen)
    items_out: list[dict[str, Any] | None] = [None] * n

    if args.resume and out_path.exists():
        prev = json.loads(out_path.read_text(encoding="utf-8"))
        raw = prev.get("items", [])
        if len(raw) > n:
            print(
                f"[pilot] resume: truncating items {len(raw)} -> {n} (pool smaller than checkpoint)",
                flush=True,
            )
        for i in range(min(len(raw), n)):
            x = raw[i]
            if isinstance(x, dict):
                items_out[i] = x

    if args.dry_run:
        for d in chosen[:3]:
            t = _render_transcript(d)
            print(f"--- dry-run sample {d.get('character_id')} len={len(t)} chars ---")
            print(t[:500] + ("…" if len(t) > 500 else ""))
        print("[pilot] dry-run: no API calls")
        return

    system = _load_system_prompt()
    workers = max(1, int(args.workers))
    ck_every = max(1, int(args.checkpoint_every))

    todo = [i for i in range(n) if not _item_extraction_ok(items_out[i])]
    if not todo:
        print("[pilot] nothing to do (all items already ok)", flush=True)
        return

    tls = threading.local()
    ck_lock = threading.Lock()
    done_since_ckpt = 0

    def _thread_client() -> LLMClient:
        c = getattr(tls, "client", None)
        if c is None:
            c = LLMClient(model=args.model, temperature=0.2, max_tokens=4096)
            tls.client = c
        return c

    def _write_checkpoint() -> None:
        payload = {
            "meta": {
                "model": args.model,
                "seed": args.seed,
                "source_name": source_name,
                "env_file": str((REPO / ".env").resolve()),
                "dialogues_source": source_meta,
                "workers": workers,
                "checkpoint_every": ck_every,
            },
            "items": items_out,
        }
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def _process_index(i: int) -> None:
        nonlocal done_since_ckpt
        d = chosen[i]
        cid = str(d.get("character_id", ""))
        transcript = _render_transcript(d)
        user = (
            "以下是同一来访者与咨询师的多轮逐字稿（中文或英文均可）。"
            "请只依据已出现内容归纳 MI Profile，自然语言字段统一用简体中文输出，"
            "输出单个 JSON 对象。\n\n【逐字稿开始】\n"
            f"{transcript}\n【逐字稿结束】"
        )
        item: dict[str, Any] = {
            "character_id": cid,
            "dialogue_id": d.get("dialogue_id"),
            "mi_profile": None,
            "raw_response": "",
            "parse_error": "",
            "schema_errors": [],
        }
        try:
            raw_resp = _thread_client().chat(system, user)
            item["raw_response"] = raw_resp
            obj = _extract_json(raw_resp)
            item["mi_profile"] = obj
            item["schema_errors"] = _validate_mi_profile(obj)
        except Exception as e:  # noqa: BLE001
            item["parse_error"] = repr(e)
        time.sleep(args.sleep)
        print(
            f"[pilot] idx={i} {cid} parse_error={bool(item['parse_error'])} "
            f"schema_errs={len(item['schema_errors'])}",
            flush=True,
        )
        with ck_lock:
            items_out[i] = item
            done_since_ckpt += 1
            if done_since_ckpt >= ck_every:
                _write_checkpoint()
                done_since_ckpt = 0

    print(
        f"[pilot] run {len(todo)}/{n} dialogues workers={workers} checkpoint_every={ck_every}",
        flush=True,
    )
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(_process_index, i) for i in todo]
        for fut in as_completed(futures):
            fut.result()
    _write_checkpoint()


if __name__ == "__main__":
    main()
