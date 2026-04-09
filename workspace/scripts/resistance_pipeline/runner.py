from __future__ import annotations

from collections import Counter
from dataclasses import asdict

from .inference import TransformersBinaryClassifier
from .io_utils import existing_id_set, load_existing_results, write_json
from .loaders import filter_unprocessed, load_annomi_full, load_extes
from .types import Sample


def load_samples(data_format: str, input_path: str, max_turns: int, max_samples: int | None) -> list[Sample]:
    if data_format == "annomi_full":
        return load_annomi_full(input_path, max_turns=max_turns, max_samples=max_samples)
    if data_format == "extes":
        return load_extes(input_path, max_turns=max_turns, max_samples=max_samples)
    raise ValueError(f"Unsupported data format: {data_format}")


def run_binary_classification(
    *,
    input_path: str,
    output_path: str,
    data_format: str,
    model_path: str,
    gpu: str,
    batch_size: int,
    save_every: int,
    max_turns: int,
    max_samples: int | None,
) -> None:
    existing_records = load_existing_results(output_path)
    seen = existing_id_set(existing_records)

    all_samples = load_samples(data_format, input_path, max_turns=max_turns, max_samples=max_samples)
    remaining = filter_unprocessed(all_samples, seen)

    print(f"Loaded {len(all_samples)} samples from {data_format}")
    print(f"Existing records: {len(existing_records)}")
    print(f"Remaining: {len(remaining)}")

    if not remaining:
        print("No remaining samples. Exit.")
        return

    classifier = TransformersBinaryClassifier(model_path=model_path, gpu=gpu)
    output = list(existing_records)
    processed_since_save = 0

    for start in range(0, len(remaining), batch_size):
        batch = remaining[start : start + batch_size]
        preds = classifier.predict(batch)

        for sample, pred in zip(batch, preds):
            output.append(
                {
                    "sample_id": sample.sample_id,
                    "context": sample.context,
                    "response": sample.response,
                    "binary_label": pred.binary_label,
                    "raw_output": pred.raw_output,
                    "metadata": sample.metadata,
                }
            )
            processed_since_save += 1

        if processed_since_save >= save_every or start + batch_size >= len(remaining):
            write_json(output_path, output)
            processed_since_save = 0
            print(f"Saved progress: {len(output)}/{len(all_samples)}")

    dist = Counter([x.get("binary_label", "UNKNOWN") for x in output])
    print("Binary distribution:", dict(dist))

