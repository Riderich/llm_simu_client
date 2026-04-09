"""
用 Qwen API 对阻抗样本进行细粒度分类
"""

import argparse
import json
import os
import re
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI


SYSTEM_PROMPT = """你是心理咨询对话数据标注专家。

任务：对阻抗样本进行 13 类细粒度分类。

阻抗行为分类：
1. 争辩-挑战：质疑咨询师所说内容的准确性
2. 争辩-贬低：贬低咨询师的专业能力或作用
3. 否认-责怪：将问题归咎于他人
4. 否认-不认同：不认同咨询师观点，无替代方案
5. 否认-找借口：为行为找借口，表达不会遵从
6. 否认-最小化：暗示咨询师夸大风险
7. 否认-悲观：做出悲观、消极的陈述
8. 否认-犹豫：对建议持保留态度
9. 否认-不愿改变：表明不愿意改变
10. 回避-最小的回应：以简短回答回避
11. 回避-界限设定：拒绝讨论某些话题
12. 忽视-不关注：沉浸在自己的话题，未关注咨询师
13. 忽视-岔开话题：改变谈话方向，提出新话题

输出JSON: {"fine_label":"类别","confidence":0.0-1.0}
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default="qwen-max")
    args = parser.parse_args()

    # Load env
    env_path = os.path.join(os.path.dirname(__file__), "../.env")
    if os.path.exists(env_path):
        load_dotenv(env_path)

    api_key = os.getenv("QWEN_API_KEY") or os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("QWEN_BASE_URL") or "https://dashscope.aliyuncs.com/compatible-mode/v1"
    
    if not api_key:
        print("Error: Missing QWEN_API_KEY")
        return

    client = OpenAI(api_key=api_key, base_url=base_url)

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Filter resistance samples
    samples = [s for s in data if s.get("binary_label") == "阻抗"]
    print(f"Processing {len(samples)} resistance samples...")

    labels_map = {
        "争辩-挑战": "A1", "争辩-贬低": "A2",
        "否认-责怪": "B1", "否认-不认同": "B2", "否认-找借口": "B3",
        "否认-最小化": "B4", "否认-悲观": "B5", "否认-犹豫": "B6", "否认-不愿改变": "B7",
        "回避-最小的回应": "C1", "回避-界限设定": "C2",
        "忽视-不关注": "D1", "忽视-岔开话题": "D2",
    }

    results = []
    for i, sample in enumerate(samples):
        context = sample.get("context", "")[:400]
        response = sample.get("response", "")

        user_prompt = f"""对话上下文：
{context}

来访者回应：
{response}

请判断阻抗行为类别，仅输出JSON。"""

        try:
            resp = client.chat.completions.create(
                model=args.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
                max_tokens=100,
            )
            text = resp.choices[0].message.content or ""
            
            # Extract JSON
            m = re.search(r"\{.*\}", text, flags=re.DOTALL)
            if m:
                parsed = json.loads(m.group(0))
                fine_label = parsed.get("fine_label", "").strip()
            else:
                fine_label = text.split("\n")[0][:15]
            
            fine_category = labels_map.get(fine_label, "Unknown")
            
            results.append({
                "sample_id": sample.get("sample_id", ""),
                "binary_label": "阻抗",
                "fine_label": fine_label,
                "fine_category": fine_category,
            })
            print(f"[{i+1}/{len(samples)}] {fine_label} -> {fine_category}")
        except Exception as e:
            print(f"[{i+1}/{len(samples)}] Error: {e}")
            results.append({
                "sample_id": sample.get("sample_id", ""),
                "binary_label": "阻抗",
                "fine_label": "ERROR",
                "fine_category": "Unknown",
            })

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nSaved to {args.output}")
    from collections import Counter
    print("Distribution:", dict(Counter([r["fine_category"] for r in results])))


if __name__ == "__main__":
    main()
