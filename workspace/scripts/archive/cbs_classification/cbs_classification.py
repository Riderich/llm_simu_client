#!/usr/bin/env python3
"""
ESConv CBS 2-8 分类脚本 - 使用 qwen-turbo (快速)
"""

import json
import os
import re
import sys
from datetime import datetime
from collections import Counter
from openai import OpenAI

# ============ 配置 ============
API_KEY = "sk-85638ad815bd46e3b44ec5b22bb94d3a"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL = "qwen-turbo"  # 最快的模型
INPUT_FILE = "results/esconv_labeled.json"
OUTPUT_FILE = "results/esconv_coop_cbs.json"
BATCH_SIZE = 100

# ============ CBS 提示词 ============
SYSTEM_PROMPT = """对来访者进行CBS 2-8分类：
CBS2-认同, CBS3-请求, CBS4-叙述, CBS5-认知, CBS6-情感, CBS7-领悟, CBS8-改变
优先级: Change>Insight>Request>Affective>Cognitive>Agreement
结束语→CBS2
输出JSON:{"cbs_type":"CBS2-8"}"""

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


def now():
    return datetime.now().strftime("%H:%M:%S")


def load_data():
    """加载数据"""
    print(f"[{now()}] Loading data...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    coop = [s for s in data if s.get("binary_label") == "合作"]
    print(f"[{now()}] Found {len(coop)} cooperative samples")
    return coop


def load_existing():
    """加载已有结果"""
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)
            print(f"[{now()}] Loaded {len(existing)} existing results")
            return existing
        except:
            pass
    return []


def classify(sample):
    """单条分类"""
    ctx = sample.get("context", "")[:200]
    resp = sample.get("response", "")
    user = f"上下文：{ctx}\n\n回应：{resp}\n\n输出JSON："
    
    try:
        r = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user},
            ],
            temperature=0.1,
            max_tokens=30,
        )
        text = r.choices[0].message.content or ""
        # 修复：匹配 CBS2 或 CBS2-xxx 格式
        m = re.search(r'"cbs_type"\s*:\s*"(CBS[2-8])', text)
        cbs_type = m.group(1) if m else "Unknown"
    except Exception as e:
        cbs_type = "Error"
    
    return {
        "sample_id": sample.get("sample_id"),
        "binary_label": "合作",
        "cbs_type": cbs_type,
        "response": resp,
    }


def save(results):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def print_stats(results):
    c = Counter([r["cbs_type"] for r in results])
    total = len(results)
    print(f"\n  Distribution:")
    for k, v in c.most_common():
        print(f"    {k}: {v:4d} ({v/total*100:5.1f}%)")


def main():
    print("=" * 60)
    print(f"CBS Classification | Model: {MODEL}")
    print("=" * 60)
    
    samples = load_data()
    existing = load_existing()
    start_idx = len(existing)
    results = existing.copy()
    
    if start_idx >= len(samples):
        print(f"[{now()}] All done!")
        print_stats(results)
        return
    
    print(f"[{now()}] Starting from {start_idx + 1}/{len(samples)}")
    print(f"[{now()}] Press Ctrl+C to pause\n")
    
    try:
        for i in range(start_idx, len(samples)):
            result = classify(samples[i])
            results.append(result)
            
            if (i + 1) % BATCH_SIZE == 0 or (i + 1) == len(samples):
                save(results)
                print(f"[{now()}] {i+1}/{len(samples)} ({(i+1)/len(samples)*100:.1f}%)")
                recent = results[-BATCH_SIZE:]
                c = Counter([r["cbs_type"] for r in recent])
                print(f"  Last {len(recent)}: {dict(c)}")
    
    except KeyboardInterrupt:
        print(f"\n[{now()}] Interrupted")
        save(results)
        print(f"[{now()}] Saved {len(results)} results")
        return
    
    print("\n" + "=" * 60)
    print(f"[{now()}] Complete! {len(results)} samples")
    print("=" * 60)
    print_stats(results)


if __name__ == "__main__":
    main()
