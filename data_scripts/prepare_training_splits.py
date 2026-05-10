"""
prepare_training_splits.py
--------------------------
Build training/validation/test splits for SFT data preparation.

Policy implemented from supervisor guidance:
1) **RECAP test holdout (default ~2000 监督轮)**：按 **完整对话** 抽样，直到「带 阻抗/合作 的来访轮」累计 **≥ --recap-test-labeled-min**
   （当前数据每对话至多 1 条监督，故约等于抽满该条数的对话段）。**整段对话**进 test，含其内无标 context 轮。
2) **其余 RECAP** 以 **整段对话** 为单位打乱后按 **8:1** 拆入 train/val（`train_recap_*` / `val_recap_*`），**绝不**把不同对话的轮次混洗成一条平铺列表。
   **COT** 仍为 `train_supplementary_balanced` / `val_supplementary_balanced`；与 RECAP 的「混合」在 **batch/采样器** 层完成，不由本脚本拆对话。
3) **Global 8:1:1 可行性**仍按 **T = |RECAP_test 内监督条数| + |balanced COT|** 计算。
4) Supplementary pool = **clinical COT only** (`cot/*.json`: profile + fine labels + real `<internal>` COT).
   **ExtES** (`results/extes/`) is **not** merged here: no coop fine taxonomy, no profile, no COT—not same asset class as cot/*.json.
5) After split, prepare translation / review queues from that pool.
   - First pass: culture-specificity judgment required (LLM/manual later).
   - Second pass: only non-culture-specific items should be translated EN->ZH.
6) Build a review queue for non-resistance items in **RECAP test holdout** turn set.

Usage:
  python data_scripts/prepare_training_splits.py
  python data_scripts/prepare_training_splits.py --recap-test-labeled-min 2000 --seed 42
  python data_scripts/prepare_training_splits.py --recap-cot-path workspace/results/recap/recap_labeled_cot.json --strict-recap-cot

RECAP COT 侧车由 ``data_scripts/generate_recap_labeled_cot.py`` 生成后再合并。
"""

from __future__ import annotations

import argparse
import json
import random
import sys
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
    """Stratify by ``label_code`` (跨 esconv/mesc/annomi), shuffle, then cap per stratum.

    ``per_label_cap <= 0`` means no truncation (keep all rows).
    """
    by_label: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        by_label[r["label_code"]].append(r)

    rnd = random.Random(seed)
    selected: list[dict[str, Any]] = []
    for _label, group in by_label.items():
        rnd.shuffle(group)
        if per_label_cap <= 0:
            k = len(group)
        else:
            k = min(len(group), per_label_cap)
        selected.extend(group[:k])
    rnd.shuffle(selected)
    return selected


