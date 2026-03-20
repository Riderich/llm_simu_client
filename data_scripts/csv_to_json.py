#!/usr/bin/env python3
"""
Convert AnnoMI-full.csv to hierarchical JSON format.
Generates two versions:
1. AnnoMI-full.json: Full version with all fields
2. AnnoMI-simple.json: Simplified version with only interlocutor and utterance_text in dialogue
"""

import csv
import json
from collections import defaultdict
from pathlib import Path


# File paths
INPUT_CSV = r"E:\OneDrive - The Chinese University of Hong Kong\Research\llm_simu_client\scr data\AnnoMI\AnnoMI-full.csv"
OUTPUT_FULL_JSON = r"E:\OneDrive - The Chinese University of Hong Kong\Research\llm_simu_client\scr data\AnnoMI-full.json"
OUTPUT_SIMPLE_JSON = r"E:\OneDrive - The Chinese University of Hong Kong\Research\llm_simu_client\scr data\AnnoMI-simple.json"

# Metadata fields (conversation-level data)
METADATA_FIELDS = ["mi_quality", "video_title", "video_url", "topic"]

# Fields to exclude from dialogue (transcript_id and metadata)
EXCLUDE_FIELDS = ["transcript_id"] + METADATA_FIELDS


def read_csv(csv_path):
    """Read CSV and aggregate data by transcript_id."""
    transcripts = defaultdict(lambda: {"utterances": []})

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            transcript_id = row["transcript_id"]

            # Store metadata from first utterance of each transcript
            if not transcripts[transcript_id].get("metadata"):
                transcripts[transcript_id]["metadata"] = {
                    field: row[field] for field in METADATA_FIELDS
                }

            # Prepare utterance data
            utterance = {
                key: value for key, value in row.items()
                if key not in EXCLUDE_FIELDS
            }
            utterance["utterance_id"] = int(utterance["utterance_id"])
            utterance["annotator_id"] = int(utterance["annotator_id"])

            transcripts[transcript_id]["utterances"].append(utterance)

    return transcripts


def build_full_structure(transcripts):
    """Build full JSON structure with all fields."""
    result = {"transcripts": {}}

    for transcript_id, data in sorted(transcripts.items()):
        # Sort utterances by utterance_id
        utterances = sorted(data["utterances"], key=lambda x: x["utterance_id"])

        result["transcripts"][transcript_id] = {
            "metadata": data["metadata"],
            "dialogue": utterances
        }

    return result


def build_simple_structure(transcripts):
    """Build simplified JSON structure with only interlocutor and utterance_text."""
    result = {"transcripts": {}}

    for transcript_id, data in sorted(transcripts.items()):
        # Sort utterances by utterance_id and keep only interlocutor and utterance_text
        sorted_utterances = sorted(data["utterances"], key=lambda x: x["utterance_id"])

        dialogue = [
            {
                "interlocutor": u["interlocutor"],
                "utterance_text": u["utterance_text"]
            }
            for u in sorted_utterances
        ]

        result["transcripts"][transcript_id] = {
            "metadata": data["metadata"],
            "dialogue": dialogue
        }

    return result


def write_json(data, output_path):
    """Write data to JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def verify_transcripts(transcripts, full_data, simple_data):
    """Verify the conversion results."""
    transcript_count = len(transcripts)
    total_utterances = sum(len(data["utterances"]) for data in transcripts.values())

    print(f"\n=== Verification ===")
    print(f"Number of transcripts: {transcript_count}")
    print(f"Total utterances: {total_utterances}")

    # Verify dialogue count in full version
    full_dialogue_count = sum(
        len(transcript["dialogue"])
        for transcript in full_data["transcripts"].values()
    )
    print(f"Full version dialogue count: {full_dialogue_count}")

    # Verify dialogue count in simple version
    simple_dialogue_count = sum(
        len(transcript["dialogue"])
        for transcript in simple_data["transcripts"].values()
    )
    print(f"Simple version dialogue count: {simple_dialogue_count}")

    # Verify simple version only has 2 fields per dialogue entry
    sample_transcript_id = list(simple_data["transcripts"].keys())[0]
    sample_dialogue = simple_data["transcripts"][sample_transcript_id]["dialogue"]
    print(f"\nSample simple dialogue entry fields: {list(sample_dialogue[0].keys())}")

    return transcript_count == 133 and total_utterances == 13551


def main():
    print("Converting AnnoMI-full.csv to JSON...")

    # Read and aggregate CSV data
    print(f"Reading {INPUT_CSV}...")
    transcripts = read_csv(INPUT_CSV)

    # Build full version
    print("Building full JSON structure...")
    full_data = build_full_structure(transcripts)

    # Build simplified version
    print("Building simple JSON structure...")
    simple_data = build_simple_structure(transcripts)

    # Write full version
    print(f"Writing full version to {OUTPUT_FULL_JSON}...")
    write_json(full_data, OUTPUT_FULL_JSON)

    # Write simplified version
    print(f"Writing simple version to {OUTPUT_SIMPLE_JSON}...")
    write_json(simple_data, OUTPUT_SIMPLE_JSON)

    # Verify results
    if verify_transcripts(transcripts, full_data, simple_data):
        print("\n✓ Conversion completed successfully!")
    else:
        print("\n✗ Verification failed!")


if __name__ == "__main__":
    main()
