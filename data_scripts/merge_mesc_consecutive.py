"""
merge_mesc_consecutive.py
─────────────────────────
Merge consecutive same-speaker turns in MESC_merged_clean.json.

Background: MESC transcripts are derived from TV show subtitles, where a single
continuous utterance is often split into multiple short fragments by timestamp.
Example:
    [user] "You know what?"
    [user] "It's disappointing."
    [user] "I thought I'd feel better"
    [user] "relieved."
→ merged: "You know what? It's disappointing. I thought I'd feel better relieved."

Merge rules:
- Join texts with a space (not punctuation — original fragments may already end
  with punctuation or be mid-sentence).
- emotion: most frequent across the group; tie-break by last turn's emotion.
- strategy: most frequent (therapist turns only); tie-break by last.
- Other fields (speaker) taken from first turn.

ESConv is NOT processed here — its consecutive turns are intentional multi-part
responses with distinct strategy annotations.
AnnoMI has no consecutive turns.

Output: workspace/dataset/MESC_merged_clean.json  (overwrite in-place)
"""

import json
from collections import Counter
from pathlib import Path

INPUT = Path("workspace/dataset/MESC_merged_clean.json")


def most_common_last(values: list[str]) -> str:
    """Most frequent value; tie-break by last occurrence."""
    counts = Counter(values)
    max_count = max(counts.values())
    candidates = [v for v in values if counts[v] == max_count]
    # among candidates, return the one that appears last
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

    merged: dict = dict(turns[0])  # copy first turn as base
    merged["text"] = merged_text
    merged["emotion"] = most_common_last(emotions)
    if strategies:
        merged["strategy"] = most_common_last(strategies)

    return merged


def main():
    data = json.loads(INPUT.read_text(encoding="utf-8"))

    total_before = sum(len(d["dialog"]) for d in data)
    merged_groups = 0
    merged_turns_removed = 0

    for dialogue in data:
        dialog = dialogue["dialog"]
        new_dialog = []
        i = 0
        while i < len(dialog):
            j = i + 1
            while (
                j < len(dialog)
                and dialog[j]["speaker"] == dialog[i]["speaker"]
            ):
                j += 1
            group = dialog[i:j]
            if len(group) > 1:
                merged_groups += 1
                merged_turns_removed += len(group) - 1
            new_dialog.append(merge_group(group))
            i = j
        dialogue["dialog"] = new_dialog

    total_after = sum(len(d["dialog"]) for d in data)

    INPUT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Turns before merge : {total_before}")
    print(f"Turns after merge  : {total_after}")
    print(f"Turns removed      : {merged_turns_removed}")
    print(f"Groups merged      : {merged_groups}")
    print(f"Output             : {INPUT}  (updated in-place)")

    # Sanity check: verify no consecutive same-speaker turns remain
    remaining = sum(
        1
        for d in data
        for i in range(len(d["dialog"]) - 1)
        if d["dialog"][i]["speaker"] == d["dialog"][i + 1]["speaker"]
    )
    print(f"Remaining consecutive groups: {remaining}")


if __name__ == "__main__":
    main()
