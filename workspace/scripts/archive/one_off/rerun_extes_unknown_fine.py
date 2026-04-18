import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm

_SCRIPTS = Path(__file__).resolve().parents[2]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from psychfire_resistance_fine_prompt import build_resistance_fine_user_prompt


MODEL_PATH = "/data5/zxj/llm_simu_client/ClientResistance-Model-Share/only_resistance_share_model"
FINE_PATH = Path("/data5/zxj/llm_simu_client/workspace/results/extes_resistance_fine.json")
BINARY_PATH = Path("/data5/zxj/llm_simu_client/workspace/results/extes_binary.json")

RERUN_OUT = Path("/data5/zxj/llm_simu_client/workspace/results/extes_unknown_420_rerun.json")
COMPARE_OUT = Path("/data5/zxj/llm_simu_client/workspace/results/extes_unknown_420_compare.json")
SUMMARY_OUT = Path("/data5/zxj/llm_simu_client/workspace/results/extes_unknown_420_analysis.json")

LABELS_MAP = {
    "争辩-挑战": "A1",
    "争辩-贬低": "A2",
    "否认-责怪": "B1",
    "否认-不认同": "B2",
    "否认-找借口": "B3",
    "否认-最小化": "B4",
    "否认-悲观": "B5",
    "否认-犹豫": "B6",
    "否认-不愿改变": "B7",
    "回避-最小的回应": "C1",
    "回避-界限设定": "C2",
    "忽视-不关注": "D1",
    "忽视-岔开话题": "D2",
    "A1": "A1",
    "A2": "A2",
    "B1": "B1",
    "B2": "B2",
    "B3": "B3",
    "B4": "B4",
    "B5": "B5",
    "B6": "B6",
    "B7": "B7",
    "C1": "C1",
    "C2": "C2",
    "D1": "D1",
    "D2": "D2",
}

ALL_CODES = ["A1", "A2", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "C1", "C2", "D1", "D2"]


def normalize_label(raw_text: str) -> tuple[str, str]:
    raw = (raw_text or "").split("\n")[0].strip()
    if "#" in raw:
        raw = raw.split("#")[0].strip()
    label = raw[:20].strip()
    cat = LABELS_MAP.get(label, "Unknown")
    if cat == "Unknown":
        for code in ALL_CODES:
            if code in label:
                cat = code
                break
    return label, cat


def main() -> None:
    fine = json.loads(FINE_PATH.read_text(encoding="utf-8"))
    binary = json.loads(BINARY_PATH.read_text(encoding="utf-8"))

    unknown_rows = [r for r in fine if r.get("fine_category") == "Unknown"]
    binary_by_id = {r["sample_id"]: r for r in binary}

    model_inputs = []
    for row in unknown_rows:
        sid = row["sample_id"]
        src = binary_by_id.get(sid, {})
        context = src.get("context", "")
        response = src.get("response", row.get("response", ""))
        model_inputs.append(
            {
                "sample_id": sid,
                "old_fine_label": row.get("fine_label", ""),
                "old_fine_category": row.get("fine_category", "Unknown"),
                "context": context,
                "response": response,
                "metadata": row.get("metadata", {}),
            }
        )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH, torch_dtype=torch.bfloat16, trust_remote_code=True
    ).to("cuda:0")
    model.eval()

    rerun = []
    for row in tqdm(model_inputs, desc="Rerunning Unknown fine labels"):
        ctx = row["context"] if isinstance(row["context"], str) else ""
        prompt = build_resistance_fine_user_prompt(ctx, row["response"])
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1536)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=15,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )
        decoded = tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[1] :], skip_special_tokens=True
        ).strip()
        new_label, new_cat = normalize_label(decoded)
        rerun.append(
            {
                **row,
                "new_raw_output": decoded,
                "new_fine_label": new_label,
                "new_fine_category": new_cat,
            }
        )

    RERUN_OUT.write_text(json.dumps(rerun, ensure_ascii=False, indent=2), encoding="utf-8")

    changed = [r for r in rerun if r["new_fine_label"] != r["old_fine_label"]]
    solved = [r for r in rerun if r["new_fine_category"] != "Unknown"]
    unresolved = [r for r in rerun if r["new_fine_category"] == "Unknown"]

    migration = Counter((r["old_fine_label"], r["new_fine_label"]) for r in rerun)
    new_cat_dist = Counter(r["new_fine_category"] for r in rerun)
    old_label_dist = Counter(r["old_fine_label"] for r in rerun)
    new_label_dist = Counter(r["new_fine_label"] for r in rerun)

    compare_rows = []
    for r in rerun:
        compare_rows.append(
            {
                "sample_id": r["sample_id"],
                "old_fine_label": r["old_fine_label"],
                "new_fine_label": r["new_fine_label"],
                "old_fine_category": r["old_fine_category"],
                "new_fine_category": r["new_fine_category"],
                "changed": r["new_fine_label"] != r["old_fine_label"],
                "solved_unknown": r["new_fine_category"] != "Unknown",
            }
        )
    COMPARE_OUT.write_text(json.dumps(compare_rows, ensure_ascii=False, indent=2), encoding="utf-8")

    grouped_examples = defaultdict(list)
    for r in rerun:
        key = f"{r['old_fine_label']} -> {r['new_fine_label']}"
        if len(grouped_examples[key]) < 3:
            grouped_examples[key].append(
                {
                    "sample_id": r["sample_id"],
                    "response": r["response"][:220],
                    "new_raw_output": r["new_raw_output"],
                }
            )

    summary = {
        "total_unknown_input": len(rerun),
        "changed_label_count": len(changed),
        "changed_label_rate": len(changed) / len(rerun) if rerun else 0.0,
        "solved_unknown_count": len(solved),
        "solved_unknown_rate": len(solved) / len(rerun) if rerun else 0.0,
        "still_unknown_count": len(unresolved),
        "still_unknown_rate": len(unresolved) / len(rerun) if rerun else 0.0,
        "old_fine_label_top20": old_label_dist.most_common(20),
        "new_fine_label_top20": new_label_dist.most_common(20),
        "new_fine_category_dist": new_cat_dist,
        "label_migration_top30": [(f"{a} -> {b}", c) for (a, b), c in migration.most_common(30)],
        "migration_examples": dict(grouped_examples),
    }
    SUMMARY_OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Done.")
    print(f"input unknown: {len(rerun)}")
    print(f"changed label: {len(changed)}")
    print(f"solved unknown: {len(solved)}")
    print(f"still unknown: {len(unresolved)}")
    print(f"wrote: {RERUN_OUT}")
    print(f"wrote: {COMPARE_OUT}")
    print(f"wrote: {SUMMARY_OUT}")


if __name__ == "__main__":
    main()
