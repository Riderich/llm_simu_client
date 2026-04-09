"""
RECAP 合作样本 CBS 2-8 分类
使用 Qwen API (qwen-turbo) 进行快速分类
"""
import os, json, time, re
from collections import Counter
from datetime import datetime
from openai import OpenAI

# API 配置
api_key = os.getenv("QWEN_API_KEY", "sk-85638ad815bd46e3b44ec5b22bb94d3a")
client = OpenAI(api_key=api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

INPUT_FILE = "workspace/dataset/RECAP.json"
OUTPUT_FILE = "workspace/results/recap_coop_cbs.json"
SAVE_EVERY = 50

CBS_PROMPT = """你是心理咨询标注专家。对来访者话语进行CBS 2-8分类。

类别定义:
CBS2-认同: 赞同/接受咨询师观点（"是的"、"有道理"）
CBS3-请求: 向咨询师提问/求助（"我该怎么办？"）
CBS4-叙述: 陈述事实/经历（"上周发生了..."）
CBS5-认知探索: 探索想法/信念（"我在想..."）
CBS6-情感探索: 探索情绪感受（"我感到很焦虑..."）
CBS7-领悟: 顿悟/新理解（"我突然明白了..."）
CBS8-改变: 报告已做/将做的改变（"这周我开始..."）

优先级: 改变>领悟>请求>情感探索>认知探索>认同>叙述

输出JSON: {"cbs_type": "CBS2-认同"}"""

labels_map = {
    "CBS2": "认同", "CBS3": "请求", "CBS4": "叙述",
    "CBS5": "认知探索", "CBS6": "情感探索",
    "CBS7": "领悟", "CBS8": "改变",
}


def format_context(dialogue, max_turns=3):
    """格式化对话上下文"""
    if not dialogue:
        return ""
    lines = []
    for turn in dialogue[-max_turns*2:]:
        role = turn.get("role", "")
        content = turn.get("content", "").strip()[:100]
        if role and content:
            spk_cn = "咨询师" if role == "assistant" else "来访者"
            lines.append(f"{spk_cn}: {content}")
    return "\n".join(lines[:-1]) if len(lines) > 1 else "（对话开始）"


def classify_sample(sample):
    """分类单个样本"""
    dialogue = sample.get("dialogue", [])
    target = sample.get("target_utterance", "")
    
    ctx = format_context(dialogue)
    msg = f"对话上下文:\n{ctx}\n\n来访者回应: {target}\n\n请输出CBS分类JSON。"
    
    try:
        resp = client.chat.completions.create(
            model="qwen-turbo",
            messages=[
                {"role": "system", "content": CBS_PROMPT},
                {"role": "user", "content": msg}
            ],
            temperature=0.1, max_tokens=50,
        )
        content = resp.choices[0].message.content.strip()
        
        # 提取 cbs_type
        m = re.search(r'"cbs_type"\s*:\s*"(CBS[2-8][^"]*)"', content)
        if m:
            cbs = m.group(1)
        else:
            # 直接匹配
            for code in ["CBS8", "CBS7", "CBS6", "CBS5", "CBS4", "CBS3", "CBS2"]:
                if code in content:
                    cbs = f"{code}-{labels_map.get(code, '')}"
                    break
            else:
                cbs = "Unknown"
    except Exception as e:
        print(f"\nAPI Error: {e}")
        cbs = "Error"
    
    return cbs


def main():
    # 加载数据
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 筛选合作样本
    coop_samples = [s for s in data if not s.get('resistance_label', {}).get('has_resistance', True)]
    
    # 添加ID
    for i, s in enumerate(coop_samples):
        if "sample_id" not in s:
            s["sample_id"] = f"recap_{i}"
    
    # 检查已有进度
    results = []
    start_idx = 0
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            results = json.load(f)
        done_ids = {r["sample_id"] for r in results}
        start_idx = len(done_ids)
        coop_samples = [s for s in coop_samples if s["sample_id"] not in done_ids]
    
    total = len(coop_samples)
    print(f"开始时间: {datetime.now().strftime('%H:%M:%S')}")
    print(f"总合作样本: 1000, 已完成: {start_idx}, 待处理: {total}")
    
    for i, sample in enumerate(coop_samples):
        cbs = classify_sample(sample)
        
        results.append({
            "sample_id": sample["sample_id"],
            "text": sample.get("target_utterance", ""),
            "dialogue": sample.get("dialogue", []),
            "original_subtype": sample.get('resistance_label', {}).get('cooperative_subtype', ''),
            "cbs_type": cbs if cbs.startswith("CBS") else f"{cbs}-",
            "source": "RECAP"
        })
        
        # 进度显示
        if (i + 1) % 10 == 0:
            print(f"  进度: {start_idx + i + 1}/1000 ({(start_idx + i + 1)/10:.1f}%) - {cbs}")
        
        # 定期保存
        if (i + 1) % SAVE_EVERY == 0:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"  [保存] 已处理 {start_idx + i + 1} 条")
        
        time.sleep(0.2)  # 控制速率
    
    # 最终保存
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n完成! 总计: {len(results)} 条")
    print(f"结束时间: {datetime.now().strftime('%H:%M:%S')}")
    
    # 统计
    print("\nCBS 分布统计:")
    cats = Counter([r["cbs_type"] for r in results])
    for k, v in cats.most_common():
        print(f"  {k}: {v}")
    
    # 原始分布对比
    print("\n原始 E1/E2/E3 分布:")
    e_cats = Counter([r["original_subtype"] for r in results])
    for e_type in ["E1", "E2", "E3"]:
        print(f"  {e_type}: {e_cats.get(e_type, 0)}")


if __name__ == "__main__":
    main()
