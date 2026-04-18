"""
run_mesc_profile_extraction.py
──────────────────────────────
Re-extract MESC Background Profiles from the **clean** source
(MESC_from_csv.json, no visual contamination).

Replaces workspace/results/profiles/mesc.json.

The original profiles were extracted from MESC_merged.json (contaminated),
causing ~60/1019 profiles to contain visual-model descriptions
("A young woman...", "appears to be...") absorbed from the raw text.

Usage (from repo root):
  nohup /path/to/python -u workspace/scripts/run_mesc_profile_extraction.py \
      > workspace/results/profiles/logs/mesc_v3b_rerun.log 2>&1 &
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

# ── Path setup ────────────────────────────────────────────────────────────────
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "workspace/scripts"))

from profile_pipeline.client import LLMClient
from profile_pipeline.extractor import ProfileExtractor
from profile_pipeline.io_utils import (
    load_existing_profiles,
    existing_id_set,
    save_profiles,
    profile_to_record,
)
from profile_pipeline.types import TranscriptSample

# ── Config ────────────────────────────────────────────────────────────────────
SOURCE_PATH = REPO / "workspace/dataset/MESC_from_csv.json"
OUTPUT_PATH = REPO / "workspace/results/profiles/mesc.json"
MODEL       = "gpt-5.4-mini"       # yunwu.ai relay
SAVE_EVERY  = 20                   # checkpoint frequency
SLEEP_BETWEEN = 0.3               # seconds between API calls


def render_transcript(dialogue: list[dict]) -> str:
    """Render a list of turns as plain-text transcript for the LLM."""
    lines = []
    for turn in dialogue:
        spk = "Client" if turn.get("speaker") == "user" else "Therapist"
        text = (turn.get("text") or "").strip()
        if text:
            lines.append(f"{spk}: {text}")
    return "\n".join(lines)


def main() -> None:
    # Load clean dialogue source
    dialogues = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))

    # Resume: skip already-processed sample_ids
    existing = load_existing_profiles(str(OUTPUT_PATH))
    done_ids = existing_id_set(existing)
    records: list[dict] = list(existing)

    remaining = [d for d in dialogues if f"mesc_{d['dialogue_id']}" not in done_ids]

    print(f"Dataset      : mesc  ({SOURCE_PATH.name})")
    print(f"Total samples: {len(dialogues)}")
    print(f"Already done : {len(done_ids)}")
    print(f"Remaining    : {len(remaining)}")

    if not remaining:
        print("Nothing to do — all samples already processed.")
        return

    client    = LLMClient(model=MODEL)
    extractor = ProfileExtractor(client)

    for i, dlg in enumerate(remaining, start=1):
        sample_id = f"mesc_{dlg['dialogue_id']}"
        transcript = render_transcript(dlg.get("dialog", []))

        sample = TranscriptSample(
            sample_id=sample_id,
            transcript_text=transcript,
            language="en",
            metadata={
                "problem_type": dlg.get("problem_type", ""),
                "situation":    dlg.get("situation", ""),
            },
        )

        profile = extractor.extract(sample)
        records.append(profile_to_record(profile))

        status = "✗ " + profile.parse_error[:60] if profile.parse_error else "✓"
        total_done = len(done_ids) + i
        print(f"[{total_done:4d}/{len(dialogues)}] {sample_id}  {status}")

        if i % SAVE_EVERY == 0:
            save_profiles(str(OUTPUT_PATH), records)
            print(f"  → checkpoint saved ({len(records)} profiles)")

        time.sleep(SLEEP_BETWEEN)

    # Final save
    save_profiles(str(OUTPUT_PATH), records)
    print(f"\nDone. {len(records)} profiles saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
