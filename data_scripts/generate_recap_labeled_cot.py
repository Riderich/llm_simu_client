#!/usr/bin/env python3
"""
为 RECAP 中带 阻抗/合作 标签的来访轮生成中文 COT（与临床 cot/*.json 对齐）。

输出 JSON 对象：键为 sample_id（``recap:{character_id}:{turn_pos}``），值含
internal、raw_cot、cot_prompt_key 等。供 prepare_training_splits.py --recap-cot-path 合并。

依赖：DEEPSEEK_API_KEY（见 workspace/src/deepseek_client.py）。

示例：
  python data_scripts/generate_recap_labeled_cot.py --max-items 5
  python data_scripts/generate_recap_labeled_cot.py --workers 4 --sleep 0.2
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "workspace" / "src"))

from deepseek_client import DeepSeekClient  # noqa: E402

RESULTS = REPO / "workspace" / "results"
DEFAULT_DIALOGUES = RESULTS / "recap" / "dialogues.json"
DEFAULT_PROFILES = RESULTS / "profiles" / "recap.json"
DEFAULT_OUT = RESULTS / "recap" / "recap_labeled_cot.json"

PROFILE_USED_KEYS = (
    "background",
    "self_view_of_problem",
    "resistance_drivers",
    "ambivalence",
    "values_and_stakes",
    "key_facts",
)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def recap_profile_used_blob(record: dict[str, Any]) -> dict[str, Any]:
    return {k: record[k] for k in PROFILE_USED_KEYS if k in record}


def load_profile_by_character(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    data = _load_json(path)
    if not isinstance(data, list):
        return {}
    out: dict[str, dict[str, Any]] = {}
    for item in data:
        sid = item.get("sample_id")
        if sid is not None:
            out[str(sid)] = recap_profile_used_blob(item)
    return out


def _turns_before(dialogue: list[dict[str, Any]], turn_pos: int) -> list[dict[str, Any]]:
    return [
        {"speaker": t.get("speaker"), "text": t.get("text")}
        for t in dialogue
        if t.get("turn_pos", -1) < turn_pos
    ]


def _last_therapist_utterance(dialogue: list[dict[str, Any]], turn_pos: int) -> str:
    for t in reversed(dialogue):
        pos = t.get("turn_pos", -1)
        if pos >= turn_pos:
            continue
        if t.get("speaker") == "therapist":
            return str(t.get("text", ""))
    return ""


def parse_internal_block(text: str) -> tuple[str | None, str | None]:
    m = re.search(r"<internal>([\s\S]*?)</internal>", text, re.IGNORECASE)
    if not m:
        return None, None
    inner = m.group(1).strip()
    raw = m.group(0).strip()
    return inner or None, raw or None


SYSTEM_PROMPT = (
    "你是心理咨询语料作者，用简体中文书写来访者的内心独白。"
    "只输出模型被要求的一段内容，不要 JSON，不要 Markdown 代码块。"
)

USER_TEMPLATE = """请为下面这一轮「来访者的外显回应」写内心独白（chain-of-thought），用于训练来访者模拟模型。

硬性格式（必须严格遵守）：
1) 全文只输出一个 ``<internal>...</internal>`` 块。
2) 块内先写 ``[Perception]`` 开头的一段，空一行，再写 ``[Decision]`` 开头的一段（标题行用英文，正文用自然中文口语）。
3) 内容须与给定外显话一致：解释来访者如何理解上一句咨询师的话、情绪与防御，以及为何选择这样说/这样简短回应。
4) 不要编造未在对话中出现的临床诊断；不要改写给定的行为细标签名称。

行为标签（参考）：
- binary_label: {binary_label}
- fine_label: {fine_label}
- fine_category: {fine_category}

来访者背景与动力摘要（JSON，可能为空）：
{profile_json}

对话上文（含说话人）：
{context_json}

当前咨询师话轮：
{therapist_turn}

