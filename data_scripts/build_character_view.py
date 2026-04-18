"""
build_character_view.py
────────────────────────
Merge resistance + cooperation annotations into a per-character (per-dialogue)
view, including ALL turns (client + therapist).

Output structure per character:
{
  "character_id": "esconv_0",
  "dataset": "esconv",
  "problem_type": "...",
  "situation": "...",
  "dialogue": [
    {
      "turn_pos": 0,
      "speaker": "therapist",
      "text": "...",
      "binary_label": null,
      "fine_label": null
    },
    {
      "turn_pos": 2,
      "speaker": "client",
      "text": "...",
      "binary_label": "合作",
      "fine_label": "CBS4-叙述"
    },
    ...
  ],
  "stats": {
    "total_turns": 25,
    "client_turns": 12,
    "therapist_turns": 13,
    "resistance_turns": 3,
    "cooperation_turns": 9,
    "unlabeled_client_turns": 0
  }
}

Sample-id format (ESConv / MESC-old): "{dialogue_id}_{full_dialog_position}"
AnnoMI format: "annomi_{transcript_id}_{client_turn_index}"
MESC new format: "mesc_{dialogue_id}_{client_turn_index}"

Outputs (under workspace/results/):
  views/esconv.json | views/mesc.json | views/annomi.json

Usage:
  python data_scripts/build_character_view.py --dataset esconv
  python data_scripts/build_character_view.py --dataset mesc
  python data_scripts/build_character_view.py --dataset annomi
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / "workspace/results"
DATASET = REPO / "workspace/dataset"

CONFIGS = {
    "esconv": {
        "dialogue_path": DATASET / "ESConv.json",
        "resistance_path": RESULTS / "labeled/esconv_resist.json",
        "coop_path":       RESULTS / "labeled/esconv_coop.json",
        "output_path":     RESULTS / "views/esconv.json",
        "client_speaker":  "seeker",
        "therapist_speaker": "supporter",
        "id_format": "pos",       # sample_id = "{cumulative_prefix}_{turn_pos}"
        "text_field": "content",
    },
    "mesc": {
        "dialogue_path": DATASET / "MESC_from_csv.json",
        "resistance_path": RESULTS / "labeled/mesc_resist.json",
        "coop_path":       RESULTS / "labeled/mesc_coop.json",
        "binary_path":     RESULTS / "labeled/mesc_binary.json",
        "output_path":     RESULTS / "views/mesc.json",
        "client_speaker":  "user",
        "therapist_speaker": "sys",
        "id_format": "turn_idx",  # sample_id = "mesc_{dlg_id}_{client_turn_index}"
        "text_field": "text",
    },
    "annomi": {
        "dialogue_path": REPO / "data/processed/AnnoMI-full.json",
        "resistance_path": RESULTS / "labeled/annomi_resist.json",
        "coop_path":       RESULTS / "labeled/annomi_coop.json",
        "output_path":     RESULTS / "views/annomi.json",
        "client_speaker":  "client",
        "therapist_speaker": "therapist",
        "id_format": "annomi",
        "text_field": "utterance_text",
    },
}


def load_label_index(
    resistance_path: Path,
    coop_path: Path,
    binary_path: Path | None = None,
) -> dict[str, dict]:
    """Build sample_id → {binary_label, fine_label} index.

    If resistance_path / coop_path don't exist but binary_path does,
    fall back to binary-only labels (fine_label will be None).
    """
    index: dict[str, dict] = {}
    if resistance_path.exists():
        for r in json.loads(resistance_path.read_text()):
            sid = r.get("sample_id", "")
            index[sid] = {
                "binary_label": r.get("binary_label", "阻抗"),
                "fine_label": r.get("fine_category") or r.get("fine_label") or None,
            }
    if coop_path.exists():
        for r in json.loads(coop_path.read_text()):
            sid = r.get("sample_id", "")
            index[sid] = {
                "binary_label": r.get("binary_label", "合作"),
                "fine_label": r.get("cbs_type") or None,
            }
    # Binary fallback: fills in entries that haven't been covered above
    if binary_path and binary_path.exists():
        for r in json.loads(binary_path.read_text()):
            sid = r.get("sample_id", "")
            if sid not in index:
                index[sid] = {
                    "binary_label": r.get("binary_label"),
                    "fine_label": None,
                }
    return index


# ─── Dataset-specific builders ───────────────────────────────────────────────

def _build_esconv_id_map(data: list) -> dict[tuple, str]:
    """
    Map (list_index, turn_pos) -> sample_id for ESConv.

    sample_id format: "{prefix}_{turn_pos}"
    where prefix = cumulative count of labeled seeker turns in all prior dialogues.
    A "labeled" seeker turn = any seeker turn that has at least one PRECEDING turn
    in the dialogue (pos > 0), meaning there is context available.
    Dialogues that start with the supporter contribute their first seeker turn too.
    """
    cumulative = 0
    mapping: dict[tuple, str] = {}
    for dlg_idx, item in enumerate(data):
        labeled_count = 0
        for pos, turn in enumerate(item.get("dialog", [])):
            if turn.get("speaker") == "seeker" and pos > 0:
                mapping[(dlg_idx, pos)] = f"{cumulative}_{pos}"
                labeled_count += 1
        cumulative += labeled_count
    return mapping


def build_esconv(cfg: dict, label_index: dict) -> list[dict]:
    data = json.loads(cfg["dialogue_path"].read_text())
    id_map = _build_esconv_id_map(data)
    result = []
    for dlg_id, item in enumerate(data):
        turns_out = []
        for pos, turn in enumerate(item.get("dialog", [])):
            spk = turn.get("speaker", "")
            text = turn.get(cfg["text_field"], "").strip()
            if not text:
                continue
            if spk == cfg["client_speaker"]:
                sid = id_map.get((dlg_id, pos), "")  # empty if pos==0 (no context)
                label = label_index.get(sid, {})
                turns_out.append({
                    "turn_pos": pos,
                    "speaker": "client",
                    "text": text,
                    "binary_label": label.get("binary_label"),
                    "fine_label": label.get("fine_label") or None,
                })
            else:
                strat = turn.get("annotation", {}).get("strategy", "")
                t = {
                    "turn_pos": pos,
                    "speaker": "therapist",
                    "text": text,
                    "binary_label": None,
                    "fine_label": None,
                }
                if strat:
                    t["strategy"] = strat
                turns_out.append(t)

        result.append(_wrap(f"esconv_{dlg_id}", "esconv", item, turns_out))
    return result


def build_mesc(cfg: dict, label_index: dict) -> list[dict]:
    data = json.loads(cfg["dialogue_path"].read_text())
    result = []
    for item in data:
        dlg_id = item.get("dialogue_id", 0)
        turns_out = []
        client_idx = 0
        for pos, turn in enumerate(item.get("dialog", [])):
            spk = turn.get("speaker", "")
            text = turn.get(cfg["text_field"], "").strip()
            if not text:
                continue
            if spk == cfg["client_speaker"]:
                sid = f"mesc_{dlg_id}_{client_idx}"
                label = label_index.get(sid, {})
                turns_out.append({
                    "turn_pos": pos,
                    "speaker": "client",
                    "text": text,
                    "binary_label": label.get("binary_label"),
                    "fine_label": label.get("fine_label") or None,
                    "emotion": turn.get("emotion", ""),
                })
                client_idx += 1
            else:
                t = {
                    "turn_pos": pos,
                    "speaker": "therapist",
                    "text": text,
                    "binary_label": None,
                    "fine_label": None,
                    "emotion": turn.get("emotion", ""),
                }
                if turn.get("strategy"):
                    t["strategy"] = turn["strategy"]
                turns_out.append(t)

        result.append(_wrap(f"mesc_{dlg_id}", "mesc", item, turns_out))
    return result


def build_annomi(cfg: dict, label_index: dict) -> list[dict]:
    raw = json.loads(cfg["dialogue_path"].read_text())
    transcripts = raw.get("transcripts", {})
    result = []
    for transcript_id, payload in transcripts.items():
        turns_out = []
        client_idx = 0
        for turn in payload.get("dialogue", []):
            role = turn.get("interlocutor", "")
            text = (turn.get(cfg["text_field"]) or "").strip()
            if not text:
                continue
            if role == cfg["client_speaker"]:
                sid = f"annomi_{transcript_id}_{client_idx}"
                label = label_index.get(sid, {})
                turns_out.append({
                    "turn_pos": client_idx,
                    "speaker": "client",
                    "text": text,
                    "binary_label": label.get("binary_label"),
                    "fine_label": label.get("fine_label") or None,
                    "client_talk_type": turn.get("client_talk_type", ""),
                })
                client_idx += 1
            else:
                turns_out.append({
                    "turn_pos": None,
                    "speaker": "therapist",
                    "text": text,
                    "binary_label": None,
                    "fine_label": None,
                    "main_therapist_behaviour": turn.get("main_therapist_behaviour", ""),
                })

        meta = {
            "mi_quality": payload.get("mi_quality", ""),
            "topic": payload.get("topic", ""),
        }
        result.append(_wrap(f"annomi_{transcript_id}", "annomi", meta, turns_out))
    return result


def _wrap(character_id: str, dataset: str, meta: dict, turns: list[dict]) -> dict:
    client_turns = [t for t in turns if t["speaker"] == "client"]
    therapist_turns = [t for t in turns if t["speaker"] == "therapist"]
    labeled = [t for t in client_turns if t["binary_label"] is not None]
    resistance = [t for t in labeled if t["binary_label"] == "阻抗"]
    coop = [t for t in labeled if t["binary_label"] == "合作"]

    return {
        "character_id": character_id,
        "dataset": dataset,
        "problem_type": meta.get("problem_type") or meta.get("topic") or "",
        "situation": meta.get("situation") or meta.get("mi_quality") or "",
        "dialogue": turns,
        "stats": {
            "total_turns": len(turns),
            "client_turns": len(client_turns),
            "therapist_turns": len(therapist_turns),
            "resistance_turns": len(resistance),
            "cooperation_turns": len(coop),
            "unlabeled_client_turns": len(client_turns) - len(labeled),
        },
    }


BUILDERS = {"esconv": build_esconv, "mesc": build_mesc, "annomi": build_annomi}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True, choices=list(CONFIGS.keys()))
    args = parser.parse_args()

    cfg = CONFIGS[args.dataset]
    label_index = load_label_index(
        cfg["resistance_path"],
        cfg["coop_path"],
        cfg.get("binary_path"),
    )
    print(f"Labels loaded: {len(label_index)}")

    builder = BUILDERS[args.dataset]
    result = builder(cfg, label_index)

    cfg["output_path"].write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    total_client = sum(c["stats"]["client_turns"] for c in result)
    total_res = sum(c["stats"]["resistance_turns"] for c in result)
    total_coop = sum(c["stats"]["cooperation_turns"] for c in result)
    unlabeled = sum(c["stats"]["unlabeled_client_turns"] for c in result)
    print(f"Characters   : {len(result)}")
    print(f"Client turns : {total_client}  (阻抗 {total_res} / 合作 {total_coop} / 无标签 {unlabeled})")
    print(f"Output       : {cfg['output_path']}")


if __name__ == "__main__":
    main()
