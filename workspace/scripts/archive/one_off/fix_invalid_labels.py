"""
重新分类无效标签样本 - 使用官方 prompt
筛选出 Unknown 和无效组合的样本，用更严格的官方 prompt 重新分类
"""

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "4"

import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from collections import Counter
from tqdm import tqdm

# 官方 prompt（严格版本）
OFFICIAL_PROMPT = """# 角色：
你是一位非常专业的心理咨询师，你能够敏锐地察觉到来访者在心理咨询对话中产生的阻抗行为，并对来访者的阻抗行为进行准确的分类。

# 任务：
下面你将会被给到一段咨询师和来访者之间的心理咨询对话片段，包括上下文和来访者回应，以及来访者阻抗行为的分类体系。
请根据来访者阻抗行为分类体系，仔细品读上下文，判断来访者回应的唯一最合适的行为类型。

# 输入
## 来访者阻抗行为分类体系
1. 争辩：来访者质疑咨询师的专业性或诚信，对咨询师的资格或经验进行挑战性回应，对咨询师在咨询中所做的事的正确性表示怀疑，或认为咨询师不知道自己（来访者）在做什么，表达对咨询师的不满意。
争辩-挑战：来访者直接质疑咨询师所说内容、信息的准确性。
争辩-贬低：来访者质疑或直接贬低咨询师的个人能力、专业知识或在咨询中所起的作用。

2. 否认：来访者表现出不愿意认识问题、不合作、不愿意接受责任或采纳建议，无法配合咨询师的回应。
否认-责怪：当咨询师进行指导性的策略时，来访者以将问题归咎于其他人的方式来传达无法配合咨询师的意图。
否认-不认同：当咨询师使用指导性的策略时，例如引导来访者反思、引导来访者从新的视角看待问题、引导来访者思考可能的解决方案或直接提供建议等，来访者表示不认同咨询师，且未提供建设性的替代方案。
否认-找借口：来访者通过为自己的行为找借口，为自己辩解的方式，来表达不会遵从咨询师设定的方向。
否认-最小化：来访者暗示咨询师夸大了风险或危险，实际上情况并不那么糟糕。
否认-悲观：来访者对自己做出悲观、失败或消极的陈述，以此来表达不遵从咨询师设定的方向。
否认-犹豫：来访者对咨询师提供的信息或建议表示持保留态度。
否认-不愿改变：来访者表现出对现状的满意，缺乏改变的意愿；或表明不愿意改变。

3. 回避：来访者表现出对某个话题的逃避，不愿意讨论某个议题。
回避-最小的回应：来访者面对咨询师的开放式提问时，保留了重要信息，并以非常简短的、没有足够信息量的、没有体现出深度思考的回答进行回应，仅提供非常表面的信息予以比较敷衍的回复。
回避-界限设定：来访者直接拒绝或通过找各种理由来避免讨论某些话题。

4. 忽视：来访者表现出忽视或不跟随咨询师的迹象。在"忽视"行为下，来访者的回常常给人一种感觉为，没有跟随咨询师的指导，来访者似乎完全没有听到咨询师的话，或表现得好像咨询师什么也没说/问。
忽视-不关注：来访者沉浸在自己的话题或情绪中，他/她的回应仍在延续之前的陈述，表明他/她没有关注咨询师所说的话。
忽视-岔开话题：来访者改变咨询师所追求的谈话方向，提出新话题或关注点。

## 心理咨询对话：
### 上下文：
{0}

### 来访者回应：
{1}

# 输出格式
请输出一行，直接输出阻抗行为类别，不要输出任何其他内容。
阻抗行为必须为"争辩-挑战""争辩-贬低""否认-责怪""否认-不认同""否认-找借口""否认-最小化""否认-悲观""否认-犹豫""否认-不愿改变""回避-最小的回应""回避-界限设定""忽视-不关注""忽视-岔开话题"中的一个。"""

LABELS_MAP = {
    "争辩-挑战": "A1", "争辩-贬低": "A2",
    "否认-责怪": "B1", "否认-不认同": "B2", "否认-找借口": "B3",
    "否认-最小化": "B4", "否认-悲观": "B5", "否认-犹豫": "B6", "否认-不愿改变": "B7",
    "回避-最小的回应": "C1", "回避-界限设定": "C2",
    "忽视-不关注": "D1", "忽视-岔开话题": "D2",
}

VALID_LABELS = set(LABELS_MAP.keys())

def format_context(context_list, max_turns=3):
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

def is_invalid(item):
    """判断是否为无效标签"""
    label = item.get('fine_label', '')
    # 去掉注释
    if "#" in label:
        label = label.split("#")[0].strip()
    # 检查是否在有效集合中
    return label not in VALID_LABELS

def main():
    print("Loading data...")
    with open("results/esconv_labeled_utterance.json", "r") as f:
        raw_data = {x['sample_id']: x for x in json.load(f)}
    
    with open("results/esconv_resistance_fine_full.json", "r") as f:
        fine_data = json.load(f)
    
    # 筛选无效样本
    invalid_samples = [x for x in fine_data if is_invalid(x)]
    print(f"Found {len(invalid_samples)} invalid samples to reclassify")
    
    if not invalid_samples:
        print("No invalid samples found!")
        return
    
    # 加载模型
    model_path = "/data5/zxj/llm_simu_client/ClientResistance-Model-Share/only_resistance_share_model"
    print(f"Loading model from {model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
    ).to("cuda:0")
    print(f"Model loaded: {model.device}")
    
    # 重新分类
    fixed_count = 0
    for item in tqdm(invalid_samples, desc="Reclassifying"):
        sample_id = item['sample_id']
        raw_item = raw_data.get(sample_id, {})
        context = format_context(raw_item.get('context', []))
        target = item['response']
        
        prompt = OFFICIAL_PROMPT.format(context, target)
        
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1536)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=20,  # 官方可能更长
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )
        
        result = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True).strip()
        new_label = result.split("\n")[0][:25].strip()
        
        # 更新
        item['fine_label'] = new_label
        item['fine_category'] = LABELS_MAP.get(new_label, "Unknown")
        
        if new_label in VALID_LABELS:
            fixed_count += 1
    
    # 保存
    with open("results/esconv_resistance_fine_full.json", "w", encoding="utf-8") as f:
        json.dump(fine_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Reclassified {len(invalid_samples)} samples")
    print(f"  Fixed: {fixed_count}")
    print(f"  Still Unknown: {len(invalid_samples) - fixed_count}")
    
    cats = Counter([x['fine_category'] for x in fine_data])
    print(f"\nFinal distribution:")
    for k, v in cats.most_common():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
