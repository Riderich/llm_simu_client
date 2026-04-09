"""
用 Qwen API 对合作样本进行 CBS 2-8 细粒度分类
CBS 2-8: Agreement, AppropriateRequests, Recounting, Cognitive-BehavioralExploration, AffectiveExploration, Insight, TherapeuticChanges
"""

import json
import os
import re
from openai import OpenAI
from collections import Counter
from datetime import datetime

# API 配置
api_key = os.getenv("QWEN_API_KEY", "sk-85638ad815bd46e3b44ec5b22bb94d3a")
base_url = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
client = OpenAI(api_key=api_key, base_url=base_url)
print(f"Using model: qwen3.5-397b-a17b")

# 加载数据
with open("results/esconv_labeled.json", "r", encoding="utf-8") as f:
    data = json.load(f)

coop_samples = [s for s in data if s.get("binary_label") == "合作"]
print(f"找到 {len(coop_samples)} 条合作样本")

# CBS 系统提示词（精简版）
SYSTEM_PROMPT = """你是心理咨询对话标注专家。对来访者 utterance 进行 CBS 2-8 分类。

## 7 类定义（一句话核心特征）

CBS2-Agreement: 赞同/接受咨询师观点（"是的"、"有道理"）
CBS3-Request: 向咨询师提问/求助（"我该怎么办？"）
CBS4-Recounting: 叙述过往事件（"上周发生了..."）
CBS5-Cognitive: 探索想法/信念/行为模式（"我在想..."）
CBS6-Affective: 探索情绪感受（"我感到很..."）
CBS7-Insight: 顿悟/新理解（"我突然明白了..."）
CBS8-Change: 报告已做/将做的改变（"这周我开始..."）

## 判别优先级（必须遵守）

1. Change > Insight: 既有顿悟又有行动 → CBS8
2. Request 优先: 含问号的求助/澄清 → CBS3（除非明显是反问）
3. Affective > Cognitive: 情绪词汇主导 → CBS6
4. Agreement 兜底: 简短配合/认同 → CBS2

## 特殊情形

- 结束语（bye/thanks/goodbye）→ CBS2（礼貌配合）
- 混合类别 → 按优先级选最高
- 无法判断 → CBS2

输出JSON: {"cbs_type":"CBS2-8"}
"""

labels_map = {
    "CBS2": "Agreement", "CBS3": "AppropriateRequests", "CBS4": "Recounting",
    "CBS5": "Cognitive-BehavioralExploration", "CBS6": "AffectiveExploration",
    "CBS7": "Insight", "CBS8": "TherapeuticChanges",
}

results = []
save_every = 100  # 每100条保存一次
output_file = "results/esconv_coop_cbs.json"

print(f"开始处理，每 {save_every} 条保存一次...")
print(f"开始时间: {datetime.now().strftime('%H:%M:%S')}")

for i, sample in enumerate(coop_samples):
    context = sample.get("context", "")[:200]
    response = sample.get("response", "")
    
    user_prompt = f"""对话上下文：
{context}

来访者回应：
{response}

请判断CBS类别，输出JSON。"""
    
    try:
        resp = client.chat.completions.create(
            model="qwen3.5-397b-a17b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
            max_tokens=50,
        )
        text = resp.choices[0].message.content or ""
        
        # 提取 cbs_type
        m = re.search(r'"cbs_type"\s*:\s*"(CBS[2-8])"', text)
        if m:
            cbs_type = m.group(1)
        else:
            # 尝试直接匹配
            for cbs in ["CBS8", "CBS7", "CBS6", "CBS5", "CBS4", "CBS3", "CBS2"]:
                if cbs in text:
                    cbs_type = cbs
                    break
            else:
                cbs_type = "Unknown"
        
        confidence_match = re.search(r'"confidence"\s*:\s*(0?\.\d+|1\.0|1)', text)
        confidence = float(confidence_match.group(1)) if confidence_match else 0.5
        
    except Exception as e:
        print(f"  错误 at {i+1}: {e}")
        cbs_type = "Unknown"
        confidence = 0.0
    
    results.append({
        "sample_id": sample.get("sample_id", ""),
        "binary_label": "合作",
        "cbs_type": cbs_type,
        "cbs_name": labels_map.get(cbs_type, "Unknown"),
        "confidence": confidence,
        "response": response,
    })
    
    # 进度显示
    if (i + 1) % 50 == 0:
        print(f"  进度: {i+1}/{len(coop_samples)} ({(i+1)/len(coop_samples)*100:.1f}%)")
    
    # 定期保存
    if (i + 1) % save_every == 0:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"  [保存] 已处理 {i+1} 条，结果保存到 {output_file}")

# 最终保存
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n完成！结果已保存到 {output_file}")
print(f"结束时间: {datetime.now().strftime('%H:%M:%S')}")

# 统计
print("\nCBS 分布统计:")
cbs_counter = Counter([r["cbs_type"] for r in results])
for cbs in ["CBS2", "CBS3", "CBS4", "CBS5", "CBS6", "CBS7", "CBS8", "Unknown"]:
    count = cbs_counter.get(cbs, 0)
    pct = count / len(results) * 100
    name = labels_map.get(cbs, "Unknown")
    print(f"  {cbs} ({name}): {count:4d} ({pct:5.1f}%)")
