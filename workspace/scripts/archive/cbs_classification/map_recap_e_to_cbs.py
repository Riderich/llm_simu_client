"""
将 RECAP 合作样本从 E1/E2/E3 映射到 CBS 2-8
基于启发式规则 + 文本特征
"""
import json
import re
from collections import Counter

# 加载数据
with open("workspace/dataset/RECAP.json", "r", encoding="utf-8") as f:
    recap = json.load(f)

coop_samples = [s for s in recap if not s.get('resistance_label', {}).get('has_resistance', True)]
print(f"RECAP 合作样本: {len(coop_samples)} 条")

# 关键词词典
AFFECTIVE_KEYWORDS = [
    "感觉", "感到", "觉得", "情绪", "心情", "焦虑", "难过", "痛苦", "害怕", "恐惧",
    "开心", "高兴", "悲伤", "愤怒", "失望", "沮丧", "孤独", "紧张", "担心"
]

COGNITIVE_KEYWORDS = [
    "想", "认为", "觉得", "看法", "想法", "观点", "角度", "思考", "反思",
    "意识到", "发现", "理解", "知道", "明白", "懂"
]

INSIGHT_KEYWORDS = [
    "突然", "明白", "意识到", "领悟", "醒悟", "顿悟", "原来", "发现", "看清楚",
    "想通", "理解", "认识到", "察觉到"
]

CHANGE_KEYWORDS = [
    "开始", "改变", "决定", "计划", "行动", "做", "尝试", "努力", "坚持",
    "改善", "调整", "转变", "变成", "成为", "不再", "以后"
]

REQUEST_KEYWORDS = [
    "怎么办", "怎么做", "对吗", "是吗", "什么意思", "为什么", "如何",
    "建议", "帮助", "?", "？"
]

AGREEMENT_KEYWORDS = [
    "对", "是的", "没错", "同意", "有道理", "明白", "懂了", "谢谢", "再见",
    "嗯", "好", "好的"
]


def classify_by_text(text, e_type):
    """基于文本特征和E-type进行分类"""
    text = text.lower()
    
    # 请求类 (最高优先级)
    if any(kw in text for kw in ["怎么办", "怎么做", "建议", "帮助"]) or "?" in text or "？" in text:
        return "CBS3-请求"
    
    # 改变类
    if any(kw in text for kw in ["开始", "改变", "决定", "计划", "行动", "不再", "以后"]):
        return "CBS8-改变"
    
    # 领悟类
    if any(kw in text for kw in ["突然明白", "意识到", "领悟", "想通", "原来如此"]):
        return "CBS7-领悟"
    
    # 根据 E-type 进一步判断
    if e_type == "E3":  # 领悟型
        # 检查是否有行动关键词
        if any(kw in text for kw in CHANGE_KEYWORDS):
            return "CBS8-改变"
        return "CBS7-领悟"
    
    elif e_type == "E1":  # 探索型
        # 情感探索 vs 认知探索
        affective_score = sum(1 for kw in AFFECTIVE_KEYWORDS if kw in text)
        cognitive_score = sum(1 for kw in COGNITIVE_KEYWORDS if kw in text)
        
        if affective_score > cognitive_score:
            return "CBS6-情感探索"
        elif cognitive_score > 0:
            return "CBS5-认知探索"
        else:
            return "CBS4-叙述"  # 默认叙述
    
    elif e_type == "E2":  # 配合型
        # 简短附和 vs 叙述事实
        if len(text) < 10 or any(kw in text for kw in ["对", "是的", "嗯", "好", "谢谢"]):
            return "CBS2-认同"
        else:
            return "CBS4-叙述"
    
    return "CBS4-叙述"  # 默认


# 处理所有样本
results = []
for i, sample in enumerate(coop_samples):
    text = sample.get("target_utterance", "")
    e_type = sample.get('resistance_label', {}).get('cooperative_subtype', 'E2')
    
    cbs = classify_by_text(text, e_type)
    
    results.append({
        "sample_id": sample.get("sample_id", f"recap_{i}"),
        "text": text,
        "dialogue": sample.get("dialogue", []),
        "original_subtype": e_type,
        "cbs_type": cbs,
        "source": "RECAP"
    })

# 保存结果
output_file = "workspace/results/recap_coop_cbs.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n结果已保存到: {output_file}")

# 统计
print("\nCBS 分布统计:")
cbs_counter = Counter([r["cbs_type"] for r in results])
for cbs, cnt in cbs_counter.most_common():
    pct = cnt / len(results) * 100
    print(f"  {cbs}: {cnt:4d} ({pct:5.1f}%)")

# E-type 与 CBS 的交叉统计
print("\nE-type → CBS 映射统计:")
for e_type in ["E1", "E2", "E3"]:
    e_samples = [r for r in results if r["original_subtype"] == e_type]
    e_cbs = Counter([r["cbs_type"] for r in e_samples])
    desc = {"E1": "探索型", "E2": "配合型", "E3": "领悟型"}.get(e_type, "")
    print(f"\n  {e_type} ({desc}) - {len(e_samples)}条:")
    for cbs, cnt in e_cbs.most_common():
        print(f"    {cbs}: {cnt}")

print(f"\n总计: {len(results)} 条")
