"""
run_profile_extraction.py
──────────────────────────
Unified entry point for client-profile extraction across all datasets.

Replaces: run_mesc_profile_extraction.py (dataset-specific)

Usage (from repo root):
  python workspace/scripts/run_profile_extraction.py --dataset mesc
  python workspace/scripts/run_profile_extraction.py --dataset esconv --model gpt-4o-mini
  python workspace/scripts/run_profile_extraction.py --dataset annomi --output path/to/out.json

Supported datasets:  mesc | esconv | annomi | recap

Background (nohup):
  nohup python -u workspace/scripts/run_profile_extraction.py --dataset mesc \
      > workspace/results/logs/profiles/mesc_rerun.log 2>&1 &
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "workspace/scripts"))

from profile_pipeline import LLMClient  # re-exported, see workspace/src/llm_client.py
from profile_pipeline.extractor import ProfileExtractor
from profile_pipeline.io_utils import (
    existing_id_set,
    load_existing_profiles,
    profile_to_record,
    save_profiles,
)
from profile_pipeline.loaders import load_dataset

# ── Default output paths per dataset ─────────────────────────────────────

_DEFAULT_OUTPUTS: dict[str, Path] = {
    "mesc":   REPO / "workspace/results/profiles/mesc.json",
    "esconv": REPO / "workspace/results/profiles/esconv.json",
    "annomi": REPO / "workspace/results/profiles/annomi.json",
    "recap":  REPO / "workspace/results/profiles/recap_dedup.json",
}

# ── Default model ─────────────────────────────────────────────────────────

_DEFAULT_MODEL = "gpt-5.4-mini"

SAVE_EVERY    = 20
SLEEP_BETWEEN = 0.3


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Extract client background profiles via LLM.")
    p.add_argument(
        "--dataset", required=True,
        choices=["mesc", "esconv", "annomi", "recap"],
        help="Which dataset to process.",
    )
    p.add_argument("--input",  default=None, help="Override default input path.")
    p.add_argument("--output", default=None, help="Override default output path.")
    p.add_argument("--model",  default=_DEFAULT_MODEL, help="LLM model name.")
    p.add_argument("--save-every", type=int, default=SAVE_EVERY, help="Checkpoint frequency.")
    p.add_argument("--sleep", type=float, default=SLEEP_BETWEEN, help="Seconds between API calls.")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    output_path = Path(args.output) if args.output else _DEFAULT_OUTPUTS[args.dataset]
    output_path.parent.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.input) if args.input else None
    samples = load_dataset(args.dataset, path=input_path)

    existing = load_existing_profiles(str(output_path))
    done_ids = existing_id_set(existing)
    records: list[dict] = list(existing)

    remaining = [s for s in samples if s.sample_id not in done_ids]

    print(f"Dataset      : {args.dataset}")
    print(f"Model        : {args.model}")
    print(f"Total samples: {len(samples)}")
    print(f"Already done : {len(done_ids)}")
    print(f"Remaining    : {len(remaining)}")
    print(f"Output       : {output_path}", flush=True)

    if not remaining:
        print("Nothing to do — all samples already processed.")
        return

    client    = LLMClient(model=args.model)
    extractor = ProfileExtractor(client)

    for i, sample in enumerate(remaining, start=1):
        profile = extractor.extract(sample)
        records.append(profile_to_record(profile))

        status = "✗ " + (profile.parse_error or "")[:60] if profile.parse_error else "✓"
        total_done = len(done_ids) + i
        print(f"[{total_done:4d}/{len(samples)}] {sample.sample_id}  {status}", flush=True)

        if i % args.save_every == 0:
            save_profiles(str(output_path), records)
            print(f"  → checkpoint saved ({len(records)} profiles)", flush=True)

        time.sleep(args.sleep)

    save_profiles(str(output_path), records)
    print(f"\nDone. {len(records)} profiles saved to {output_path}")


if __name__ == "__main__":
    main()
