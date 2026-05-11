#!/usr/bin/env python3
"""
ExtES automatic audit + stratified review packet (Markdown).

Outputs (default paths under workspace/results/extes/):
  - extes_audit_report.md       — stats / distributions / join rates / heuristics
  - extes_review_packet.md      — sampled rows + human review criteria

Usage:
  python data_scripts/extes_audit_and_review_packet.py
  python data_scripts/extes_audit_and_review_packet.py --per-stratum 12 --seed 42
"""

from __future__ import annotations

import argparse
import json
import math
import random
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
DEFAULT_BINARY = REPO / "workspace/results/extes/binary.json"
DEFAULT_FINE = REPO / "workspace/results/extes/resist_fine.json"
DEFAULT_OUT_DIR = REPO / "workspace/results/extes"


def _pct(x: float) -> str:
    return f"{100.0 * x:.2f}%"


def _quantiles(xs: list[int]) -> dict[str, float]:
    if not xs:
        return {"p50": 0.0, "p90": 0.0, "p99": 0.0}
    ys = sorted(xs)
    n = len(ys)

    def q(p: float) -> float:
        if n == 1:
            return float(ys[0])
        idx = (n - 1) * p
        lo = int(math.floor(idx))
        hi = int(math.ceil(idx))
        if lo == hi:
            return float(ys[lo])
        return float(ys[lo] + (ys[hi] - ys[lo]) * (idx - lo))

    return {"p50": q(0.50), "p90": q(0.90), "p99": q(0.99)}


def _english_heuristic(text: str) -> bool:
    t = (text or "").strip()
    if not t:
        return False
    letters = sum(1 for c in t if "a" <= c.lower() <= "z")
    return letters / max(len(t), 1) > 0.55


def _scene_bucket(scene: str, top_scenes: list[str]) -> str:
    s = (scene or "").strip() or "(empty)"
    return s if s in top_scenes else "__other__"


