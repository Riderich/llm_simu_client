from __future__ import annotations

import argparse

from resistance_pipeline.runner import run_binary_classification


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Structured binary resistance classification for AnnoMI-full / MESC / ExTES."
    )
    parser.add_argument("--input", required=True, help="Path to dataset JSON")
    parser.add_argument("--output", required=True, help="Path to output JSON")
    parser.add_argument(
        "--data-format",
        required=True,
        choices=["annomi_full", "mesc", "extes"],
        help="Dataset format loader",
    )
    parser.add_argument(
        "--model",
        default="/data5/zxj/llm_simu_client/ClientResistance-Model-Share/binary_share_model",
        help="Binary RECAP model path",
    )
    parser.add_argument("--gpu", default="0", help="GPU id for inference")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--save-every", type=int, default=50)
    parser.add_argument("--max-turns", type=int, default=6, help="Number of context turns to keep")
    parser.add_argument("--max-samples", type=int, default=None, help="Optional sample cap for dry/probe runs")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_binary_classification(
        input_path=args.input,
        output_path=args.output,
        data_format=args.data_format,
        model_path=args.model,
        gpu=args.gpu,
        batch_size=args.batch_size,
        save_every=args.save_every,
        max_turns=args.max_turns,
        max_samples=args.max_samples,
    )


if __name__ == "__main__":
    main()

