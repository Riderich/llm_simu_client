"""
修复剩余85条样本 - 使用精简版官方prompt
"""
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "4"

import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from collections import Counter
from tqdm import tqdm

# 精简版官方prompt - 保留核心约束，去掉冗余描述
REFINED_PROMPT = """# 角色
你是专业心理咨询师，对来访者的阻抗行为进行准确分类。

# 阻抗行为分类（仅以下13种）
1. 争辩-挑战：质疑咨询师内容的准确性
2. 争辩-贬低：贬低咨询师的专业能力
3. 否认-责怪：将问题归咎于他人
4. 否认-不认同：不认同咨询师观点，无替代方案
5. 否认-找借口：为行为找借口，表达不会遵从
6. 否认-最小化：暗示咨询师夸大风险
7. 否认-悲观：做出悲观消极陈述
8. 否认-犹豫：对建议持保留态度
9. 否认-不愿改变：直接表明不愿改变
10. 回避-最小的回应：以简短回答回避深入讨论
11. 回避-界限设定：拒绝讨论某些话题
12. 忽视-不关注：沉浸在自己的话题
13. 忽视-岔开话题：改变谈话方向，提出新话题

# 重要规则
- 必须且只能从上述13个类别中选择1个
- 直接输出类别名称，不要任何解释、注释或理由
- 禁止输出"无法识别"、"无阻抗"等额外文字
- 禁止输出多个类别

# 对话
### 上下文：
{0}

### 来访者回应：
{1}

### 阻抗类别："""

LABELS_MAP = {
    "争辩-挑战": "A1", "争辩-贬低": "A2",
    "否认-责怪": "B1", "否认-不认同": "B2", "否认-找借口": "B3",
    "否认-最小化": "B4", "否认-悲观": "B5", "否认-犹豫": "B6", "否认-不愿改变": "B7",
    "回避-最小的回应": "C1", "回避-界限设定": "C2",
    "忽视-不关注": "D1", "忽视-岔开话题": "D2",
}

VALID_LABELS = set(LABELS_MAP.keys())

def format_context(context_list, max_turns=2):
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

def is_still_invalid(item):
    """判断是否仍为无效标签"""
    label = item.get('fine_label', '').strip()
    # 清理常见污染
    label = label.replace('。', '').replace('#', '').strip()
    return label not in VALID_LABELS

def clean_output(raw_output):
    """清洗模型输出"""
    # 取第一行
    label = raw_output.split('\n')[0].strip()
    # 去掉标点
    label = label.replace('。', '').replace('，', '').replace('.', '').strip()
    # 去掉注释
    if '#' in label:
        label = label.split('#')[0].strip()
    # 取前20字符
    return label[:20]

def main():
    print("Loading data...")
    with open("results/esconv_labeled_utterance.json", "r") as f:
        raw_data = {x['sample_id']: x for x in json.load(f)}
    
    with open("results/esconv_resistance_fine_full.json", "r") as f:
        fine_data = json.load(f)
    
    # 筛选剩余无效样本
    invalid_samples = [x for x in fine_data if is_still_invalid(x)]
    print(f"Found {len(invalid_samples)} remaining invalid samples")
    
    if not invalid_samples:
        print("No invalid samples remaining!")
        return
    
    # 加载模型
    model_path = "/data5/zxj/llm_simu_client/ClientResistance-Model-Share/only_resistance_share_model"
    print(f"Loading model...")
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    device = torch.device("cuda:0")
    torch.cuda.set_device(0)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
    ).to(device)
    print(f"Model loaded: {model.device}")
    
    # 重新分类
    fixed_count = 0
    for item in tqdm(invalid_samples, desc="Reclassifying"):
        sample_id = item['sample_id']
        raw_item = raw_data.get(sample_id, {})
        context = format_context(raw_item.get('context', []))
        target = item['response']
        
        prompt = REFINED_PROMPT.format(context, target)
        
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=15,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )
        
        result = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True).strip()
        new_label = clean_output(result)
        
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
        pct = len(fine_data) / v if v > 0 else 0
        print(f"  {k}: {v} ({v/len(fine_data)*100:.1f}%)")

if __name__ == "__main__":
    main()
