"""
RECAP 合作样本 CBS 2-8 分类 - qwen3.5-plus 版
"""
import json
import time
import re
from openai import OpenAI

api_key = "sk-85638ad815bd46e3b44ec5b22bb94d3a"
client = OpenAI(api_key=api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

CBS_PROMPT = """你是心理咨询标注专家。对来访者话语进行CBS 2-8分类。

类别定义:
CBS2-认同: 赞同/接受咨询师观点（"是的"、"有道理"、"同意"）
CBS3-请求: 向咨询师提问/求助（"我该怎么办？"、"什么意思"）
CBS4-叙述: 陈述事实/经历（"上周发生了..."、"我有三个孩子"）
CBS5-认知探索: 探索想法/信念（"我在想..."、"我觉得可能是因为..."）
CBS6-情感探索: 探索情绪感受（"我感到很焦虑..."、"这让我很难过"）
CBS7-领悟: 顿悟/新理解（"我突然明白了..."、"我意识到..."）
CBS8-改变: 报告已做/将做的改变（"这周我开始..."、"我决定以后..."）

优先级: 改变>领悟>请求>情感探索>认知探索>认同>叙述

只输出JSON: {"cbs_type": "CBS2-认同"}"""

labels_map = {
    "CBS2": "认同", "CBS3": "请求", "CBS4": "叙述",
    "CBS5": "认知探索", "CBS6": "情感探索",
    "CBS7": "领悟", "CBS8": "改变",
}

# 加载数据
with open("workspace/dataset/RECAP.json") as f:
    recap = json.load(f)

coop_samples = [s for s in recap if not s.get('resistance_label', {}).get('has_resistance', True)]

# 加载已有进度（从recap_coop_cbs_api.json继续）
output_file = "workspace/results/recap_coop_cbs_plus.json"
input_progress = "workspace/results/recap_coop_cbs_api.json"

try:
    with open(output_file) as f:
        results = json.load(f)
    start = len(results)
except:
    # 从之前的进度导入
    try:
        with open(input_progress) as f:
            prev = json.load(f)
        results = prev[:250]  # 保留前250条
        start = len(results)
        print(f"从之前进度导入 {start} 条")
    except:
        results = []
        start = 0

print(f"开始处理: {start}/{len(coop_samples)} 已完成，剩余 {len(coop_samples)-start}")

count = 0
for i in range(start, len(coop_samples)):
    sample = coop_samples[i]
    text = sample.get("target_utterance", "")
    
    try:
        resp = client.chat.completions.create(
            model="qwen3.5-plus-2026-02-15",
            messages=[
                {"role": "system", "content": CBS_PROMPT},
                {"role": "user", "content": f"来访者: {text}\n输出JSON:"}
            ],
            temperature=0.0,
            max_tokens=30,
        )
        content = resp.choices[0].message.content
        m = re.search(r'"cbs_type"\s*:\s*"(CBS[2-8])"', content)
        cbs = m.group(1) if m else "CBS4"
    except Exception as e:
        print(f"Error at {i}: {e}")
        cbs = "CBS4"
    
    results.append({
        "sample_id": sample.get("sample_id", f"recap_{i}"),
        "text": text,
        "dialogue": sample.get("dialogue", []),
        "cbs_type": f"{cbs}-{labels_map.get(cbs, '')}",
        "source": "RECAP"
    })
    
    count += 1
    if count % 50 == 0:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"  已保存: {i+1}/1000", flush=True)
    
    time.sleep(0.2)  # plus模型可以更快

# 最终保存
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n完成! 共 {len(results)} 条")

# 统计
from collections import Counter
cbs_counter = Counter([r["cbs_type"] for r in results])
print("\n分布统计:")
for k, v in cbs_counter.most_common():
    print(f"  {k}: {v}")
