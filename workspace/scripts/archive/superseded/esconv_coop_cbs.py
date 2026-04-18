"""
ESConv 合作样本 CBS 2-8 分类 (完整版)
- 输入: esconv_labeled_utterance.json
- 输出: esconv_coop_cbs_full.json
- 模型: qwen-turbo API
"""

import os
import json
import time
from collections import Counter
from tqdm import tqdm

# 配置
INPUT_FILE = "results/esconv_labeled_utterance.json"
OUTPUT_FILE = "results/esconv_coop_cbs_full.json"
SAVE_EVERY = 100

# CBS 优先级规则
CBS_PRIORITY = {
    "CBS8-改变": 7, "CBS7-领悟": 6, "CBS3-请求": 5,
    "CBS6-情感探索": 4, "CBS5-认知探索": 3, 
    "CBS4-叙述": 2, "CBS2-认同": 1
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


def call_qwen_api(message, client):
    """调用 Qwen API"""
    try:
        response = client.chat.completions.create(
            model="qwen-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ],
            temperature=0.1,
            max_tokens=50,
        )
        content = response.choices[0].message.content.strip()
        
        # 解析 JSON
        try:
            result = json.loads(content)
            return result.get("cbs_type", "Unknown")
        except json.JSONDecodeError:
            # 尝试从文本中提取
            for cbs in CBS_PRIORITY.keys():
                if cbs in content:
                    return cbs
            return "Unknown"
    except Exception as e:
        print(f"API Error: {e}")
        return "Error"


def format_context(context_list, max_turns=2):
    """格式化对话上下文"""
    if isinstance(context_list, str):
        return context_list
    if not context_list:
        return ""
    lines = []
    for turn in context_list[-max_turns:]:
        speaker = turn.get("speaker", turn.get("role", ""))
        content = turn.get("content", turn.get("text", "")).strip()
        if speaker and content:
            speaker_cn = "咨询师" if speaker in ["therapist", "supporter", "user"] else "来访者"
            lines.append(f"{speaker_cn}: {content}")
    return "\n".join(lines)


def main():
    from openai import OpenAI
    
    # 初始化 API
    api_key = os.getenv("DASHSCOPE_API_KEY") or os.getenv("QWEN_API_KEY")
    if not api_key:
        # 尝试从 .env 文件读取
        try:
            with open(".env", "r") as f:
                for line in f:
                    if line.startswith("QWEN_API_KEY="):
                        api_key = line.strip().split("=", 1)[1]
                        break
        except:
            pass
    if not api_key:
        raise ValueError("请设置 DASHSCOPE_API_KEY 或 QWEN_API_KEY 环境变量")
    
    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    
    # 加载数据
    print(f"加载数据: {INPUT_FILE}")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 筛选合作样本
    coop_samples = [s for s in data if s.get("prediction") == "合作"]
    print(f"总样本: {len(data)}, 合作样本: {len(coop_samples)}")
    
    # 检查已有结果
    existing_results = []
    processed_ids = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            existing_results = json.load(f)
        processed_ids = {r["sample_id"] for r in existing_results}
        print(f"已处理: {len(existing_results)} 条，继续处理...")
    
    # 筛选未处理样本
    samples_to_process = [s for s in coop_samples if s["sample_id"] not in processed_ids]
    if not samples_to_process:
        print("所有样本已处理完成！")
        return
    
    print(f"待处理: {len(samples_to_process)} 条")
    
    # 处理样本
    results = existing_results.copy()
    
    for i, sample in enumerate(tqdm(samples_to_process, desc="Processing")):
        context = format_context(sample.get("context", []))
        target = sample.get("target", "")
        
        # 构建请求
        message = f"对话上下文:\n{context}\n\n来访者话语:\n{target}\n\n请分类为CBS 2-8之一，输出JSON格式。"
        
        # 调用 API
        cbs_type = call_qwen_api(message, client)
        
        results.append({
            "sample_id": sample["sample_id"],
            "binary_label": "合作",
            "cbs_type": cbs_type,
            "response": target,
        })
        
        # 定期保存
        if (i + 1) % SAVE_EVERY == 0:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"  已保存: {len(results)}/{len(coop_samples)}")
        
        # 避免限流
        time.sleep(0.3)
    
    # 最终保存
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 完成！结果保存到: {OUTPUT_FILE}")
    print(f"总处理: {len(results)} 条")
    
    # 统计分布
    print("\nCBS类别分布:")
    for cat, count in Counter([r["cbs_type"] for r in results]).most_common():
        print(f"  {cat}: {count}")


if __name__ == "__main__":
    main()
