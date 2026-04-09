"""
用 Qwen API 对 RECAP 合作样本进行 CBS 2-8 细粒度分类
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

# CBS 系统提示词（中文适配版）
SYSTEM_PROMPT = """你是心理咨询对话标注专家。对来访者 utterance 进行 CBS 2-8 分类。

## 7 类定义（中文示例）

CBS2-认同: 赞同/接受咨询师观点（"是的"、"有道理"、"确实如此"）
CBS3-请求: 向咨询师提问/求助（"我该怎么办？"、"这是什么意思？"）
CBS4-叙述: 陈述事实/经历（"上周发生了..."、"我有三个朋友..."）
CBS5-认知探索: 探索想法/信念（"我在想..."、"我觉得可能是因为..."）
CBS6-情感探索: 探索情绪感受（"我感到很焦虑..."、"这让我很难过"）
CBS7-领悟: 顿悟/新理解（"我突然明白了..."、"我意识到..."）
CBS8-改变: 报告已做/将做的改变（"这周我开始..."、"我决定以后..."）

## 判别优先级（必须遵守）

1. Change > Insight: 既有顿悟又有行动 → CBS8
2. Request 优先: 含问号的求助/澄清 → CBS3（除非明显是反问）
3. Affective > Cognitive: 情绪词汇主导 → CBS6
4. Agreement 兜底: 简短配合/认同 → CBS2

## 特殊情形

- 简短附和（"嗯"、"对"、"是的"）→ CBS2
- 结束语（"谢谢"、"再见"）→ CBS2（礼貌配合）
- 混合类别 → 按优先级选最高
- 无法判断 → CBS2

输出JSON: {"cbs_type":"CBS2-8"}
"""

labels_map = {
    "CBS2": "认同", "CBS3": "请求", "CBS4": "叙述",
    "CBS5": "认知探索", "CBS6": "情感探索",
    "CBS7": "领悟", "CBS8": "改变",
}


def classify_recap_sample(sample):
    """对单个 RECAP 样本进行分类"""
    dialogue = sample.get("dialogue", [])
    target = sample.get("target_utterance", "")
    
    # 构建上下文（取最后3-4轮对话）
    context_lines = []
    for turn in dialogue[-6:]:  # 最后3轮（每轮2个turn）
        role = "来访者" if turn["role"] == "user" else "咨询师"
        content = turn["content"][:100]  # 限制长度
        context_lines.append(f"{role}: {content}")
    
    context = "\n".join(context_lines[:-1]) if len(context_lines) > 1 else "（对话开始）"
    
    user_prompt = f"""对话上下文：
{context}

来访者回应（需分类）：
{target}

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
        
    except Exception as e:
        print(f"  API错误: {e}")
        cbs_type = "Unknown"
    
    return cbs_type


def main():
    # 加载 RECAP 数据
    with open("workspace/dataset/RECAP.json", "r", encoding="utf-8") as f:
        recap = json.load(f)
    
    # 筛选合作样本
    coop_samples = [s for s in recap if not s.get('resistance_label', {}).get('has_resistance', True)]
    print(f"找到 {len(coop_samples)} 条 RECAP 合作样本")
    
    results = []
    save_every = 100
    output_file = "workspace/results/recap_coop_cbs.json"
    
    # 检查是否有部分结果
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            results = json.load(f)
        print(f"已加载 {len(results)} 条历史结果，从第 {len(results)+1} 条继续")
    
    start_idx = len(results)
    
    print(f"开始处理，每 {save_every} 条保存一次...")
    print(f"开始时间: {datetime.now().strftime('%H:%M:%S')}")
    
    for i, sample in enumerate(coop_samples[start_idx:], start=start_idx):
        cbs_type = classify_recap_sample(sample)
        
        # 保留原始信息，添加 CBS 分类
        result = {
            "sample_id": sample.get("sample_id", f"recap_{i}"),
            "text": sample.get("target_utterance", ""),
            "dialogue": sample.get("dialogue", []),
            "original_subtype": sample.get('resistance_label', {}).get('cooperative_subtype', ''),
            "cbs_type": f"{cbs_type}-{labels_map.get(cbs_type, 'Unknown')}",
            "source": "RECAP"
        }
        results.append(result)
        
        # 进度显示
        if (i + 1) % 50 == 0:
            print(f"  进度: {i+1}/{len(coop_samples)} ({(i+1)/len(coop_samples)*100:.1f}%)")
        
        # 定期保存
        if (i + 1) % save_every == 0:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"  [保存] 已处理 {i+1} 条")
    
    # 最终保存
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n完成！结果已保存到 {output_file}")
    print(f"结束时间: {datetime.now().strftime('%H:%M:%S')}")
    
    # 统计
    print("\nCBS 分布统计:")
    cbs_counter = Counter([r["cbs_type"] for r in results])
    for cbs_code, name in labels_map.items():
        cbs_type = f"{cbs_code}-{name}"
        count = cbs_counter.get(cbs_type, 0)
        pct = count / len(results) * 100
        print(f"  {cbs_type}: {count:4d} ({pct:5.1f}%)")
    
    unknown = cbs_counter.get("Unknown", 0)
    if unknown > 0:
        print(f"  Unknown: {unknown:4d} ({unknown/len(results)*100:5.1f}%)")
    
    # 对比原始 E1/E2/E3 分布
    print("\n原始 E1/E2/E3 分布:")
    e_counter = Counter([r["original_subtype"] for r in results])
    for e_type in ["E1", "E2", "E3"]:
        count = e_counter.get(e_type, 0)
        pct = count / len(results) * 100
        desc = {"E1": "探索型", "E2": "配合型", "E3": "领悟型"}.get(e_type, "")
        print(f"  {e_type} ({desc}): {count:4d} ({pct:5.1f}%)")


if __name__ == "__main__":
    main()
