"""
RECAP 合作样本 CBS 分类 - 高频保存监控版
每10条保存一次，方便监控进度
"""
import json
import time
import sys
from openai import OpenAI

api_key = "sk-85638ad815bd46e3b44ec5b22bb94d3a"
client = OpenAI(api_key=api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", timeout=20)

OUTPUT_FILE = "workspace/results/recap_coop_cbs_plus.json"

labels = {"CBS2": "认同", "CBS3": "请求", "CBS4": "叙述", "CBS5": "认知探索", "CBS6": "情感探索", "CBS7": "领悟", "CBS8": "改变"}

print("[INFO] 加载数据...", flush=True)
with open("workspace/dataset/RECAP.json") as f:
    recap = json.load(f)

coop_samples = [s for s in recap if not s.get('resistance_label', {}).get('has_resistance', True)]
print(f"[INFO] 总合作样本: {len(coop_samples)}", flush=True)

# 加载已有进度
results = []
start_idx = 0
try:
    with open(OUTPUT_FILE) as f:
        results = json.load(f)
    start_idx = len(results)
    print(f"[INFO] 已处理: {start_idx} 条，从第 {start_idx+1} 条继续", flush=True)
except:
    print(f"[INFO] 新任务，从第 1 条开始", flush=True)

print("[INFO] 开始分类...", flush=True)

for i in range(start_idx, len(coop_samples)):
    text = coop_samples[i].get("target_utterance", "")
    
    try:
        resp = client.chat.completions.create(
            model="qwen3.5-plus-2026-02-15",
            messages=[{"role": "user", "content": f'对来访者话分类(CBS2-8):"{text}" 只输出类别如CBS4-叙述'}],
            max_tokens=15, temperature=0,
        )
        content = resp.choices[0].message.content
        # 解析
        cbs = "CBS4-叙述"  # 默认
        for code in ["CBS8", "CBS7", "CBS6", "CBS5", "CBS4", "CBS3", "CBS2"]:
            if code in content:
                cbs = f"{code}-{labels[code]}"
                break
    except Exception as e:
        print(f"[WARN] 第{i+1}条出错: {e}", flush=True)
        cbs = "CBS4-叙述"
    
    results.append({
        "sample_id": f"recap_{i}",
        "text": text,
        "cbs_type": cbs,
        "source": "RECAP"
    })
    
    # 每10条保存一次
    if (i + 1) % 10 == 0:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False)
        print(f"[PROGRESS] 已处理: {i+1}/1000 ({(i+1)/10:.1f}%)", flush=True)
    
    time.sleep(0.15)

# 最终保存
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"[DONE] 完成! 共 {len(results)} 条", flush=True)

# 统计
from collections import Counter
c = Counter([r["cbs_type"] for r in results])
print("[STATS] CBS分布:", dict(c), flush=True)
