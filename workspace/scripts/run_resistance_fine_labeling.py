"""
run_resistance_fine_labeling.py
─────────────────────────────────
Unified entry point for PsyFIRE 13-class fine-grained resistance labeling
using the local RECAP transformer model.

Replaces:
  annomi_resistance_fine.py
  esconv_resistance_fine.py
  mesc_resistance_fine.py   (resistance step only; CBS step → run_cbs_labeling.py)

Usage (from repo root):
  python workspace/scripts/run_resistance_fine_labeling.py --dataset annomi --gpu 4
  python workspace/scripts/run_resistance_fine_labeling.py --dataset esconv --gpu 0
  python workspace/scripts/run_resistance_fine_labeling.py --dataset mesc   --gpu 4

Background:
  nohup python -u workspace/scripts/run_resistance_fine_labeling.py \
      --dataset annomi --gpu 4 \
      > workspace/results/logs/annomi_resistance_fine.log 2>&1 &
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Any

# GPU must be set before torch import — parse early
def _pre_parse_gpu() -> str:
    for i, arg in enumerate(sys.argv):
        if arg in ("--gpu", "-g") and i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return "0"

_gpu = _pre_parse_gpu()
os.environ.setdefault("CUDA_VISIBLE_DEVICES", _gpu)

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "workspace/scripts"))

from resistance_pipeline.fine_prompts import (
    build_resistance_fine_user_prompt,
    normalize_label,
)

# ── Default paths & model ─────────────────────────────────────────────────

_DEFAULT_MODEL_PATH = str(
    REPO / "ClientResistance-Model-Share/only_resistance_share_model"
)

_DATASET_CONFIGS: dict[str, dict[str, Any]] = {
    "annomi": {
        "input":          REPO / "workspace/results/annomi_full_binary_recap.json",
        "output":         REPO / "workspace/results/annomi_resistance.json",
        "filter_field":   "binary_label",
        "filter_value":   "阻抗",
        "response_field": "response",
        "context_field":  "context",
    },
    "esconv": {
        "input":          REPO / "workspace/results/esconv_resistance.json",
        "output":         REPO / "workspace/results/esconv_resistance_fine.json",
        "filter_field":   "binary_label",
        "filter_value":   "阻抗",
        "response_field": "response",
        "context_field":  "context",
    },
    "mesc": {
        "input":          REPO / "workspace/results/mesc_binary_clean.json",
        "output":         REPO / "workspace/results/mesc_resistance.json",
        "filter_field":   "binary_label",
        "filter_value":   "阻抗",
        "response_field": "response",
        "context_field":  "context",
    },
}

SAVE_EVERY = 100


def _format_context(ctx: Any, max_turns: int = 4) -> str:
    if isinstance(ctx, str):
        return ctx.strip()
    if not isinstance(ctx, list) or not ctx:
        return ""
    lines: list[str] = []
    for turn in ctx[-max_turns:]:
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


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="PsyFIRE 13-class fine-grained resistance labeling (local model)."
    )
    p.add_argument("--dataset", required=True, choices=list(_DATASET_CONFIGS))
    p.add_argument("--input",   default=None, help="Override default input path.")
    p.add_argument("--output",  default=None, help="Override default output path.")
    p.add_argument("--model-path", default=_DEFAULT_MODEL_PATH,
                   help="Path to the local resistance model.")
    p.add_argument("--gpu", "-g", default="0",
                   help="GPU index for CUDA_VISIBLE_DEVICES (already applied at startup).")
    p.add_argument("--max-tokens",  type=int, default=1536)
    p.add_argument("--save-every",  type=int, default=SAVE_EVERY)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    cfg  = _DATASET_CONFIGS[args.dataset]

    input_path  = Path(args.input)  if args.input  else cfg["input"]
    output_path = Path(args.output) if args.output else cfg["output"]
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data: list[dict] = json.loads(input_path.read_text(encoding="utf-8"))
    res_samples = [
        s for s in data
        if s.get(cfg["filter_field"]) == cfg["filter_value"]
    ]

    print(f"Dataset       : {args.dataset}")
    print(f"GPU           : {os.environ.get('CUDA_VISIBLE_DEVICES')}")
    print(f"阻抗样本总数   : {len(res_samples)}", flush=True)

    # Resume
    records: list[dict] = []
    done_ids: set[str]  = set()
    if output_path.exists():
        records  = json.loads(output_path.read_text(encoding="utf-8"))
        done_ids = {r["sample_id"] for r in records}
        print(f"已完成        : {len(done_ids)}", flush=True)

    todo = [s for s in res_samples if s.get("sample_id") not in done_ids]
    if not todo:
        print("所有样本已处理完成！")
        _print_distribution(records)
        return

    print(f"待处理        : {len(todo)}", flush=True)
    print("加载模型...", flush=True)

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from tqdm import tqdm

    tokenizer = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        args.model_path,
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None,
        trust_remote_code=True,
    )
    print(f"模型加载完成: {model.device}", flush=True)

    for i, sample in enumerate(tqdm(todo, desc=f"{args.dataset} resistance fine"), start=1):
        ctx  = _format_context(sample.get(cfg["context_field"], []))
        resp = (sample.get(cfg["response_field"]) or "").strip()
        prompt = build_resistance_fine_user_prompt(ctx, resp)

        inputs = tokenizer(
            prompt, return_tensors="pt",
            truncation=True, max_length=args.max_tokens,
        )
        inputs = {k: v.to(model.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model.generate(
                **inputs, max_new_tokens=15, do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )
        raw_text = tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True
        ).strip()

        fine_label, fine_category = normalize_label(raw_text)
        total_done = len(done_ids) + i

        records.append({
            "sample_id":     sample["sample_id"],
            "binary_label":  "阻抗",
            "fine_label":    fine_label,
            "fine_category": fine_category,
            "response":      resp,
        })

        print(
            f"[{total_done:5d}/{len(res_samples)}] {sample['sample_id']}"
            f"  → {fine_label}  ({fine_category})",
            flush=True,
        )

        if i % args.save_every == 0:
            output_path.write_text(
                json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            print(f"  → checkpoint saved ({len(records)} records)", flush=True)

    output_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✓ 完成 → {output_path}  ({len(records)} 条)", flush=True)
    _print_distribution(records)


def _print_distribution(records: list[dict]) -> None:
    print("\nPsyFIRE 分布:")
    for cat, cnt in Counter(r["fine_category"] for r in records).most_common():
        print(f"  {cat}: {cnt}")


if __name__ == "__main__":
    main()
