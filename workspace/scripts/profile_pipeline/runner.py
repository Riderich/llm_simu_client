from __future__ import annotations

from .client import LLMClient
from .extractor import ProfileExtractor
from .io_utils import (
    existing_id_set,
    load_existing_profiles,
    profile_to_record,
    save_profiles,
)
from .loaders import load_samples


def run_profile_extraction(
    *,
    input_path: str,
    output_path: str,
    data_format: str,
    model: str,
    api_key: str | None,
    base_url: str | None,
    temperature: float,
    max_tokens: int,
    save_every: int,
    max_samples: int | None,
    label_coop_path: str | None = None,
    label_res_path: str | None = None,
) -> None:
    # ── Resume from checkpoint ────────────────────────────────────────────────
    existing = load_existing_profiles(output_path)
    seen = existing_id_set(existing)

    # ── Load dataset ──────────────────────────────────────────────────────────
    all_samples = load_samples(
        data_format,
        input_path,
        max_samples=max_samples,
        label_coop_path=label_coop_path,
        label_res_path=label_res_path,
    )
    remaining = [s for s in all_samples if s.sample_id not in seen]

    print(f"Dataset      : {data_format}  ({input_path})")
    print(f"Total samples: {len(all_samples)}")
    print(f"Already done : {len(existing)}")
    print(f"Remaining    : {len(remaining)}")

    if not remaining:
        print("Nothing to do — all samples already processed.")
        _print_summary(existing)
        return

    # ── Build pipeline ────────────────────────────────────────────────────────
    client = LLMClient(
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    extractor = ProfileExtractor(client)

    records = list(existing)
    pending_save = 0

    for i, sample in enumerate(remaining, start=1):
        profile = extractor.extract(sample)
        record = profile_to_record(profile)
        records.append(record)
        pending_save += 1

        status = "✓" if not profile.parse_error else f"✗ ({profile.parse_error[:60]})"
        print(f"[{len(existing) + i:4d}/{len(all_samples)}] {sample.sample_id}  {status}")

        if pending_save >= save_every or i == len(remaining):
            save_profiles(output_path, records)
            pending_save = 0
            print(f"  💾 Saved {len(records)} profiles → {output_path}")

    _print_summary(records)


def _print_summary(records: list[dict]) -> None:
    total = len(records)
    errors = sum(1 for r in records if r.get("parse_error"))
    print(f"\n── Summary ──────────────────────────")
    print(f"  Total profiles : {total}")
    print(f"  Parse errors   : {errors}")
    print(f"  Success rate   : {(total - errors) / total * 100:.1f}%" if total else "  No data.")
    if errors:
        print(f"\n  Failed sample IDs:")
        for r in records:
            if r.get("parse_error"):
                print(f"    {r['sample_id']}: {r['parse_error'][:80]}")
