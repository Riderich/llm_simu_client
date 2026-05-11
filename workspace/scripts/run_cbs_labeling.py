"""
run_cbs_labeling.py
────────────────────
Unified entry point for CBS 2-8 cooperation sub-type labeling via Qwen API.

Replaces:
  annomi_coop_cbs.py   (input: labeled/annomi_binary.json → binary_label==合作)
  esconv_coop_cbs.py   (input: labeled/esconv_utterances.json → binary_label==合作)
  mesc_coop_cbs.py     (input: labeled/mesc_binary.json → binary_label==合作)

Usage (from repo root):
  python workspace/scripts/run_cbs_labeling.py --dataset annomi
  python workspace/scripts/run_cbs_labeling.py --dataset esconv --input path/to/file.json
  python workspace/scripts/run_cbs_labeling.py --dataset mesc --output path/to/out.json

Background:
  nohup python -u workspace/scripts/run_cbs_labeling.py --dataset annomi \
      > workspace/results/logs/annomi_cbs.log 2>&1 &
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "workspace/scripts"))
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from data_scripts.extes_pipeline.cbs_constants import CBS_CATEGORIES, CBS_SYSTEM_PROMPT

from profile_pipeline.client import LLMClient  # reuse unified LLM client

# CBS_SYSTEM_PROMPT / CBS_CATEGORIES live in data_scripts.extes_pipeline.cbs_constants (shared with ExtES local screen).

# ── Default paths per dataset ─────────────────────────────────────────────

_DATASET_CONFIGS: dict[str, dict[str, Any]] = {
    "annomi": {
        "input":          REPO / "workspace/results/labeled/annomi_binary.json",
        "output":         REPO / "workspace/results/labeled/annomi_coop.json",
        "filter_field":   "binary_label",
        "response_field": "response",
        "context_field":  "context",
    },
    "esconv": {
        "input":          REPO / "workspace/results/labeled/esconv_utterances.json",
        "output":         REPO / "workspace/results/labeled/esconv_coop.json",
        "filter_field":   "binary_label",
        "response_field": "response",
        "context_field":  "context",
    },
    "mesc": {
        "input":          REPO / "workspace/results/labeled/mesc_binary.json",
        "output":         REPO / "workspace/results/labeled/mesc_coop_all.json",
        "filter_field":   "binary_label",
        "response_field": "response",
        "context_field":  "context",
    },
}

SAVE_EVERY    = 100
SLEEP_BETWEEN = 0.3


# ── Helpers ───────────────────────────────────────────────────────────────

def _format_context(context: Any, max_turns: int = 2) -> str:
    if isinstance(context, str):
        return context.strip()
    if not isinstance(context, list) or not context:
        return ""
    lines: list[str] = []
    for turn in context[-max_turns:]:
        role = turn.get("speaker", turn.get("role", ""))
        text = turn.get("content", turn.get("text", "")).strip()
        if not text:
            continue
        if role in ("therapist", "supporter", "counselor"):
            label = "咨询师"
        elif role in ("client", "seeker", "user"):
            label = "来访者"
        else:
            label = role
        lines.append(f"{label}: {text}")
    return "\n".join(lines)


def _call_cbs(llm: LLMClient, context: str, response: str) -> str:
    user_msg = (
        f"对话上下文:\n{context}\n\n来访者话语:\n{response}\n\n"
        f"请分类为CBS 2-8之一，输出JSON格式。"
    )
    try:
        raw = llm.chat(
            system=CBS_SYSTEM_PROMPT,
            user=user_msg,
            temperature=0.1,
            max_tokens=50,
        )
        try:
            return json.loads(raw).get("cbs_type", "Unknown")
        except json.JSONDecodeError:
            for cat in CBS_CATEGORIES:
                if cat in raw:
                    return cat
            return "Unknown"
    except Exception as exc:
        print(f"  API Error: {exc}", flush=True)
        return "Error"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="CBS 2-8 cooperation sub-type labeling.")
    p.add_argument("--dataset", required=True, choices=list(_DATASET_CONFIGS),
                   help="Dataset to process.")
    p.add_argument("--input",   default=None, help="Override default input path.")
    p.add_argument("--output",  default=None, help="Override default output path.")
    p.add_argument("--model",   default="qwen-turbo", help="LLM model name.")
    p.add_argument("--max-turns", type=int, default=2,
                   help="Max context turns to include in the prompt.")
    p.add_argument("--save-every", type=int, default=SAVE_EVERY)
    p.add_argument("--sleep", type=float, default=SLEEP_BETWEEN)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    cfg  = _DATASET_CONFIGS[args.dataset]

    input_path  = Path(args.input)  if args.input  else cfg["input"]
    output_path = Path(args.output) if args.output else cfg["output"]
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data: list[dict] = json.loads(input_path.read_text(encoding="utf-8"))
    coop_samples = [s for s in data if s.get(cfg["filter_field"]) == "合作"]
    print(f"Dataset       : {args.dataset}")
    print(f"Model         : {args.model}")
    print(f"合作样本总数   : {len(coop_samples)}", flush=True)

    # Resume
    records: list[dict] = []
    done_ids: set[str]  = set()
    if output_path.exists():
        records  = json.loads(output_path.read_text(encoding="utf-8"))
        done_ids = {r["sample_id"] for r in records}
        print(f"已完成        : {len(done_ids)}", flush=True)

    todo = [s for s in coop_samples if s.get("sample_id") not in done_ids]
    if not todo:
        print("所有样本已处理完成！")
        _print_distribution(records)
        return

    print(f"待处理        : {len(todo)}", flush=True)
    llm = LLMClient(model=args.model)

    for i, sample in enumerate(todo, start=1):
        ctx  = _format_context(sample.get(cfg["context_field"], []), max_turns=args.max_turns)
        resp = (sample.get(cfg["response_field"]) or "").strip()
        cbs  = _call_cbs(llm, ctx, resp)

        records.append({
            "sample_id":    sample["sample_id"],
            "binary_label": "合作",
            "cbs_type":     cbs,
            "response":     resp,
        })

        total_done = len(done_ids) + i
        print(f"[{total_done:5d}/{len(coop_samples)}] {sample['sample_id']}  → {cbs}", flush=True)

        if i % args.save_every == 0:
            output_path.write_text(
                json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            print(f"  → checkpoint saved ({len(records)} records)", flush=True)

        time.sleep(args.sleep)

    output_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✓ 完成 → {output_path}  ({len(records)} 条)", flush=True)
    _print_distribution(records)


def _print_distribution(records: list[dict]) -> None:
    print("\nCBS 分布:")
    for cat, cnt in Counter(r["cbs_type"] for r in records).most_common():
        print(f"  {cat}: {cnt}")


if __name__ == "__main__":
    main()
