import json
import time
import os
from openai import OpenAI

api_key = "sk-85638ad815bd46e3b44ec5b22bb94d3a"
client = OpenAI(api_key=api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", timeout=30)

OUTPUT_FILE = "workspace/results/recap_coop_cbs_plus.json"
labels = {"CBS2": "认同", "CBS3": "请求", "CBS4": "叙述", "CBS5": "认知探索", "CBS6": "情感探索", "CBS7": "领悟", "CBS8": "改变"}

print("[START] 使用 qwen3.5-flash 开始分类", flush=True)

with open("workspace/dataset/RECAP.json") as f:
    recap = json.load(f)

coop_samples = [s for s in recap if not s.get('resistance_label', {}).get('has_resistance', True)]

# 加载已有进度（从之前的30条继续）
results = []
start = 0
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE) as f:
        results = json.load(f)
    start = len(results)
    print(f"[RESUME] 从第 {start} 条继续", flush=True)

for i in range(start, 1000):
    text = coop_samples[i].get("target_utterance", "")
    cbs = "CBS4-叙述"  # 默认
    
    try:
        resp = client.chat.completions.create(
            model="qwen3.5-flash",
            messages=[{"role": "user", "content": f'对来访者话分类(CBS2-8):"{text}" 只输出类别如CBS4-叙述'}],
            max_tokens=15, temperature=0,
        )
        content = resp.choices[0].message.content
        for code in ["CBS8", "CBS7", "CBS6", "CBS5", "CBS4", "CBS3", "CBS2"]:
            if code in content:
                cbs = f"{code}-{labels[code]}"
                break
    except Exception as e:
        print(f"[ERROR] {i+1}: {e}", flush=True)
    
    results.append({"sample_id": f"recap_{i}", "text": text, "cbs_type": cbs, "source": "RECAP"})
    
    # 每10条保存
    if (i + 1) % 10 == 0:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False)
        print(f"[SAVE] {i+1}/1000", flush=True)
    
    time.sleep(0.05)  # flash模型更快，间隔可以更短

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"[DONE] 完成 {len(results)} 条", flush=True)

# 统计
from collections import Counter
c = Counter([r["cbs_type"] for r in results])
print(f"[STATS] {dict(c)}", flush=True)
