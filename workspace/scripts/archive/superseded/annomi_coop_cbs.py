"""
AnnoMI 合作样本 CBS 2-8 细粒度分类
  输入: workspace/results/annomi_full_binary_recap.json  (binary_label == "合作")
  输出: workspace/results/annomi_coop.json
  模型: qwen-turbo API (DashScope)
"""
import os
import json
import time
from collections import Counter
from tqdm import tqdm

INPUT_FILE  = "workspace/results/annomi_full_binary_recap.json"
OUTPUT_FILE = "workspace/results/annomi_coop.json"
SAVE_EVERY  = 100

CBS_PRIORITY = {
    "CBS8-改变": 7, "CBS7-领悟": 6, "CBS3-请求": 5,
    "CBS6-情感探索": 4, "CBS5-认知探索": 3,
    "CBS4-叙述": 2, "CBS2-认同": 1,
}

SYSTEM_PROMPT = """你是心理咨询标注专家。对来访者话语进行CBS 2-8分类。

## 类别定义 (Hill Client Behavior System)
- CBS2-认同: 同意咨询师观点，或表示理解、认可
- CBS3-请求: 寻求信息、建议或指导
- CBS4-叙述: 陈述事实、事件或经历（无情感/认知加工）
- CBS5-认知探索: 讨论想法、观点、意义或解释
- CBS6-情感探索: 探索、表达或澄清情感体验
- CBS7-领悟: 表达新理解、觉察或顿悟（"我明白了..."）
- CBS8-改变: 表达改变的意愿或行为（"我会尝试..."）

## 优先级 (高→低)
改变 > 领悟 > 请求 > 情感探索 > 认知探索 > 认同 > 叙述

## 规则
- 结束语/告别语 → CBS2-认同
- 单纯陈述事实 → CBS4-叙述
- 涉及情感但无领悟 → CBS6-情感探索
- 必须直接输出JSON，不要任何其他文字

## 输出格式
{"cbs_type": "CBS2-认同"} 或 {"cbs_type": "CBS3-请求"} 等"""


def get_api_key():
    key = os.getenv("DASHSCOPE_API_KEY") or os.getenv("QWEN_API_KEY")
    if key:
        return key
    for env_path in [".env", "workspace/.env"]:
        try:
            for line in open(env_path):
                k, _, v = line.strip().partition("=")
                if k in ("DASHSCOPE_API_KEY", "QWEN_API_KEY"):
                    return v.strip()
        except FileNotFoundError:
            pass
    raise ValueError("未找到 DASHSCOPE_API_KEY，请设置环境变量")


def call_api(message: str, client) -> str:
    try:
        resp = client.chat.completions.create(
            model="qwen-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
            temperature=0.1,
            max_tokens=50,
        )
        content = resp.choices[0].message.content.strip()
        try:
            return json.loads(content).get("cbs_type", "Unknown")
        except json.JSONDecodeError:
            for cbs in CBS_PRIORITY:
                if cbs in content:
                    return cbs
            return "Unknown"
    except Exception as e:
        print(f"API Error: {e}", flush=True)
        return "Error"


def main():
    from openai import OpenAI

    client = OpenAI(
        api_key=get_api_key(),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    data = json.load(open(INPUT_FILE, encoding="utf-8"))
    coop_samples = [s for s in data if s.get("binary_label") == "合作"]
    print(f"合作样本: {len(coop_samples)}", flush=True)

    # Resume
    existing: list = []
    done_ids: set = set()
    if os.path.exists(OUTPUT_FILE):
        existing = json.load(open(OUTPUT_FILE, encoding="utf-8"))
        done_ids = {r["sample_id"] for r in existing}
        print(f"已完成: {len(done_ids)}，剩余: {len(coop_samples) - len(done_ids)}", flush=True)

    todo = [s for s in coop_samples if s["sample_id"] not in done_ids]
    if not todo:
        print("全部完成！")
        return

    results = existing.copy()
    for i, s in enumerate(tqdm(todo, desc="CBS")):
        ctx = (s.get("context") or "").strip()
        tgt = (s.get("response") or "").strip()

        msg = f"对话上下文:\n{ctx}\n\n来访者话语:\n{tgt}\n\n请分类为CBS 2-8之一，输出JSON格式。"
        cbs_type = call_api(msg, client)

        results.append({
            "sample_id": s["sample_id"],
            "binary_label": "合作",
            "cbs_type": cbs_type,
            "response": tgt,
        })

        if (i + 1) % SAVE_EVERY == 0:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"  Saved {len(results)}/{len(coop_samples)}", flush=True)

        time.sleep(0.25)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n✓ 完成 → {OUTPUT_FILE}", flush=True)
    print(f"总计: {len(results)} 条", flush=True)
    print("\nCBS分布:", flush=True)
    for cat, cnt in Counter(r["cbs_type"] for r in results).most_common():
        print(f"  {cat}: {cnt}", flush=True)


if __name__ == "__main__":
    main()
