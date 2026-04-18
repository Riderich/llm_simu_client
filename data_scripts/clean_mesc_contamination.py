"""
clean_mesc_contamination.py
───────────────────────────
Remove visual-model contamination from MESC_merged.json.

Problem: Every dialog turn text contains appended visual descriptions like:
    "I told you. The speaker is a young woman... She appears to be sad..."
These were injected by a vision model during preprocessing and must be stripped.

Fix: Truncate each turn's text at the first occurrence of "The speaker" or
"the speaker", then strip trailing whitespace and punctuation fragments.

Output: workspace/dataset/MESC_merged_clean.json
"""

import json
import re
from pathlib import Path

INPUT  = Path("workspace/dataset/MESC_merged.json")
OUTPUT = Path("workspace/dataset/MESC_merged_clean.json")

CONTAM_PATTERN = re.compile(r'\s*[Tt]he speaker\b.*', re.DOTALL)


def clean_text(text: str) -> str:
    cleaned = CONTAM_PATTERN.sub("", text)
    # Strip trailing punctuation fragments like trailing comma, space
    cleaned = cleaned.rstrip(" ,;")
    return cleaned.strip()


def main():
    data = json.loads(INPUT.read_text(encoding="utf-8"))

    total_turns = 0
    cleaned_turns = 0

    for dialogue in data:
        for turn in dialogue.get("dialog", []):
            original = turn.get("text", "")
            total_turns += 1
            if re.search(r'[Tt]he speaker', original):
                turn["text"] = clean_text(original)
                cleaned_turns += 1

    OUTPUT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Total turns  : {total_turns}")
    print(f"Cleaned turns: {cleaned_turns} ({cleaned_turns/total_turns*100:.1f}%)")
    print(f"Output       : {OUTPUT}")

    # Sanity check: verify no contamination remains
    remaining = sum(
        1
        for d in data
        for t in d.get("dialog", [])
        if re.search(r'[Tt]he speaker', t.get("text", ""))
    )
    print(f"Remaining contaminated turns: {remaining}")


if __name__ == "__main__":
    main()
