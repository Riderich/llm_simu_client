"""
run_profile_extraction.py
─────────────────────────
CLI entry point for Background Profile extraction.

Supported datasets:
  annomi  →  data/processed/AnnoMI-full.json       (English, with fine-grained labels)
  recap   →  workspace/dataset/RECAP.json           (Chinese)
  esconv  →  workspace/dataset/ESConv.json          (English, with labels)
  mesc    →  workspace/dataset/MESC_merged.json     (English, with labels)

Examples:
  # AnnoMI — all 133 transcripts (label files auto-detected)
  python run_profile_extraction.py \\
      --input  data/processed/AnnoMI-full.json \\
      --output workspace/results/profiles/annomi_profiles.json \\
      --data-format annomi

  # ESConv — 50-sample probe (label files auto-detected)
  python run_profile_extraction.py \\
      --input  workspace/dataset/ESConv.json \\
      --output workspace/results/profiles/esconv_profiles_probe.json \\
      --data-format esconv \\
      --max-samples 50

  # MESC — 50-sample probe
  python run_profile_extraction.py \\
      --input  workspace/dataset/MESC_merged.json \\
      --output workspace/results/profiles/mesc_profiles_probe.json \\
      --data-format mesc \\
      --max-samples 50

  # Override model and temperature
  python run_profile_extraction.py \\
      --input  data/processed/AnnoMI-full.json \\
      --output workspace/results/profiles/annomi_profiles.json \\
      --data-format annomi \\
      --model qwen-max \\
      --temperature 0.3
"""

from __future__ import annotations

import argparse

from profile_pipeline.runner import run_profile_extraction


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract client Background Profiles from therapy transcripts.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    # ── I/O ───────────────────────────────────────────────────────────────────
    parser.add_argument("--input", required=True, help="Path to input dataset JSON")
    parser.add_argument("--output", required=True, help="Path to output profiles JSON")
    parser.add_argument(
        "--data-format",
        required=True,
        choices=["annomi", "recap", "esconv", "mesc"],
        help="Dataset format (determines loader and prompt language)",
    )
    # ── Model ─────────────────────────────────────────────────────────────────
    parser.add_argument(
        "--model",
        default="deepseek-v3.2",
        help="LLM model name (default: deepseek-v3.2)",
    )
    parser.add_argument("--api-key", default=None, help="Override API key from env")
    parser.add_argument("--base-url", default=None, help="Override API base URL")
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Sampling temperature (default: 0.2 — deterministic extraction)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=1500,
        help="Max tokens for profile response (default: 1500)",
    )
    # ── Run control ───────────────────────────────────────────────────────────
    parser.add_argument(
        "--save-every",
        type=int,
        default=10,
        help="Checkpoint every N profiles (default: 10)",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=None,
        help="Cap on number of samples (useful for probing)",
    )
    # ── Label files (annomi / esconv / mesc) ─────────────────────────────────
    parser.add_argument(
        "--label-coop",
        default=None,
        help="Path to cooperation label JSON (default: auto-detected per dataset)",
    )
    parser.add_argument(
        "--label-res",
        default=None,
        help="Path to resistance label JSON (default: auto-detected per dataset)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_profile_extraction(
        input_path=args.input,
        output_path=args.output,
        data_format=args.data_format,
        model=args.model,
        api_key=args.api_key,
        base_url=args.base_url,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        save_every=args.save_every,
        max_samples=args.max_samples,
        label_coop_path=args.label_coop,
        label_res_path=args.label_res,
    )


if __name__ == "__main__":
    main()
