"""
prepare_training_splits.py
--------------------------
Build training/validation/test splits for SFT data preparation.

Policy implemented from supervisor guidance:
1) Test set comes from RECAP and is fully retained.
2) Non-RECAP datasets are supplementary and used for train/val.
3) Train/val should be label-balanced as much as possible.
4) After split, prepare translation queues:
   - First pass: culture-specificity judgment required (LLM/manual later).
   - Second pass: only non-culture-specific items should be translated EN->ZH.
5) Build a review queue for non-resistance items in RECAP test set.

Usage:
  python data_scripts/prepare_training_splits.py
  python data_scripts/prepare_training_splits.py --train-ratio 0.9 --per-label-cap 260
"""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / "workspace" / "results"
OUT_DIR = RESULTS / "training_splits"


def _load_json(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def _dump_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _label_code(item: dict[str, Any]) -> str:
    raw = item.get("fine_category") or item.get("fine_label") or "UNKNOWN"
    if "-" in raw:
        return raw.split("-", 1)[0].strip()
    return raw.strip() or "UNKNOWN"


def load_cot_samples() -> list[dict[str, Any]]:
    sources = {
        "esconv": RESULTS / "cot" / "esconv.json",
        "mesc": RESULTS / "cot" / "mesc.json",
        "annomi": RESULTS / "cot" / "annomi.json",
    }
    all_rows: list[dict[str, Any]] = []
    for source, path in sources.items():
        rows = _load_json(path)
        for r in rows:
            internal = (r.get("internal") or "").strip()
            # Remove empty COT samples from training pool.
            if not internal:
                continue
            item = {
                "source": source,
                "sample_id": f"{source}:{r.get('character_id')}:{r.get('turn_pos')}",
                "character_id": r.get("character_id"),
                "turn_pos": r.get("turn_pos"),
                "binary_label": r.get("binary_label"),
                "fine_label": r.get("fine_label"),
                "fine_category": r.get("fine_category"),
                "label_code": _label_code(r),
                "context": r.get("context", []),
                "therapist_turn": r.get("therapist_turn", ""),
                "client_response": r.get("client_response", ""),
                "internal": internal,
                "profile_used": r.get("profile_used"),
            }
            all_rows.append(item)
    # Dedup by sample_id.
    uniq = {}
    for x in all_rows:
        uniq[x["sample_id"]] = x
    return list(uniq.values())


def build_balanced_pool(
    rows: list[dict[str, Any]],
    per_label_cap: int,
    seed: int,
) -> list[dict[str, Any]]:
    by_label: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        by_label[r["label_code"]].append(r)

    rnd = random.Random(seed)
    selected: list[dict[str, Any]] = []
    for label, group in by_label.items():
        rnd.shuffle(group)
        k = min(len(group), per_label_cap)
        selected.extend(group[:k])
    rnd.shuffle(selected)
    return selected


def split_train_val(
    rows: list[dict[str, Any]],
    train_ratio: float,
    seed: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_label: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        by_label[r["label_code"]].append(r)

    rnd = random.Random(seed)
    train: list[dict[str, Any]] = []
    val: list[dict[str, Any]] = []
    for _, group in by_label.items():
        rnd.shuffle(group)
        cut = int(len(group) * train_ratio)
        cut = min(max(cut, 1), len(group))
        train.extend(group[:cut])
        val.extend(group[cut:])
    rnd.shuffle(train)
    rnd.shuffle(val)
    return train, val


def _turns_before(dialogue: list[dict[str, Any]], turn_pos: int) -> list[dict[str, Any]]:
    return [
        {"speaker": t.get("speaker"), "text": t.get("text")}
        for t in dialogue
        if t.get("turn_pos", -1) < turn_pos
    ]


def _last_therapist_utterance(dialogue: list[dict[str, Any]], turn_pos: int) -> str:
    for t in reversed(dialogue):
        pos = t.get("turn_pos", -1)
        if pos >= turn_pos:
            continue
        if t.get("speaker") == "therapist":
            return t.get("text", "")
    return ""


def build_recap_test_set() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Returns:
      - turn-level eval units (for scoring/filtering)
      - full dialogues (for human review and context-preserving evaluation)
    """
    recaps = _load_json(RESULTS / "recap" / "dialogues.json")
    test_rows: list[dict[str, Any]] = []
    full_dialogues: list[dict[str, Any]] = []

    for dlg in recaps:
        dialogue = dlg.get("dialogue", [])
        char_id = dlg.get("character_id")
        full_dialogues.append(
            {
                "source": "recap",
                "character_id": char_id,
                "dialogue_id": dlg.get("dialogue_id"),
                "problem_type": dlg.get("problem_type"),
                "situation": dlg.get("situation"),
                "dialogue": dialogue,
                "stats": dlg.get("stats", {}),
            }
        )
        for turn in dialogue:
            if turn.get("speaker") != "client":
                continue
            turn_pos = turn.get("turn_pos", -1)
            row = {
                "source": "recap",
                "sample_id": f"recap:{char_id}:{turn_pos}",
                "character_id": char_id,
                "turn_pos": turn_pos,
                "binary_label": turn.get("binary_label"),
                "fine_label": turn.get("fine_label"),
                "fine_category": turn.get("fine_category"),
                "label_code": _label_code(turn),
                "context": _turns_before(dialogue, turn_pos),
                "therapist_turn": _last_therapist_utterance(dialogue, turn_pos),
                "client_response": turn.get("text", ""),
                # RECAP currently has no COT internal in this file.
                "internal": None,
                "profile_used": None,
            }
            test_rows.append(row)
    return test_rows, full_dialogues


def split_recap_targets_and_context_only(
    test_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Split RECAP test rows into:
    - labeled targets (can be scored)
    - unlabeled rows (context-only, not training/eval targets)
    """
    labeled = []
    context_only = []
    for r in test_rows:
        if r.get("binary_label") in ("阻抗", "合作"):
            labeled.append(r)
        else:
            context_only.append(r)
    return labeled, context_only


def build_non_resistance_review_queue(test_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    queue = []
    for r in test_rows:
        if r.get("binary_label") != "阻抗":
            queue.append(
                {
                    "sample_id": r["sample_id"],
                    "character_id": r.get("character_id"),
                    "turn_pos": r.get("turn_pos"),
                    "binary_label": r.get("binary_label"),
                    "fine_label": r.get("fine_label"),
                    "text": r.get("client_response"),
                    "dialogue_ref": {
                        "source": "recap",
                        "character_id": r.get("character_id"),
                    },
                    "review_status": "pending",
                    "reviewer": None,
                    "review_note": "",
                }
            )
    return queue


def build_translation_judge_queue(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    # English supplementary data only (cot sources).
    queue = []
    for r in rows:
        queue.append(
            {
                "sample_id": r["sample_id"],
                "source": r["source"],
                "label_code": r["label_code"],
                "binary_label": r.get("binary_label"),
                "culture_specificity_status": "pending",  # pending/yes/no
                "culture_specificity_reason": "",
                "translation_status": "pending",  # pending/skipped/translated
                "text_bundle": {
                    "context": r.get("context", []),
                    "therapist_turn": r.get("therapist_turn", ""),
                    "client_response": r.get("client_response", ""),
                    "internal": r.get("internal", ""),
                },
            }
        )
    return queue


def build_translation_manual_qc_pool(
    translated_rows: list[dict[str, Any]],
    sample_size: int,
    seed: int,
) -> list[dict[str, Any]]:
    rnd = random.Random(seed)
    rows = translated_rows[:]
    rnd.shuffle(rows)
    picked = rows[: min(sample_size, len(rows))]
    out = []
    for r in picked:
        out.append(
            {
                "sample_id": r.get("sample_id"),
                "label_code": r.get("label_code"),
                "binary_label": r.get("binary_label"),
                "qc_status": "pending",
                "qc_note": "",
            }
        )
    return out


def summarize(name: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    c_bin = Counter(str(r.get("binary_label")) for r in rows)
    c_lbl = Counter(str(r.get("label_code")) for r in rows)
    return {
        "name": name,
        "size": len(rows),
        "binary_dist": dict(c_bin),
        "label_code_top20": dict(c_lbl.most_common(20)),
    }


def build_consistency_report(out_dir: Path) -> dict[str, Any]:
    full_dialogues = _load_json(out_dir / "test_recap_full_dialogues_retained.json")
    turn_level = _load_json(out_dir / "test_recap_all_retained_turn_level.json")
    labeled_targets = _load_json(out_dir / "test_recap_labeled_targets.json")
    null_only = _load_json(out_dir / "test_recap_context_only_null_labels.json")
    review_queue = _load_json(out_dir / "review_queue_recap_non_resistance.json")

    index = {
        (x.get("sample_id"), x.get("character_id"), x.get("turn_pos"))
        for x in turn_level
    }
    missing_refs = []
    for r in review_queue:
        key = (r.get("sample_id"), r.get("character_id"), r.get("turn_pos"))
        if key not in index:
            missing_refs.append(r.get("sample_id"))

    expected_turn = len(labeled_targets) + len(null_only)
    turn_partition_ok = expected_turn == len(turn_level)

    dialogue_ids = {d.get("character_id") for d in full_dialogues}
    turn_dialogue_ids = {x.get("character_id") for x in turn_level}
    dialogue_cover_ok = turn_dialogue_ids.issubset(dialogue_ids)

    return {
        "checks": {
            "turn_partition_ok": turn_partition_ok,
            "turn_partition": {
                "turn_level": len(turn_level),
                "labeled_targets_plus_null_only": expected_turn,
            },
            "review_queue_reference_ok": len(missing_refs) == 0,
            "review_queue_missing_reference_count": len(missing_refs),
            "dialogue_cover_ok": dialogue_cover_ok,
            "full_dialogues_count": len(full_dialogues),
            "turn_level_unique_character_ids": len(turn_dialogue_ids),
        },
        "missing_review_refs_preview": missing_refs[:20],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-ratio", type=float, default=0.9)
    parser.add_argument(
        "--per-label-cap",
        type=int,
        default=260,
        help="Max samples per label from supplementary datasets.",
    )
    parser.add_argument("--manual-qc-size", type=int, default=300)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    cot_rows = load_cot_samples()
    balanced_pool = build_balanced_pool(cot_rows, args.per_label_cap, args.seed)
    train_rows, val_rows = split_train_val(balanced_pool, args.train_ratio, args.seed)
    recap_test_rows, recap_full_dialogues = build_recap_test_set()
    recap_labeled_targets, recap_context_only = split_recap_targets_and_context_only(recap_test_rows)

    non_resistance_review = build_non_resistance_review_queue(recap_test_rows)
    translation_judge_queue = build_translation_judge_queue(train_rows + val_rows)
    # Placeholder: manual QC pool built from translated rows in the future.
    translation_manual_qc_pool = build_translation_manual_qc_pool(
        translated_rows=[],
        sample_size=args.manual_qc_size,
        seed=args.seed,
    )

    out = OUT_DIR
    _dump_json(out / "train_supplementary_balanced.json", train_rows)
    _dump_json(out / "val_supplementary_balanced.json", val_rows)
    _dump_json(out / "test_recap_all_retained_turn_level.json", recap_test_rows)
    _dump_json(out / "test_recap_full_dialogues_retained.json", recap_full_dialogues)
    _dump_json(out / "test_recap_labeled_targets.json", recap_labeled_targets)
    _dump_json(out / "test_recap_context_only_null_labels.json", recap_context_only)
    _dump_json(out / "review_queue_recap_non_resistance.json", non_resistance_review)
    _dump_json(out / "translation_culture_judge_queue.json", translation_judge_queue)
    _dump_json(out / "translation_manual_qc_pool_template.json", translation_manual_qc_pool)

    report = {
        "policy": {
            "test_set": "all_recap_client_turns_retained",
            "supplementary_datasets": ["esconv", "mesc", "annomi"],
            "balancing": {
                "method": "per_label_cap_downsample",
                "per_label_cap": args.per_label_cap,
            },
            "translation_pipeline": [
                "culture_specificity_judge",
                "drop_culture_specific",
                "en_to_zh_translation",
                "manual_qc_sample_check",
            ],
        },
        "splits": [
            summarize("train_supplementary_balanced", train_rows),
            summarize("val_supplementary_balanced", val_rows),
            summarize("test_recap_all_retained_turn_level", recap_test_rows),
            summarize("test_recap_labeled_targets", recap_labeled_targets),
            summarize("test_recap_context_only_null_labels", recap_context_only),
        ],
        "queues": {
            "recap_non_resistance_review_count": len(non_resistance_review),
            "translation_culture_judge_count": len(translation_judge_queue),
            "recap_full_dialogues_count": len(recap_full_dialogues),
        },
        "notes": [
            "RECAP full dialogues are retained in test_recap_full_dialogues_retained.json.",
            "Turn-level files are derived views for scoring/filtering only.",
            "Only test_recap_labeled_targets should be used as scoring/evaluation targets.",
            "test_recap_context_only_null_labels should only be used as context carriers.",
            "RECAP non-resistance queue includes binary_label != 阻抗 (including null).",
            "translation_manual_qc_pool_template is intentionally empty before translation outputs exist.",
        ],
    }
    _dump_json(out / "split_report.json", report)
    consistency_report = build_consistency_report(out)
    _dump_json(out / "consistency_report.json", consistency_report)

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("\n=== consistency_report ===")
    print(json.dumps(consistency_report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

