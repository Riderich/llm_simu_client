"""
AnnoMI 阻抗样本细粒度分类
  输入: workspace/results/annomi_full_binary_recap.json  (binary_label == "阻抗")
  输出: workspace/results/annomi_resistance.json
  模型: RECAP 本地模型 (GPU 4) → A1-D2 (11类)
"""
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "4"

import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from collections import Counter
from tqdm import tqdm

from psychfire_resistance_fine_prompt import build_resistance_fine_user_prompt

INPUT_FILE  = "workspace/results/annomi_full_binary_recap.json"
OUTPUT_FILE = "workspace/results/annomi_resistance.json"
MODEL_PATH  = "/data5/zxj/llm_simu_client/ClientResistance-Model-Share/only_resistance_share_model"
SAVE_EVERY  = 100

LABELS_MAP = {
    "争辩-挑战": "A1", "争辩-贬低": "A2",
    "否认-责怪": "B1", "否认-不认同": "B2", "否认-找借口": "B3",
    "否认-最小化": "B4", "否认-悲观": "B5", "否认-犹豫": "B6", "否认-不愿改变": "B7",
    "回避-最小的回应": "C1", "回避-界限设定": "C2",
    "忽视-不关注": "D1", "忽视-岔开话题": "D2",
    "A1": "A1", "A2": "A2",
    "B1": "B1", "B2": "B2", "B3": "B3", "B4": "B4",
    "B5": "B5", "B6": "B6", "B7": "B7",
    "C1": "C1", "C2": "C2",
    "D1": "D1", "D2": "D2",
}

CODES = ["A1","A2","B1","B2","B3","B4","B5","B6","B7","C1","C2","D1","D2"]

def classify(model, tokenizer, samples):
    results = []
    for i, s in enumerate(tqdm(samples, desc="Resistance fine")):
        ctx = (s.get("context") or "").strip()
        tgt = (s.get("response") or "").strip()
        prompt = build_resistance_fine_user_prompt(ctx, tgt)

        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1536)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model.generate(
                **inputs, max_new_tokens=15, do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )

        raw = tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True
        ).strip().split("\n")[0].split("#")[0].strip()[:20]

        cat = LABELS_MAP.get(raw, "Unknown")
        if cat == "Unknown":
            for code in CODES:
                if code in raw:
                    cat = code
                    break

        results.append({
            "sample_id": s["sample_id"],
            "binary_label": "阻抗",
            "fine_label": raw,
            "fine_category": cat,
            "response": tgt,
        })

        if (i + 1) % SAVE_EVERY == 0:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"  Saved {len(results)}", flush=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return results


def main():
    print(f"GPU: {os.environ.get('CUDA_VISIBLE_DEVICES')}", flush=True)

    data = json.load(open(INPUT_FILE, encoding="utf-8"))
    res_samples = [s for s in data if s.get("binary_label") == "阻抗"]
    print(f"阻抗样本: {len(res_samples)}", flush=True)

    # Resume
    done_ids: set = set()
    existing: list = []
    if os.path.exists(OUTPUT_FILE):
        existing = json.load(open(OUTPUT_FILE, encoding="utf-8"))
        done_ids = {r["sample_id"] for r in existing}
        print(f"已完成: {len(done_ids)}，剩余: {len(res_samples) - len(done_ids)}", flush=True)

    todo = [s for s in res_samples if s["sample_id"] not in done_ids]
    if not todo:
        print("全部完成！")
        return

    print("加载模型...", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=True
    )
    print(f"模型加载完成: {model.device}", flush=True)

    # Prepend existing so checkpoint file stays complete
    results_so_far = existing.copy()

    class _Wrapper:
        pass

    # Monkey-patch to accumulate on top of existing
    original_classify = classify

    def classify_with_resume(model, tokenizer, todo_samples):
        results = results_so_far.copy()
        for i, s in enumerate(tqdm(todo_samples, desc="Resistance fine")):
            ctx = (s.get("context") or "").strip()
            tgt = (s.get("response") or "").strip()
            prompt = build_resistance_fine_user_prompt(ctx, tgt)
            inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1536)
            inputs = {k: v.to(model.device) for k, v in inputs.items()}
            with torch.no_grad():
                outputs = model.generate(
                    **inputs, max_new_tokens=15, do_sample=False,
                    pad_token_id=tokenizer.eos_token_id,
                )
            raw = tokenizer.decode(
                outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True
            ).strip().split("\n")[0].split("#")[0].strip()[:20]
            cat = LABELS_MAP.get(raw, "Unknown")
            if cat == "Unknown":
                for code in CODES:
                    if code in raw:
                        cat = code
                        break
            results.append({
                "sample_id": s["sample_id"],
                "binary_label": "阻抗",
                "fine_label": raw,
                "fine_category": cat,
                "response": tgt,
            })
            if (i + 1) % SAVE_EVERY == 0:
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                print(f"  Saved {len(results)}", flush=True)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        return results

    results = classify_with_resume(model, tokenizer, todo)

    print("\n分布:", flush=True)
    for cat, cnt in Counter(r["fine_category"] for r in results).most_common():
        print(f"  {cat}: {cnt}", flush=True)
    print(f"\n✓ 完成 → {OUTPUT_FILE}", flush=True)


if __name__ == "__main__":
    main()