def split_balanced_cot_with_recap_in_test_union(
    recap_labeled_targets: list[dict[str, Any]],
    cot_balanced: list[dict[str, Any]],
    train_frac: float,
    val_frac: float,
    test_frac: float,
    seed: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """
    Global 8:1:1 on T = |recap_labeled_targets| + |cot|.

    `recap_labeled_targets` must be only supervision/eval units (e.g. 阻抗/合作); context-only turns are excluded from T.

    Returns (train_cot, val_cot, test_cot, feasibility_meta).
    """
    if abs(train_frac + val_frac + test_frac - 1.0) > 1e-5:
        raise ValueError("train_frac + val_frac + test_frac must sum to 1.0")

    R = len(recap_labeled_targets)
    S = len(cot_balanced)
    T = R + S
    # Integer targets summing to T (same as (T*8)//10 style)
    w_tr, w_va, w_te = train_frac, val_frac, test_frac
    s = w_tr + w_va + w_te
    n_train = int((T * w_tr) / s)
    n_val = int((T * w_va) / s)
    n_test_total = T - n_train - n_val
    rnd = random.Random(seed)
    cot_pool = cot_balanced[:]
    rnd.shuffle(cot_pool)

    feasible = n_test_total >= R
    meta: dict[str, Any] = {
        "union_T": T,
        "R_recap_labeled_targets_in_union": R,
        "S_cot_balanced": S,
        "target_train": n_train,
        "target_val": n_val,
        "target_test_slot_including_labeled_recap": n_test_total,
        "feasible_exact_global_split_with_all_labeled_recap_in_test": feasible,
    }

    if not feasible:
        # All COT → train+val only, ratio 8:1 within COT mass (no held-out COT test fold).
        cot_test: list[dict[str, Any]] = []
        L = len(cot_pool)
        nt2 = (L * 8) // 9
        nv2 = L - nt2
        train = cot_pool[:nt2]
        val = cot_pool[nt2 : nt2 + nv2]
        meta["mode"] = "fallback_recap_exceeds_target_test_mass"
        meta["cot_test_count"] = 0
        meta["actual_global_train"] = len(train)
        meta["actual_global_val"] = len(val)
        meta["actual_global_test"] = R
        meta["actual_train_frac"] = len(train) / T if T else 0.0
        meta["actual_val_frac"] = len(val) / T if T else 0.0
        meta["actual_test_frac"] = R / T if T else 0.0
        meta["note_zh"] = (
            "「RECAP test 内监督」条数已超过并集 T 下总体的 test 槽位（按 train/val/test 比例），"
            "在「test 中 RECAP 监督必须全部落在 test 槽」约束下无法同时满足全局 8:1:1；"
            "已将全部 COT 按 8:1 拆入 train/val，且不划分 COT test 折。"
            "train/val 中的 RECAP 余量以整段对话写入 train_recap_* / val_recap_*；COT 仍单独列出，训练时再做 batch 级混合。"
        )
        return train, val, cot_test, meta

    k_cot_test = n_test_total - R
    cot_test = cot_pool[:k_cot_test]
    cot_rem = cot_pool[k_cot_test:]
    assert len(cot_rem) == n_train + n_val
    rnd2 = random.Random(seed + 911)
    rnd2.shuffle(cot_rem)
    train = cot_rem[:n_train]
    val = cot_rem[n_train : n_train + n_val]
    meta["mode"] = "global_union_8_1_1"
    meta["cot_test_count"] = k_cot_test
    meta["actual_global_train"] = len(train)
    meta["actual_global_val"] = len(val)
    meta["actual_global_test"] = R + len(cot_test)
    meta["actual_train_frac"] = len(train) / T
    meta["actual_val_frac"] = len(val) / T
    meta["actual_test_frac"] = (R + len(cot_test)) / T
    return train, val, cot_test, meta


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


def load_recap_dialogues() -> list[dict[str, Any]]:
    return _load_json(RESULTS / "recap" / "dialogues.json")


PROFILE_USED_KEYS = (
    "background",
    "self_view_of_problem",
    "resistance_drivers",
    "ambivalence",
    "values_and_stakes",
    "key_facts",
)


def recap_profile_used_blob(record: dict[str, Any]) -> dict[str, Any]:
    """Subset aligned with clinical COT ``profile_used`` (drop raw_response / metadata)."""
    return {k: record[k] for k in PROFILE_USED_KEYS if k in record}


def load_recap_profiles(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    data = _load_json(path)
    if not isinstance(data, list):
        return {}
    out: dict[str, dict[str, Any]] = {}
    for item in data:
        sid = item.get("sample_id")
        if sid is not None:
            out[str(sid)] = recap_profile_used_blob(item)
    return out


def load_recap_cot_map(path: Path) -> dict[str, dict[str, Any]]:
    """Load COT sidecar: either a JSON object keyed by sample_id, or a list of rows with sample_id."""
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        return {str(k): v for k, v in raw.items() if isinstance(v, dict)}
    if isinstance(raw, list):
        out: dict[str, dict[str, Any]] = {}
        for item in raw:
            if not isinstance(item, dict):
                continue
            sid = item.get("sample_id")
            if sid:
                out[str(sid)] = item
        return out
    return {}


def dialogue_supervision_label(dlg: dict[str, Any]) -> str | None:
    """First client turn with 阻抗/合作; RECAP schema typically has exactly one."""
    for turn in dlg.get("dialogue", []):
        if turn.get("speaker") != "client":
            continue
        bl = turn.get("binary_label")
        if bl in ("阻抗", "合作"):
            return str(bl)
    return None


def partition_recap_dialogues_for_test(
    dialogues: list[dict[str, Any]],
    min_labeled: int,
    seed: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """
    Whole dialogues into test until cumulative labeled client turns (阻抗/合作) >= min_labeled.
    Stratify pick: round-robin from shuffled 阻抗-dialogues vs 合作-dialogues.
    Dialogues with no supervision label go to remainder only.
    """
    imp: list[dict[str, Any]] = []
    coop: list[dict[str, Any]] = []
    no_label: list[dict[str, Any]] = []
    for dlg in dialogues:
        bl = dialogue_supervision_label(dlg)
        if bl == "阻抗":
            imp.append(dlg)
        elif bl == "合作":
            coop.append(dlg)
        else:
            no_label.append(dlg)

    rnd = random.Random(seed)
    rnd.shuffle(imp)
    rnd.shuffle(coop)

    test: list[dict[str, Any]] = []
    i = j = 0
    labeled = 0
    while labeled < min_labeled:
        took = False
        if i < len(imp):
            test.append(imp[i])
            i += 1
            labeled += 1
            took = True
        if labeled >= min_labeled:
            break
        if j < len(coop):
            test.append(coop[j])
            j += 1
            labeled += 1
            took = True
        if not took:
            break

    test_ids = {d.get("character_id") for d in test}
    remainder: list[dict[str, Any]] = []
    for dlg in dialogues:
        cid = dlg.get("character_id")
        if cid in test_ids:
            continue
        remainder.append(dlg)
    remainder.extend(no_label)
    rnd.shuffle(remainder)

    meta = {
        "recap_test_labeled_min_requested": min_labeled,
        "recap_test_dialogues": len(test),
        "recap_test_labeled_turns_in_test": labeled,
        "recap_remainder_dialogues": len(remainder),
        "recap_dialogues_without_supervision_label": len(no_label),
        "recap_test_binary_dist": dict(Counter(dialogue_supervision_label(d) for d in test if dialogue_supervision_label(d))),
    }
    return test, remainder, meta


def build_turn_rows_from_dialogues(
    dialogues: list[dict[str, Any]],
    *,
    profile_by_char: dict[str, dict[str, Any]] | None = None,
    recap_cot_by_sample: dict[str, dict[str, Any]] | None = None,
    count_cot_gaps: bool = True,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    profile_by_char = profile_by_char or {}
    recap_cot_by_sample = recap_cot_by_sample or {}
    missing_chars: set[str] = set()
    stats: dict[str, Any] = {
        "recap_profile_missing_turn_rows": 0,
        "recap_cot_missing_labeled": 0,
        "recap_cot_filled_labeled": 0,
    }
    test_rows: list[dict[str, Any]] = []
    for dlg in dialogues:
        dialogue = dlg.get("dialogue", [])
        char_id = dlg.get("character_id")
        char_key = str(char_id) if char_id is not None else ""
        profile_used = profile_by_char.get(char_key) if char_key else None
        for turn in dialogue:
            if turn.get("speaker") != "client":
                continue
            turn_pos = turn.get("turn_pos", -1)
            sample_id = f"recap:{char_id}:{turn_pos}"
            if char_key and profile_used is None:
                stats["recap_profile_missing_turn_rows"] += 1
                missing_chars.add(char_key)

            cot_hit = recap_cot_by_sample.get(sample_id) or {}
            internal_val = cot_hit.get("internal")
            internal = (internal_val or "").strip() if isinstance(internal_val, str) else None
            if internal == "":
                internal = None
            raw_cot = cot_hit.get("raw_cot")
            cot_prompt_key = cot_hit.get("cot_prompt_key")

            bl = turn.get("binary_label")
            if count_cot_gaps and bl in ("阻抗", "合作"):
                if internal:
                    stats["recap_cot_filled_labeled"] += 1
                else:
                    stats["recap_cot_missing_labeled"] += 1

            row = {
                "source": "recap",
                "sample_id": sample_id,
                "character_id": char_id,
                "turn_pos": turn_pos,
                "binary_label": turn.get("binary_label"),
                "fine_label": turn.get("fine_label"),
                "fine_category": turn.get("fine_category"),
                "label_code": _label_code(turn),
                "context": _turns_before(dialogue, turn_pos),
                "therapist_turn": _last_therapist_utterance(dialogue, turn_pos),
                "client_response": turn.get("text", ""),
                "internal": internal,
                "raw_cot": raw_cot if internal else None,
                "cot_prompt_key": cot_prompt_key if internal else None,
                "profile_used": profile_used,
            }
            test_rows.append(row)
    stats["recap_profile_missing_character_ids"] = sorted(missing_chars)
    return test_rows, stats


def build_full_dialogues_from_dialogues(
    dialogues: list[dict[str, Any]],
    *,
    profile_by_char: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    profile_by_char = profile_by_char or {}
    out: list[dict[str, Any]] = []
    for dlg in dialogues:
        cid = dlg.get("character_id")
        ck = str(cid) if cid is not None else ""
        item: dict[str, Any] = {
            "source": "recap",
            "character_id": cid,
            "dialogue_id": dlg.get("dialogue_id"),
            "problem_type": dlg.get("problem_type"),
            "situation": dlg.get("situation"),
            "dialogue": dlg.get("dialogue", []),
            "stats": dlg.get("stats", {}),
        }
        if ck:
            item["profile_used"] = profile_by_char.get(ck)
        else:
            item["profile_used"] = None
        out.append(item)
    return out


def build_recap_test_set(
    dialogues: list[dict[str, Any]] | None = None,
    *,
    profile_by_char: dict[str, dict[str, Any]] | None = None,
    recap_cot_by_sample: dict[str, dict[str, Any]] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """All RECAP dialogues → turn rows + full dialogue list (legacy helper)."""
    if dialogues is None:
        dialogues = load_recap_dialogues()
    rows, _stats = build_turn_rows_from_dialogues(
        dialogues,
        profile_by_char=profile_by_char,
        recap_cot_by_sample=recap_cot_by_sample,
        count_cot_gaps=False,
    )
    return rows, build_full_dialogues_from_dialogues(dialogues, profile_by_char=profile_by_char)


def merge_turn_build_stats(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    chars = set(a.get("recap_profile_missing_character_ids") or []) | set(
        b.get("recap_profile_missing_character_ids") or []
    )
    return {
        "recap_profile_missing_turn_rows": int(a.get("recap_profile_missing_turn_rows", 0))
        + int(b.get("recap_profile_missing_turn_rows", 0)),
        "recap_profile_missing_character_ids": sorted(chars),
        "recap_cot_missing_labeled": int(a.get("recap_cot_missing_labeled", 0))
        + int(b.get("recap_cot_missing_labeled", 0)),
        "recap_cot_filled_labeled": int(a.get("recap_cot_filled_labeled", 0))
        + int(b.get("recap_cot_filled_labeled", 0)),
    }


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
    parser.add_argument(
        "--train-frac",
        type=float,
        default=0.8,
        help="全局 train 目标占比（RECAP∪COT 并集 T 上，与 val/test 之和为 1）。",
    )
    parser.add_argument(
        "--val-frac",
        type=float,
        default=0.1,
        help="全局 val 目标占比（同上）。",
    )
    parser.add_argument(
        "--test-frac",
        type=float,
        default=0.1,
        help="全局 test 槽占比；test 槽先预留 RECAP_test 内监督条数，再给 COT held-out。",
    )
    parser.add_argument(
        "--recap-test-labeled-min",
        type=int,
        default=2000,
        help="RECAP test：按整段对话抽样，直至 阻抗/合作 监督轮累计≥该值（当前数据每对话 1 条监督时可略超）。",
    )
    parser.add_argument(
        "--per-label-cap",
        type=int,
        default=260,
        help="按 label_code 分层时每层上限（减轻大类碾压长尾）；<=0 表示不截断。",
    )
    parser.add_argument("--manual-qc-size", type=int, default=300)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--recap-profile-path",
        type=Path,
        default=RESULTS / "profiles" / "recap.json",
        help="RECAP profile 列表 JSON；sample_id 与 dialogues 的 character_id 对齐。",
    )
    parser.add_argument(
        "--recap-cot-path",
        type=Path,
        default=RESULTS / "recap" / "recap_labeled_cot.json",
        help="RECAP 监督轮 COT 侧车（对象键为 sample_id 或 list[dict]）；不存在则跳过 COT 且不统计缺失。",
    )
    parser.add_argument(
        "--strict-recap-cot",
        action="store_true",
        help="当 --recap-cot-path 文件存在时，若仍有监督轮缺少 internal 则退出码 1。",
    )
    args = parser.parse_args()

    cot_rows = load_cot_samples()
    balanced_pool = build_balanced_pool(cot_rows, args.per_label_cap, args.seed)

    dialogues = load_recap_dialogues()
    profile_by_char = load_recap_profiles(args.recap_profile_path)
    recap_cot_path = args.recap_cot_path
    recap_cot_loaded = recap_cot_path.exists()
    recap_cot_by_sample = load_recap_cot_map(recap_cot_path) if recap_cot_loaded else {}
    count_cot_gaps = recap_cot_loaded

    test_dlgs, remainder_dlgs, part_meta = partition_recap_dialogues_for_test(
        dialogues,
        min_labeled=args.recap_test_labeled_min,
        seed=args.seed,
    )

    recap_test_rows, st_test = build_turn_rows_from_dialogues(
        test_dlgs,
        profile_by_char=profile_by_char,
        recap_cot_by_sample=recap_cot_by_sample,
        count_cot_gaps=count_cot_gaps,
    )
    recap_full_dialogues = build_full_dialogues_from_dialogues(
        test_dlgs, profile_by_char=profile_by_char
    )
    recap_labeled_targets, recap_context_only = split_recap_targets_and_context_only(recap_test_rows)

    rnd_dlg = random.Random(args.seed + 1337)
    remainder_shuffled = remainder_dlgs[:]
    rnd_dlg.shuffle(remainder_shuffled)
    n_train_d = (len(remainder_shuffled) * 8) // 9 if remainder_shuffled else 0
    train_recap_dlgs = remainder_shuffled[:n_train_d]
    val_recap_dlgs = remainder_shuffled[n_train_d:]

    train_recap_full = build_full_dialogues_from_dialogues(
        train_recap_dlgs, profile_by_char=profile_by_char
    )
    val_recap_full = build_full_dialogues_from_dialogues(
        val_recap_dlgs, profile_by_char=profile_by_char
    )
    train_recap_turn_rows, st_tr = build_turn_rows_from_dialogues(
        train_recap_dlgs,
        profile_by_char=profile_by_char,
        recap_cot_by_sample=recap_cot_by_sample,
        count_cot_gaps=count_cot_gaps,
    )
    val_recap_turn_rows, st_va = build_turn_rows_from_dialogues(
        val_recap_dlgs,
        profile_by_char=profile_by_char,
        recap_cot_by_sample=recap_cot_by_sample,
        count_cot_gaps=count_cot_gaps,
    )
    recap_turn_stats = merge_turn_build_stats(merge_turn_build_stats(st_test, st_tr), st_va)

    train_rows, val_rows, test_sup_rows, feas = split_balanced_cot_with_recap_in_test_union(
        recap_labeled_targets,
        balanced_pool,
        args.train_frac,
        args.val_frac,
        args.test_frac,
        args.seed,
    )

    feas = {
        **feas,
        "recap_partition": part_meta,
        "recap_test_client_turns_total": len(recap_test_rows),
        "recap_train_full_dialogues": len(train_recap_dlgs),
        "recap_val_full_dialogues": len(val_recap_dlgs),
        "recap_train_client_turns": len(train_recap_turn_rows),
        "recap_val_client_turns": len(val_recap_turn_rows),
        "recap_context_only_turns_in_test_only": len(recap_context_only),
        "recap_profile_path": str(args.recap_profile_path),
        "recap_profile_keys_loaded": len(profile_by_char),
        "recap_turn_build_stats": recap_turn_stats,
        "recap_cot_path": str(recap_cot_path),
        "recap_cot_file_loaded": recap_cot_loaded,
    }

    if args.strict_recap_cot and recap_cot_loaded:
        miss = int(recap_turn_stats.get("recap_cot_missing_labeled", 0))
        if miss > 0:
            print(
                json.dumps(
                    {"error": "strict_recap_cot", "recap_cot_missing_labeled": miss},
                    ensure_ascii=False,
                ),
                file=sys.stderr,
            )
            raise SystemExit(1)

    non_resistance_review = build_non_resistance_review_queue(recap_test_rows)
    translation_judge_queue = build_translation_judge_queue(train_rows + val_rows + test_sup_rows)
    # Placeholder: manual QC pool built from translated rows in the future.
    translation_manual_qc_pool = build_translation_manual_qc_pool(
        translated_rows=[],
        sample_size=args.manual_qc_size,
        seed=args.seed,
    )

    out = OUT_DIR
    _dump_json(out / "train_supplementary_balanced.json", train_rows)
    _dump_json(out / "val_supplementary_balanced.json", val_rows)
    _dump_json(out / "test_supplementary_balanced.json", test_sup_rows)
    _dump_json(out / "train_recap_full_dialogues_retained.json", train_recap_full)
    _dump_json(out / "val_recap_full_dialogues_retained.json", val_recap_full)
    _dump_json(out / "train_recap_all_turn_level.json", train_recap_turn_rows)
    _dump_json(out / "val_recap_all_turn_level.json", val_recap_turn_rows)
    _dump_json(out / "test_recap_all_retained_turn_level.json", recap_test_rows)
    _dump_json(out / "test_recap_full_dialogues_retained.json", recap_full_dialogues)
    _dump_json(out / "test_recap_labeled_targets.json", recap_labeled_targets)
    _dump_json(out / "test_recap_context_only_null_labels.json", recap_context_only)
    _dump_json(out / "review_queue_recap_non_resistance.json", non_resistance_review)
    _dump_json(out / "translation_culture_judge_queue.json", translation_judge_queue)
    _dump_json(out / "translation_manual_qc_pool_template.json", translation_manual_qc_pool)

    report = {
        "policy": {
            "recap_test_holdout": "whole_dialogues_until_labeled_min",
            "recap_test_labeled_min": args.recap_test_labeled_min,
            "union_definition": "|RECAP_test_labeled_targets| + |balanced_clinical_cot|; RECAP train/val = whole dialogues in train_recap_* / val_recap_*",
            "target_global_fracs": [args.train_frac, args.val_frac, args.test_frac],
            "recap_outputs": "test_recap_* = holdout; remainder RECAP = train_recap_* + val_recap_* (dialogue-integrity preserved)",
            "cot_allocation": "COT split vs RECAP_test for global 8:1:1 feasibility; COT lists separate from RECAP dialogue JSON",
            "supplementary_datasets": ["esconv", "mesc", "annomi"],
            "extes_note": "results/extes/ excluded: no coop fine taxonomy, no profile, no COT—not same asset class as cot/*.json",
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
        "feasibility": feas,
        "splits": [
            summarize("train_supplementary_balanced_cot_only", train_rows),
            summarize("val_supplementary_balanced_cot_only", val_rows),
            summarize("test_supplementary_balanced", test_sup_rows),
            summarize("train_recap_all_turn_level", train_recap_turn_rows),
            summarize("val_recap_all_turn_level", val_recap_turn_rows),
            summarize("test_recap_all_retained_turn_level", recap_test_rows),
            summarize("test_recap_labeled_targets", recap_labeled_targets),
            summarize("test_recap_context_only_null_labels", recap_context_only),
        ],
        "queues": {
            "recap_non_resistance_review_count": len(non_resistance_review),
            "translation_culture_judge_count": len(translation_judge_queue),
            "recap_full_dialogues_count_test_holdout": len(recap_full_dialogues),
            "recap_full_dialogues_count_train": len(train_recap_full),
            "recap_full_dialogues_count_val": len(val_recap_full),
        },
        "notes": [
            "RECAP test = whole-dialogue holdout; labeled count ≈ recap_test_labeled_min.",
            "Remainder RECAP: shuffle at **dialogue** level then 8:1 split → train_recap_full_dialogues_retained + val_recap_full_dialogues_retained (same inner structure as test_recap_full_*).",
            "Turn-level convenience exports: train_recap_all_turn_level.json / val_recap_all_turn_level.json (turns only from dialogs in that split; dialogue order preserved within each dialog when iterating dialogues list).",
            "COT remains train_supplementary_balanced / val_supplementary_balanced; mix RECAP+COT in the **dataloader** (e.g. interleaved batches), not by flattening turns.",
            "8:1:1 feasibility uses |test_recap_labeled_targets| + |balanced COT| only.",
            "Optional COT held-out rows: test_supplementary_balanced (only when global 8:1:1 is feasible).",
            "Only test_recap_labeled_targets should be used as primary RECAP test eval targets.",
            "test_recap_context_only_null_labels are context carriers within the test holdout dialogues.",
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

