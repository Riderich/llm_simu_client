import json
import time
import os
from openai import OpenAI

# yunwu API + qwen3.5-plus
client = OpenAI(
    api_key="sk-4GBFSb4E7q3ZneOH12kuY80iKO1eqQBrKxmzhFgsm9l0aNMe",
    base_url="https://yunwu.ai/v1",
    timeout=20
)

OUTPUT_FILE = "workspace/results/recap_coop_cbs_plus.json"
labels = {"CBS2": "认同", "CBS3": "请求", "CBS4": "叙述", "CBS5": "认知探索", "CBS6": "情感探索", "CBS7": "领悟", "CBS8": "改变"}

def classify(text):
    try:
        resp = client.chat.completions.create(
            model="qwen3.5-plus",
            messages=[{"role": "user", "content": f'对来访者话分类(CBS2-8):"{text}" 只输出类别如CBS4-叙述'}],
            max_tokens=20, temperature=0,
        )
        content = resp.choices[0].message.content
        for code in ["CBS8", "CBS7", "CBS6", "CBS5", "CBS4", "CBS3", "CBS2"]:
            if code in content:
                return f"{code}-{labels[code]}"
        return "CBS4-叙述"
    except Exception as e:
        print(f"[ERR] {e}", flush=True)
        return "CBS4-叙述"

print("[START] yunwu + qwen3.5-plus v2", flush=True)

with open("workspace/dataset/RECAP.json") as f:
    recap = json.load(f)

coop_samples = [s for s in recap if not s.get('resistance_label', {}).get('has_resistance', True)]

# 检查已有进度
results = []
start = 0
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE) as f:
        results = json.load(f)
    start = len(results)

print(f"[INFO] 总样本: {len(coop_samples)}, 已处理: {start}, 待处理: {len(coop_samples)-start}", flush=True)

if start >= len(coop_samples):
    print("[DONE] 已全部完成", flush=True)
    exit(0)

for i in range(start, len(coop_samples)):
    text = coop_samples[i].get("target_utterance", "")
    cbs = classify(text)
    results.append({"sample_id": f"recap_{i}", "text": text, "cbs_type": cbs, "source": "RECAP"})
    
    if (i + 1) % 10 == 0:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False)
        print(f"[SAVE] {i+1}/{len(coop_samples)} - {cbs}", flush=True)
    
    time.sleep(0.1)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"[DONE] {len(results)} 条", flush=True)

# 统计
from collections import Counter
c = Counter([r["cbs_type"] for r in results])
print(f"[STATS] {dict(c)}", flush=True)
