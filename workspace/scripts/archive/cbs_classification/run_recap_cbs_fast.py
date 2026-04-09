"""
用 Qwen API 对 RECAP 合作样本进行 CBS 2-8 细粒度分类（快速版，批量处理）
"""

import json
import os
import re
from openai import OpenAI
from collections import Counter
from datetime import datetime
import concurrent.futures
import time

# API 配置
api_key = os.getenv("QWEN_API_KEY", "sk-85638ad815bd46e3b44ec5b22bb94d3a")
base_url = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
client = OpenAI(api_key=api_key, base_url=base_url)

# CBS 系统提示词
SYSTEM_PROMPT = """你是心理咨询对话标注专家。对来访者 utterance 进行 CBS 2-8 分类。

## 7 类定义
CBS2-认同: 赞同/接受咨询师观点（"是的"、"有道理"）
CBS3-请求: 向咨询师提问/求助（"我该怎么办？"）
CBS4-叙述: 陈述事实/经历（"上周发生了..."）
CBS5-认知探索: 探索想法/信念（"我在想..."）
CBS6-情感探索: 探索情绪感受（"我感到很焦虑..."）
CBS7-领悟: 顿悟/新理解（"我突然明白了..."）
CBS8-改变: 报告已做/将做的改变（"这周我开始..."）

## 优先级
Change>Insight; Request优先; Affective>Cognitive; Agreement兜底

输出JSON: {"cbs_type":"CBS2-8"}"""

labels_map = {
    "CBS2": "认同", "CBS3": "请求", "CBS4": "叙述",
    "CBS5": "认知探索", "CBS6": "情感探索",
    "CBS7": "领悟", "CBS8": "改变",
}


def classify_single(sample):
    """分类单个样本"""
    dialogue = sample.get("dialogue", [])
    target = sample.get("target_utterance", "")
    
    # 构建上下文
    context_lines = []
    for turn in dialogue[-4:]:
        role = "来访者" if turn["role"] == "user" else "咨询师"
        content = turn["content"][:80]
        context_lines.append(f"{role}: {content}")
    
    context = "\n".join(context_lines[:-1]) if len(context_lines) > 1 else "（对话开始）"
    
    user_prompt = f"""上下文：{context}
来访者：{target}
CBS类别？输出JSON：{{"cbs_type":"CBS2-8"}}"""
    
    try:
        resp = client.chat.completions.create(
            model="qwen3.5-397b-a17b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
            max_tokens=30,
        )
        text = resp.choices[0].message.content or ""
        
        # 提取 cbs_type
        m = re.search(r'"cbs_type"\s*:\s*"(CBS[2-8])"', text)
        if m:
            cbs_type = m.group(1)
        else:
            for cbs in ["CBS8", "CBS7", "CBS6", "CBS5", "CBS4", "CBS3", "CBS2"]:
                if cbs in text:
                    cbs_type = cbs
                    break
            else:
                cbs_type = "CBS2"  # 默认认同
        
    except Exception as e:
        print(f"  API错误: {e}")
        cbs_type = "CBS2"
    
    return {
        "sample_id": sample.get("sample_id", ""),
        "text": target,
        "original_subtype": sample.get('resistance_label', {}).get('cooperative_subtype', ''),
        "cbs_type": f"{cbs_type}-{labels_map.get(cbs_type, '认同')}",
        "source": "RECAP"
    }


def main():
    # 加载数据
    with open("workspace/dataset/RECAP.json", "r", encoding="utf-8") as f:
        recap = json.load(f)
    
    coop_samples = [s for s in recap if not s.get('resistance_label', {}).get('has_resistance', True)]
    print(f"找到 {len(coop_samples)} 条 RECAP 合作样本")
    print(f"开始时间: {datetime.now().strftime('%H:%M:%S')}")
    
    output_file = "workspace/results/recap_coop_cbs.json"
    
    # 检查已有结果
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            results = json.load(f)
        print(f"已加载 {len(results)} 条历史结果，继续处理...")
        coop_samples = coop_samples[len(results):]
    else:
        results = []
    
    # 串行处理（API 限制）
    total = len(coop_samples)
    for i, sample in enumerate(coop_samples):
        result = classify_single(sample)
        results.append(result)
        
        # 每10条显示进度
        if (i + 1) % 10 == 0:
            elapsed = time.time() - start_time if i > 0 else 0
            speed = (i + 1) / elapsed if elapsed > 0 else 0
            eta = (total - i - 1) / speed if speed > 0 else 0
            print(f"  进度: {i+1}/{total} ({(i+1)/total*100:.1f}%) | 速度: {speed:.1f}条/秒 | 预计剩余: {eta/60:.1f}分钟")
        
        # 每50条保存
        if (i + 1) % 50 == 0:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
    
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
    
    # 对比原始分布
    print("\n原始 E1/E2/E3 分布:")
    e_counter = Counter([r["original_subtype"] for r in results])
    for e_type in ["E1", "E2", "E3"]:
        count = e_counter.get(e_type, 0)
        pct = count / len(results) * 100
        desc = {"E1": "探索型", "E2": "配合型", "E3": "领悟型"}.get(e_type, "")
        print(f"  {e_type} ({desc}): {count:4d} ({pct:5.1f}%)")


if __name__ == "__main__":
    start_time = time.time()
    main()
