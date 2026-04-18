"""
build_mesc_from_csv.py
──────────────────────
Build MESC dialogue JSON from **raw** `data/raw/MESC.csv`.

Why: `workspace/dataset/MESC_merged.json` was produced by an older pipeline that
appended vision-model captions (`The speaker...`) to utterances. The raw CSV
does not contain those strings — it is the authoritative text source.

This script:
  1. Reads all rows from MESC.csv (Utterance, Speaker, Emotion, Strategy, ...).
  2. Groups by Dialogue_ID, sorts by Utterance_ID.
  3. Maps Speaker: Client → user, Therapist → sys (same as merged JSON).
  4. Merges consecutive rows from the **same** speaker (subtitle-style splits).
  5. Attaches `problem_type` and `situation` from `MESC_merged.json` by
     dialogue_id (CSV does not include these fields).

Output:
  workspace/dataset/MESC_from_csv.json

Usage (from repo root):
  python data_scripts/build_mesc_from_csv.py
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CSV_PATH = REPO / "data/raw/MESC.csv"
META_PATH = REPO / "workspace/dataset/MESC_merged.json"
OUT_PATH = REPO / "workspace/dataset/MESC_from_csv.json"


def most_common_last(values: list[str]) -> str:
    counts = Counter(values)
    max_count = max(counts.values())
    candidates = [v for v in values if counts[v] == max_count]
    for v in reversed(values):
        if v in candidates:
            return v
    return values[-1]


def merge_group(turns: list[dict]) -> dict:
    if len(turns) == 1:
        return turns[0]
    texts = [t.get("text", "").strip() for t in turns]
    merged_text = " ".join(t for t in texts if t)
    emotions = [t.get("emotion", "") for t in turns]
    strategies = [t.get("strategy", "") for t in turns if t.get("strategy")]
    merged = dict(turns[0])
    merged["text"] = merged_text
    merged["emotion"] = most_common_last(emotions)
    if strategies:
        merged["strategy"] = most_common_last(strategies)
    return merged


def load_metadata() -> dict[int, dict[str, str]]:
    data = json.loads(META_PATH.read_text(encoding="utf-8"))
    out: dict[int, dict[str, str]] = {}
    for item in data:
        did = int(item["dialogue_id"])
        out[did] = {
            "problem_type": item.get("problem_type") or "",
            "situation": item.get("situation") or "",
        }
    return out


def main() -> None:
    meta = load_metadata()

    rows: list[dict[str, str]] = []
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    # Group by Dialogue_ID
    by_dialogue: dict[int, list[dict[str, str]]] = {}
    for r in rows:
        did = int(r["Dialogue_ID"])
        by_dialogue.setdefault(did, []).append(r)

    for did in by_dialogue:
        by_dialogue[did].sort(key=lambda x: int(x["Utterance_ID"]))

    result: list[dict] = []
    for did in sorted(by_dialogue.keys()):
        raw_turns: list[dict] = []
        for r in by_dialogue[did]:
            speaker = r["Speaker"].strip()
            text = (r["Utterance"] or "").strip()
            if not text:
                continue
            sp = "user" if speaker == "Client" else "sys"
            turn: dict = {
                "text": text,
                "speaker": sp,
                "emotion": (r.get("Emotion") or "").strip(),
            }
            strat = (r.get("Strategy") or "").strip()
            if sp == "sys" and strat and strat != "undefined":
                turn["strategy"] = strat
            raw_turns.append(turn)

        # Merge consecutive same-speaker (subtitle splits)
        dialog: list[dict] = []
        i = 0
        while i < len(raw_turns):
            j = i + 1
            while j < len(raw_turns) and raw_turns[j]["speaker"] == raw_turns[i]["speaker"]:
                j += 1
            dialog.append(merge_group(raw_turns[i:j]))
            i = j

        m = meta.get(did, {"problem_type": "", "situation": ""})
        result.append(
            {
                "dialogue_id": did,
                "problem_type": m["problem_type"],
                "situation": m["situation"],
                "dialog": dialog,
            }
        )

    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    total_turns = sum(len(d["dialog"]) for d in result)
    client_turns = sum(
        1 for d in result for t in d["dialog"] if t["speaker"] == "user"
    )
    print(f"Dialogues     : {len(result)}")
    print(f"Total turns   : {total_turns}")
    print(f"Client turns  : {client_turns}")
    print(f"Output        : {OUT_PATH}")


if __name__ == "__main__":
    main()