来访者外显回应（本轮须解释其内心）：
{client_response}
"""


def build_user_prompt(
    *,
    binary_label: str,
    fine_label: str | None,
    fine_category: str | None,
    profile_used: dict[str, Any] | None,
    context: list[dict[str, Any]],
    therapist_turn: str,
    client_response: str,
) -> str:
    prof = profile_used if profile_used else {}
    return USER_TEMPLATE.format(
        binary_label=binary_label,
        fine_label=fine_label or "",
        fine_category=fine_category or "",
        profile_json=json.dumps(prof, ensure_ascii=False, indent=2),
        context_json=json.dumps(context, ensure_ascii=False, indent=2),
        therapist_turn=therapist_turn,
        client_response=client_response,
    )


def iter_labeled_client_turns(
    dialogues: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for dlg in dialogues:
        char_id = dlg.get("character_id")
        dialogue = dlg.get("dialogue", [])
        for turn in dialogue:
            if turn.get("speaker") != "client":
                continue
            bl = turn.get("binary_label")
            if bl not in ("阻抗", "合作"):
                continue
            turn_pos = turn.get("turn_pos", -1)
            sample_id = f"recap:{char_id}:{turn_pos}"
            tasks.append(
                {
                    "sample_id": sample_id,
                    "character_id": char_id,
                    "turn_pos": turn_pos,
                    "binary_label": bl,
                    "fine_label": turn.get("fine_label"),
                    "fine_category": turn.get("fine_category"),
                    "context": _turns_before(dialogue, turn_pos),
                    "therapist_turn": _last_therapist_utterance(dialogue, turn_pos),
                    "client_response": str(turn.get("text", "")),
                }
            )
    return tasks


_write_lock = threading.Lock()


def process_one(
    client: DeepSeekClient,
    row: dict[str, Any],
    profile_by_char: dict[str, dict[str, Any]],
    *,
    max_retries: int,
) -> dict[str, Any]:
    char_key = str(row.get("character_id") or "")
    profile_used = profile_by_char.get(char_key)
    cot_key = row.get("fine_label") or row.get("fine_category") or row.get("binary_label") or ""
    user = build_user_prompt(
        binary_label=str(row.get("binary_label")),
        fine_label=row.get("fine_label"),
        fine_category=row.get("fine_category"),
        profile_used=profile_used,
        context=row.get("context") or [],
        therapist_turn=row.get("therapist_turn") or "",
        client_response=row.get("client_response") or "",
    )
    last_err = ""
    for attempt in range(max_retries):
        raw = client.chat(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user},
            ],
            temperature=0.25,
            max_tokens=2048,
        )
        internal, raw_cot = parse_internal_block(raw)
        if internal and raw_cot:
            return {
                "sample_id": row["sample_id"],
                "character_id": row.get("character_id"),
                "turn_pos": row.get("turn_pos"),
                "internal": internal,
                "raw_cot": raw_cot,
                "cot_prompt_key": str(cot_key),
                "parse_error": "",
            }
        last_err = "missing_<internal>_block"
        user = user + "\n\n【上次输出未包含合法 <internal>...</internal>，请严格按格式重试。】\n"
    return {
        "sample_id": row["sample_id"],
        "character_id": row.get("character_id"),
        "turn_pos": row.get("turn_pos"),
        "internal": "",
        "raw_cot": "",
        "cot_prompt_key": str(cot_key),
        "parse_error": last_err or "failed",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dialogues", type=Path, default=DEFAULT_DIALOGUES)
    parser.add_argument("--profiles", type=Path, default=DEFAULT_PROFILES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--sleep", type=float, default=0.0, help="每条请求后睡眠秒数（限流）")
    parser.add_argument("--max-items", type=int, default=0, help=">0 时仅处理前 N 条（调试用）")
    parser.add_argument("--max-retries", type=int, default=2)
    args = parser.parse_args()

    dialogues = _load_json(args.dialogues)
    if not isinstance(dialogues, list):
        raise SystemExit("dialogues 必须是 JSON 数组")
    profile_by_char = load_profile_by_character(args.profiles)
    tasks = iter_labeled_client_turns(dialogues)
    if args.max_items > 0:
        tasks = tasks[: args.max_items]

    out_path = args.out
    existing: dict[str, Any] = {}
    if out_path.exists():
        raw = _load_json(out_path)
        if isinstance(raw, dict):
            existing = raw
        else:
            raise SystemExit("已有输出文件格式须为 JSON 对象（sample_id -> 记录）")

    pending = [t for t in tasks if not (existing.get(t["sample_id"], {}).get("internal") or "").strip()]
    print(
        json.dumps(
            {
                "total_labeled_tasks": len(tasks),
                "already_done": len(tasks) - len(pending),
                "to_run": len(pending),
                "out": str(out_path),
            },
            ensure_ascii=False,
        )
    )
    if not pending:
        return

    if args.workers <= 1:
        client = DeepSeekClient()

        def run_row(row: dict[str, Any]) -> dict[str, Any]:
            return process_one(client, row, profile_by_char, max_retries=args.max_retries)
    else:

        def run_row(row: dict[str, Any]) -> dict[str, Any]:
            return process_one(DeepSeekClient(), row, profile_by_char, max_retries=args.max_retries)

    if args.workers <= 1:
        for row in pending:
            rec = run_row(row)
            if args.sleep > 0:
                time.sleep(args.sleep)
            with _write_lock:
                existing[rec["sample_id"]] = rec
                _atomic_write_json(out_path, existing)
            print(rec.get("sample_id"), "ok" if not rec.get("parse_error") else rec.get("parse_error"))
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(run_row, row): row for row in pending}
            for fut in as_completed(futs):
                rec = fut.result()
                if args.sleep > 0:
                    time.sleep(args.sleep)
                with _write_lock:
                    existing[rec["sample_id"]] = rec
                    _atomic_write_json(out_path, existing)
                print(rec.get("sample_id"), "ok" if not rec.get("parse_error") else rec.get("parse_error"))


if __name__ == "__main__":
    main()
