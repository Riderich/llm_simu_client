#!/usr/bin/env python3
"""
Pilot: extract MI-aligned final profiles from RECAP dialogues.

API 密钥：固定读取仓库根 `.env`（override=False）。

Usage (repo root):
  python3 data_scripts/extract_mi_profile_pilot.py --dry-run
  python3 data_scripts/extract_mi_profile_pilot.py --max-dialogues 10
  python3 data_scripts/extract_mi_profile_pilot.py --resume
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]

# 固定使用仓库根 `.env`（OPENAI_API_KEY / QWEN_API_KEY / OPENAI_BASE_URL 等）
from dotenv import load_dotenv

load_dotenv(REPO / ".env", override=False)

SCRIPTS = REPO / "workspace" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from profile_pipeline.client import LLMClient  # noqa: E402


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
    turns = sorted(dlg.get("dialogue", []), key=lambda t: t.get("turn_pos", 0))
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


def main() -> None:
    ap = argparse.ArgumentParser(description="MI Profile pilot on RECAP dialogues; 使用仓库根 .env")
    ap.add_argument(
        "--recap-dialogues",
        type=Path,
        default=REPO / "workspace/results/recap/dialogues.json",
        help="RECAP 整段对话 JSON（列表）；默认 results 真源",
    )
    ap.add_argument("--max-dialogues", type=int, default=10)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--min-client-turns", type=int, default=2)
    ap.add_argument("--model", default="deepseek-v4-flash")
    ap.add_argument("--sleep", type=float, default=0.35)
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=REPO / "workspace/results/profiles/pilot_mi",
        help="试点产出目录；默认 results/profiles/pilot_mi/",
    )
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()

    dlg_path = args.recap_dialogues.resolve()
    dialogues = json.loads(dlg_path.read_text(encoding="utf-8"))
    source_meta: dict[str, Any] = {
        "kind": "recap_dialogues",
        "path": str(dlg_path.relative_to(REPO)),
        "dialogues_total": len(dialogues),
    }

    pool = [d for d in dialogues if _client_turns(d) >= args.min_client_turns]
    rnd = random.Random(args.seed)
    rnd.shuffle(pool)
    chosen = pool[: args.max_dialogues]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    selection = {
        "env_file": str((REPO / ".env").resolve()),
        "dialogues_source": source_meta,
        "seed": args.seed,
        "max_dialogues": args.max_dialogues,
        "min_client_turns": args.min_client_turns,
        "chosen_count": len(chosen),
        "character_ids": [d.get("character_id") for d in chosen],
        "dialogue_ids": [d.get("dialogue_id") for d in chosen],
    }
    sel_path = args.out_dir / "selection.json"
    sel_path.write_text(json.dumps(selection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[pilot] wrote {sel_path.relative_to(REPO)} ({len(chosen)} dialogues)")

    out_path = args.out_dir / "recap_profiles.json"
    done: dict[str, dict[str, Any]] = {}
    if args.resume and out_path.exists():
        prev = json.loads(out_path.read_text(encoding="utf-8"))
        for it in prev.get("items", []):
            cid = str(it.get("character_id", ""))
            if cid and not it.get("parse_error") and it.get("mi_profile"):
                done[cid] = it

    items_out: list[dict[str, Any]] = []

    if args.dry_run:
        for d in chosen[:3]:
            t = _render_transcript(d)
            print(f"--- dry-run sample {d.get('character_id')} len={len(t)} chars ---")
            print(t[:500] + ("…" if len(t) > 500 else ""))
        print("[pilot] dry-run: no API calls")
        return

    system = _load_system_prompt()
    client = LLMClient(model=args.model, temperature=0.2, max_tokens=4096)

    def _write_checkpoint() -> None:
        payload = {
            "meta": {
                "model": args.model,
                "seed": args.seed,
                "env_file": str((REPO / ".env").resolve()),
                "dialogues_source": source_meta,
            },
            "items": items_out,
        }
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for d in chosen:
        cid = str(d.get("character_id", ""))
        if cid in done:
            items_out.append(done[cid])
            print(f"[skip] {cid} (resume)")
            continue
        transcript = _render_transcript(d)
        user = (
            "以下是同一来访者与咨询师的多轮中文逐字稿。请只依据已出现内容归纳 MI Profile，"
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
            raw = client.chat(system, user)
            item["raw_response"] = raw
            obj = _extract_json(raw)
            item["mi_profile"] = obj
            item["schema_errors"] = _validate_mi_profile(obj)
        except Exception as e:  # noqa: BLE001
            item["parse_error"] = repr(e)
        items_out.append(item)
        _write_checkpoint()
        print(f"[pilot] {cid} parse_error={bool(item['parse_error'])} schema_errs={len(item['schema_errors'])}")
        time.sleep(args.sleep)


if __name__ == "__main__":
    main()
