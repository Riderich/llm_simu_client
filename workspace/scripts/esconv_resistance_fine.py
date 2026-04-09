"""
ESConv 阻抗样本 13 类细粒度标注 (完整版)
- 输入: esconv_labeled_utterance.json
- 输出: esconv_resistance_fine_full.json
- 模型: only_resistance_share_model
"""

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "4"

import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from collections import Counter
from tqdm import tqdm

# 配置
INPUT_FILE = "results/esconv_labeled_utterance.json"
OUTPUT_FILE = "results/esconv_resistance_fine_full.json"
MODEL_PATH = "/data5/zxj/llm_simu_client/ClientResistance-Model-Share/only_resistance_share_model"
BATCH_SIZE = 8
SAVE_EVERY = 100

# PsyFIRE 标签映射
LABELS_MAP = {
    "争辩-挑战": "A1", "争辩-贬低": "A2",
    "否认-责怪": "B1", "否认-不认同": "B2", "否认-找借口": "B3",
    "否认-最小化": "B4", "否认-悲观": "B5", "否认-犹豫": "B6", "否认-不愿改变": "B7",
    "回避-最小的回应": "C1", "回避-界限设定": "C2",
    "忽视-不关注": "D1", "忽视-岔开话题": "D2",
}

# 提示词
SYSTEM_PROMPT = """# 角色
你是专业心理咨询师，对来访者的阻抗行为进行分类。

# 阻抗行为定义与类别
## 争辩 (Challenging)
- 争辩-挑战(A1): 质疑咨询师所说内容的准确性、合理性和可能性
- 争辩-贬低(A2): 贬低咨询师的专业能力和作用

## 否认 (Denying)  
- 否认-责怪(B1): 将问题归咎于他人或外部环境
- 否认-不认同(B2): 不认同咨询师的观点，没有提出替代方案
- 否认-找借口(B3): 为行为找借口，表达不会遵从咨询建议
- 否认-最小化(B4): 暗示咨询师夸大了问题的严重性
- 否认-悲观(B5): 做出悲观、消极的陈述，表示没有希望
- 否认-犹豫(B6): 对咨询师的建议持保留态度，犹豫是否采纳
- 否认-不愿改变(B7): 直接表明不愿意改变现状

## 回避 (Avoiding)
- 回避-最小的回应(C1): 以简短回答回避深入讨论
- 回避-界限设定(C2): 拒绝讨论某些话题，设定界限

## 忽视 (Ignoring)
- 忽视-不关注(D1): 沉浸在自己的话题，未关注咨询师
- 忽视-岔开话题(D2): 改变谈话方向，提出新话题

# 任务
根据对话上下文和来访者回应，判断属于以上哪一类阻抗行为。
直接输出类别名称（如"争辩-挑战"），不要输出其他内容。"""


def format_context(context_list, max_turns=3):
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
    print(f"使用 GPU: {os.environ.get('CUDA_VISIBLE_DEVICES')}")
    
    # 加载数据
    print(f"\n加载数据: {INPUT_FILE}")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 筛选阻抗样本
    resistance_samples = [s for s in data if s.get("prediction") == "阻抗"]
    print(f"总样本: {len(data)}, 阻抗样本: {len(resistance_samples)}")
    
    # 检查已有结果（断点续传）
    existing_results = []
    processed_ids = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            existing_results = json.load(f)
        processed_ids = {r["sample_id"] for r in existing_results}
        print(f"已处理: {len(existing_results)} 条，继续处理...")
    
    # 筛选未处理的样本
    samples_to_process = [s for s in resistance_samples if s["sample_id"] not in processed_ids]
    if not samples_to_process:
        print("所有样本已处理完成！")
        return
    
    print(f"待处理: {len(samples_to_process)} 条")
    
    # 加载模型
    print(f"\n加载模型: {MODEL_PATH}")
    import torch
    # 如果设置了 CUDA_VISIBLE_DEVICES，直接使用 cuda:0
    device = torch.device("cuda:0")
    torch.cuda.set_device(0)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
    ).to(device)
    print(f"模型加载完成: {model.device}")
    
    # 处理样本
    results = existing_results.copy()
    
    for i, sample in enumerate(tqdm(samples_to_process, desc="Processing")):
        # 构建输入
        context = format_context(sample.get("context", []))
        target = sample.get("target", "")
        
        prompt = f"{SYSTEM_PROMPT}\n\n### 对话上下文:\n{context}\n\n### 来访者回应:\n{target}\n\n### 阻抗类别:\n"
        
        # 推理
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1536)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=15,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )
        
        # 解码结果
        result = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True).strip()
        # 提取标签（去掉注释）
        raw_label = result.split("\n")[0].strip()
        # 去掉 # 后面的注释
        if "#" in raw_label:
            raw_label = raw_label.split("#")[0].strip()
        fine_label = raw_label[:20].strip()
        fine_category = LABELS_MAP.get(fine_label, "Unknown")
        
        results.append({
            "sample_id": sample["sample_id"],
            "binary_label": "阻抗",
            "fine_label": fine_label,
            "fine_category": fine_category,
            "response": target,
        })
        
        # 定期保存
        if (i + 1) % SAVE_EVERY == 0:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"  已保存: {len(results)}/{len(resistance_samples)}")
    
    # 最终保存
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 完成！结果保存到: {OUTPUT_FILE}")
    print(f"总处理: {len(results)} 条")
    
    # 统计分布
    print("\n阻抗类别分布:")
    for cat, count in Counter([r["fine_category"] for r in results]).most_common():
        print(f"  {cat}: {count}")


if __name__ == "__main__":
    main()