def load_json_array(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{path} root must be a JSON array")
    return data


def run_audit(binary: list[dict[str, Any]], fine: list[dict[str, Any]]) -> dict[str, Any]:
    by_id: dict[str, dict[str, Any]] = {}
    dup_ids = 0
    for r in binary:
        sid = str(r.get("sample_id", "")).strip()
        if not sid:
            continue
        if sid in by_id:
            dup_ids += 1
        by_id[sid] = r

    bin_labels = Counter(str(r.get("binary_label", "")).strip() or "(empty)" for r in binary)
    scenes = Counter(
        str((r.get("metadata") or {}).get("scene", "")).strip() or "(empty)"
        for r in binary
    )
    top_scenes = [s for s, _ in scenes.most_common(12)]

    resp_lens = [len((r.get("response") or "").strip()) for r in binary]
    ctx_lens = [len((r.get("context") or "").strip()) for r in binary]

    norm_resp: dict[str, list[str]] = defaultdict(list)
    for r in binary:
        sid = str(r.get("sample_id", "")).strip()
        resp = (r.get("response") or "").strip().lower()
        key = re.sub(r"\s+", " ", resp)[:500]
        norm_resp[key].append(sid)

    dup_groups = sum(1 for _k, ids in norm_resp.items() if len(ids) > 1)
    dup_extra_rows = sum(len(ids) - 1 for ids in norm_resp.values() if len(ids) > 1)

    en_like = sum(1 for r in binary if _english_heuristic(str(r.get("response") or "")))

    dialog_indices = []
    bad_id_pattern = 0
    pat = re.compile(r"^extes_(\d+)_(\d+)$")
    for r in binary:
        sid = str(r.get("sample_id", "")).strip()
        m = pat.match(sid)
        if m:
            dialog_indices.append(int(m.group(1)))
        else:
            bad_id_pattern += 1

    fine_by_id = {str(r.get("sample_id", "")).strip(): r for r in fine if r.get("sample_id")}
    fine_hit = sum(1 for sid in fine_by_id if sid in by_id)
    fine_miss = len(fine_by_id) - fine_hit

    fine_cat = Counter(str(r.get("fine_category", "")).strip() or "(empty)" for r in fine)
    fine_lbl = Counter(str(r.get("fine_label", "")).strip() or "(empty)" for r in fine)

    did_min = min(dialog_indices) if dialog_indices else None
    did_max = max(dialog_indices) if dialog_indices else None

    empty_resp = sum(1 for r in binary if not (str(r.get("response") or "").strip()))
    short_resp = sum(1 for r in binary if 0 < len(str(r.get("response") or "").strip()) < 10)

    return {
        "binary_rows": len(binary),
        "binary_unique_sample_id": len(by_id),
        "binary_duplicate_sample_id_rows": dup_ids,
        "fine_rows": len(fine),
        "binary_label_dist": dict(bin_labels.most_common()),
        "scene_top": scenes.most_common(25),
        "scene_unique": len(scenes),
        "dialog_index_min": did_min,
        "dialog_index_max": did_max,
        "sample_id_non_standard_pattern": bad_id_pattern,
        "response_len_quantiles": _quantiles(resp_lens),
        "context_len_quantiles": _quantiles(ctx_lens),
        "empty_response": empty_resp,
        "short_response_lt10chars": short_resp,
        "normalized_response_duplicate_groups": dup_groups,
        "normalized_response_duplicate_extra_rows": dup_extra_rows,
        "response_looks_majority_english_heuristic": en_like,
        "fine_join_hit_in_binary": fine_hit,
        "fine_join_miss_binary_missing": fine_miss,
        "fine_category_top15": dict(fine_cat.most_common(15)),
        "fine_label_top15": dict(fine_lbl.most_common(15)),
        "_top_scenes_for_sampling": top_scenes,
    }


def audit_to_markdown(a: dict[str, Any]) -> str:
    lines = [
        "# ExtES 自动审计报告",
        "",
        "数据源：`binary.json`（来访轮次 + 上下文字符串）、`resist_fine.json`（阻抗细粒度子集）。",
        "",
        "## 1. 规模与主键",
        "",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| binary 行数 | {a['binary_rows']} |",
        f"| binary 唯一 sample_id | {a['binary_unique_sample_id']} |",
        f"| binary 重复 sample_id 行数（后者覆盖计数） | {a['binary_duplicate_sample_id_rows']} |",
        f"| resist_fine 行数 | {a['fine_rows']} |",
        "",
        "## 2. binary_label 分布",
        "",
        "| label | count |",
        "|-------|-------|",
    ]
    for k, v in sorted(a["binary_label_dist"].items(), key=lambda kv: -kv[1]):
        lines.append(f"| {k} | {v} |")
    lines.extend(["", "## 3. metadata.scene（Top 25）", "", "| scene | count |", "|-------|-------|"])
    for k, v in a["scene_top"]:
        lines.append(f"| {k} | {v} |")
    lines.extend(
        [
            "",
            f"- scene 种类数：**{a['scene_unique']}**",
            f"- dialog_index（从 sample_id `extes_<d>_<t>` 解析）范围：**{a['dialog_index_min']} ~ {a['dialog_index_max']}**",
            f"- sample_id 不符合 `extes_<digits>_<digits>`：**{a['sample_id_non_standard_pattern']}**",
            "",
            "## 4. 文本长度（字符）",
            "",
            "| 字段 | p50 | p90 | p99 |",
            "|------|-----|-----|-----|",
            (
                f"| response | {a['response_len_quantiles']['p50']:.0f} | "
                f"{a['response_len_quantiles']['p90']:.0f} | "
                f"{a['response_len_quantiles']['p99']:.0f} |"
            ),
            (
                f"| context | {a['context_len_quantiles']['p50']:.0f} | "
                f"{a['context_len_quantiles']['p90']:.0f} | "
                f"{a['context_len_quantiles']['p99']:.0f} |"
            ),
            "",
            f"- 空 response：**{a['empty_response']}**",
            f"- 极短 response（1–9 字符）：**{a['short_response_lt10chars']}**",
            "",
            "## 5. 规范化 response 重复（粗略）",
            "",
            "将 response `strip` + `lower` + 空白折叠后取前 500 字符作为键。",
        ]
    )
    dup_rate = (
        a["normalized_response_duplicate_extra_rows"] / a["binary_rows"]
        if a["binary_rows"]
        else 0.0
    )
    lines.extend(
        [
            "",
            f"- 重复键组数：**{a['normalized_response_duplicate_groups']}**",
            f"- 因重复多出来的行数：**{a['normalized_response_duplicate_extra_rows']}**（约占 binary 行 {_pct(dup_rate)}）",
            "",
            "## 6. 语言粗测（来访句）",
            "",
            f"- `response` 中英文字符占比阈值启发式判为「偏英文」：**{a['response_looks_majority_english_heuristic']}** "
            f"/ {a['binary_rows']}（{_pct(a['response_looks_majority_english_heuristic'] / a['binary_rows']) if a['binary_rows'] else 'N/A'}）",
            "",
            "## 7. resist_fine ↔ binary 对齐",
            "",
            f"- fine 中 sample_id 在 binary 命中：**{a['fine_join_hit_in_binary']}**",
            f"- fine 中 sample_id 在 binary 缺失：**{a['fine_join_miss_binary_missing']}**",
            "",
            "### fine_category Top 15",
            "",
            "| category | count |",
            "|----------|-------|",
        ]
    )
    for k, v in sorted(a["fine_category_top15"].items(), key=lambda kv: -kv[1]):
        lines.append(f"| {k} | {v} |")
    lines.extend(["", "### fine_label Top 15", "", "| fine_label | count |", "|------------|-------|"])
    for k, v in sorted(a["fine_label_top15"].items(), key=lambda kv: -kv[1]):
        lines.append(f"| {k} | {v} |")
    lines.extend(["", "---", "*脚本：`data_scripts/extes_audit_and_review_packet.py`*", ""])
    return "\n".join(lines)


REVIEW_CRITERIA = """## 人工评审标准（每条快速勾选 / 备注）

对下方每一条样本，建议回答四个问题（可用 ✅ / ⚠️ / ❌ 或 1–5 分）：

1. **对话真实性**：读来是否像真实来访者（vs 模板腔、翻译腔、人设断裂）。
2. **粗标签可信度**：`binary_label`（阻抗/合作）与当前 `response` 及上文是否一致。
3. **上下文可用性**：给定 `context`，是否足以支撑后续 profile 或「需要内心过程」类建模（信息过少则 profile/COT 成本高）。
4. **任务域匹配**：是否与您关心的中文 RECAP / 临床来访者模拟设定足够接近（主观即可）。

**汇总**：若 2）大量不可信 → 优先重做粗标或清洗；若 3）大量不可用 → 暂缓 profile/COT 管线；若 4）长期偏离 → 考虑仅作英文侧扩量或单独 loss。
"""


def stratified_samples(
    binary: list[dict[str, Any]],
    fine: list[dict[str, Any]],
    *,
    by_id: dict[str, dict[str, Any]],
    top_scenes: list[str],
    per_stratum: int,
    seed: int,
    fine_top_cats: int,
    per_fine_cat: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rnd = random.Random(seed)
    buckets: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for r in binary:
        scene = str((r.get("metadata") or {}).get("scene", "")).strip() or "(empty)"
        bl = str(r.get("binary_label", "")).strip() or "(empty)"
        bk = _scene_bucket(scene, top_scenes)
        buckets[(bl, bk)].append(r)

    picked_binary: list[dict[str, Any]] = []
    for key, rows in sorted(buckets.items()):
        rows = rows[:]
        rnd.shuffle(rows)
        take = min(per_stratum, len(rows))
        for r in rows[:take]:
            picked_binary.append({**r, "_stratum": f"{key[0]} | {key[1]}"})

    fine_counts = Counter(str(r.get("fine_category", "")).strip() or "(empty)" for r in fine)
    top_cats = [c for c, _ in fine_counts.most_common(fine_top_cats)]
    fine_buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in fine:
        cat = str(r.get("fine_category", "")).strip() or "(empty)"
        if cat in top_cats:
            fine_buckets[cat].append(r)

    picked_fine: list[dict[str, Any]] = []
    for cat in top_cats:
        rows = fine_buckets.get(cat, [])
        rows = rows[:]
        rnd.shuffle(rows)
        for r in rows[: min(per_fine_cat, len(rows))]:
            sid = str(r.get("sample_id", "")).strip()
            bin_row = by_id.get(sid)
            picked_fine.append(
                {
                    "fine_row": r,
                    "binary_join": bin_row,
                    "join_ok": bin_row is not None,
                    "_stratum": f"resist_fine | {cat}",
                }
            )
    return picked_binary, picked_fine


def escape_md_cell(s: str, max_len: int = 12000) -> str:
    t = (s or "").replace("\r\n", "\n").replace("\r", "\n")
    if len(t) > max_len:
        t = t[: max_len - 20] + "\n\n…(truncated)…"
    return t.replace("|", "\\|")


def review_packet_to_markdown(
    picked_binary: list[dict[str, Any]],
    picked_fine: list[dict[str, Any]],
) -> str:
    parts = [
        "# ExtES 分层抽样评审包",
        "",
        REVIEW_CRITERIA,
        "",
        "---",
        "",
        "## Part A — binary.json 分层样本",
        "",
        "分层：`binary_label` × (`metadata.scene` ∈ Top scenes 或 `__other__`)。",
        "",
        "| # | stratum | sample_id | binary_label | scene | len(resp) | len(ctx) |",
        "|---|---------|-----------|--------------|-------|-----------|----------|",
    ]
    for i, r in enumerate(picked_binary, 1):
        meta = r.get("metadata") or {}
        scene = str(meta.get("scene", "")).strip()
        resp = str(r.get("response") or "")
        ctx = str(r.get("context") or "")
        parts.append(
            f"| {i} | {escape_md_cell(str(r.get('_stratum', '')), 80)} | `{r.get('sample_id', '')}` | "
            f"{escape_md_cell(str(r.get('binary_label', '')), 20)} | {escape_md_cell(scene, 60)} | "
            f"{len(resp.strip())} | {len(ctx.strip())} |"
        )

    parts.extend(["", "### Part A 全文（逐条）", ""])

    for i, r in enumerate(picked_binary, 1):
        meta = r.get("metadata") or {}
        desc = str(meta.get("description", "")).strip()
        scene_v = str(meta.get("scene", "")).strip()
        parts.extend(
            [
                f"### A-{i}. `{r.get('sample_id', '')}` — {r.get('_stratum', '')}",
                "",
                f"- **scene**：{scene_v}",
                f"- **description**：{desc}",
                f"- **binary_label**：{r.get('binary_label', '')}",
                "",
                "**context**",
                "",
                "```text",
                str(r.get("context") or "").strip(),
                "```",
                "",
                "**response（来访当前句）**",
                "",
                "```text",
                str(r.get("response") or "").strip(),
                "```",
                "",
                "**raw_output（若有，节选）**",
                "",
                "```text",
                (str(r.get("raw_output") or "").strip())[:8000],
                "```",
                "",
                "---",
                "",
            ]
        )

    parts.extend(
        [
            "## Part B — resist_fine.json（按 fine_category 抽样，附 binary join）",
            "",
            "| # | stratum | sample_id | join_ok | binary_label | fine_category | fine_label |",
            "|---|---------|-----------|---------|--------------|---------------|------------|",
        ]
    )
    for i, pack in enumerate(picked_fine, 1):
        fr = pack["fine_row"]
        parts.append(
            f"| {i} | {escape_md_cell(str(pack.get('_stratum', '')), 40)} | `{fr.get('sample_id', '')}` | "
            f"{'yes' if pack['join_ok'] else 'no'} | {fr.get('binary_label', '')} | "
            f"{escape_md_cell(str(fr.get('fine_category', '')), 20)} | "
            f"{escape_md_cell(str(fr.get('fine_label', '')), 40)} |"
        )

    parts.extend(["", "### Part B 全文（逐条）", ""])

    for i, pack in enumerate(picked_fine, 1):
        fr = pack["fine_row"]
        br = pack["binary_join"]
        meta_f = fr.get("metadata") or {}
        parts.extend(
            [
                f"### B-{i}. `{fr.get('sample_id', '')}` — {pack.get('_stratum', '')}",
                "",
                f"- **join_ok**：{pack['join_ok']}",
                f"- **binary_label**：{fr.get('binary_label', '')}",
                f"- **fine_category / fine_label**：{fr.get('fine_category')} / {fr.get('fine_label')}",
                f"- **scene（fine metadata）**：{meta_f.get('scene', '')}",
                "",
                "**resist_fine.response（若 join 失败则仅此句）**",
                "",
                "```text",
                str(fr.get("response") or "").strip(),
                "```",
                "",
            ]
        )
        if br:
            meta_b = br.get("metadata") or {}
            parts.extend(
                [
                    "**binary.context（对齐全文）**",
                    "",
                    "```text",
                    str(br.get("context") or "").strip(),
                    "```",
                    "",
                    "**binary.response（应与 fine 一致场景下来访句）**",
                    "",
                    "```text",
                    str(br.get("response") or "").strip(),
                    "```",
                    "",
                    f"**description**：{str(meta_b.get('description', '')).strip()}",
                    "",
                ]
            )
        parts.extend(["---", ""])

    parts.append("\n*脚本：`data_scripts/extes_audit_and_review_packet.py`*\n")
    return "\n".join(parts)


def main() -> None:
    ap = argparse.ArgumentParser(description="ExtES audit + review packet markdown")
    ap.add_argument("--binary", type=Path, default=DEFAULT_BINARY)
    ap.add_argument("--resist-fine", type=Path, default=DEFAULT_FINE)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--per-stratum", type=int, default=12, help="每层 (binary_label × scene_bucket) 最多抽样条数")
    ap.add_argument("--fine-top-cats", type=int, default=8, help="resist_fine 按 fine_category Top-K 分层")
    ap.add_argument("--per-fine-cat", type=int, default=10, help="每个 fine_category 最多抽样条数")
    args = ap.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    audit_path = args.out_dir / "extes_audit_report.md"
    review_path = args.out_dir / "extes_review_packet.md"

    print("Loading resist_fine...", flush=True)
    fine = load_json_array(args.resist_fine)
    print("Loading binary (may take RAM)...", flush=True)
    binary = load_json_array(args.binary)

    audit = run_audit(binary, fine)
    top_scenes = audit.pop("_top_scenes_for_sampling")

    by_id = {}
    for r in binary:
        sid = str(r.get("sample_id", "")).strip()
        if sid:
            by_id[sid] = r

    audit_md = audit_to_markdown(audit)
    audit_path.write_text(audit_md, encoding="utf-8")
    print(f"Wrote {audit_path}", flush=True)

    pb, pf = stratified_samples(
        binary,
        fine,
        by_id=by_id,
        top_scenes=top_scenes,
        per_stratum=args.per_stratum,
        seed=args.seed,
        fine_top_cats=args.fine_top_cats,
        per_fine_cat=args.per_fine_cat,
    )
    review_md = review_packet_to_markdown(pb, pf)
    review_path.write_text(review_md, encoding="utf-8")
    print(f"Wrote {review_path} ({len(pb)} binary samples, {len(pf)} fine samples)", flush=True)


if __name__ == "__main__":
    main()
