"""
ESConv 细粒度标注脚本
- 阻抗样本: 用 only_resistance_share_model 进行 11 类分类
- 合作样本: 调用 classify_cbs_coop.py 进行 CBS 2-8 分类
"""

import os
import sys
import json
import argparse
from collections import Counter

os.environ["CUDA_VISIBLE_DEVICES"] = sys.argv[sys.argv.index("--gpu") + 1] if "--gpu" in sys.argv else "4"

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


RESISTANCE_INSTRUCTION = """# 角色：
你是一位非常专业的心理咨询师，能够敏锐地察觉并准确分类来访者的阻抗行为。

# 来访者阻抗行为分类：
1. 争辩-挑战：质疑咨询师所说内容的准确性
2. 争辩-贬低：贬低咨询师的专业能力或作用
3. 否认-责怪：将问题归咎于他人
4. 否认-不认同：不认同咨询师观点，无替代方案
5. 否认-找借口：为行为找借口，表达不会遵从
6. 否认-最小化：暗示咨询师夸大风险
7. 否认-悲观：做出悲观、消极的陈述
8. 否认-犹豫：对建议持保留态度
9. 否认-不愿改变：表明不愿意改变
10. 回避-最小的回应：以简短回答回避
11. 回避-界限设定：拒绝讨论某些话题
12. 忽视-不关注：沉浸在自己的话题，未关注咨询师
13. 忽视-岔开话题：改变谈话方向，提出新话题

# 对话：
### 上下文：
{0}

### 来访者回应：
{1}

# 输出格式
请输出一行，直接输出阻抗行为类别。
"""

RESISTANCE_LABELS = {
    "争辩-挑战": "A1", "争辩-贬低": "A2",
    "否认-责怪": "B1", "否认-不认同": "B2", "否认-找借口": "B3",
    "否认-最小化": "B4", "否认-悲观": "B5", "否认-犹豫": "B6", "否认-不愿改变": "B7",
    "回避-最小的回应": "C1", "回避-界限设定": "C2",
    "忽视-不关注": "D1", "忽视-岔开话题": "D2",
}


def format_context(context_list, max_turns=5):
    if isinstance(context_list, str):
        return context_list
    lines = []
    for turn in context_list[-max_turns:]:
        speaker = turn.get("speaker", turn.get("role", ""))
        content = turn.get("content", turn.get("text", "")).strip()
        if speaker and content:
            speaker_cn = "咨询师" if speaker in ["therapist", "supporter", "user"] else "来访者"
            lines.append(f"{speaker_cn}: {content}")
    return "\n".join(lines)


def predict_resistance(model, tokenizer, samples, batch_size=4):
    results = []
    for i in range(0, len(samples), batch_size):
        batch = samples[i:i+batch_size]
        for sample in batch:
            metadata = sample.get("metadata", {})
            context_list = metadata.get("dialog", [])
            context_str = format_context(context_list[:-1] if context_list else [])
            target = sample.get("response", "")
            
            prompt = RESISTANCE_INSTRUCTION.format(context_str, target)
            inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048).to(model.device)
            
            with torch.no_grad():
                outputs = model.generate(**inputs, max_new_tokens=20, do_sample=False, pad_token_id=tokenizer.eos_token_id)
            
            result = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()
            fine_label = result.split("\n")[0][:20]
            fine_category = RESISTANCE_LABELS.get(fine_label, "Unknown")
            
            results.append({
                "sample_id": sample.get("sample_id", ""),
                "binary_label": "阻抗",
                "fine_label": fine_label,
                "fine_category": fine_category,
            })
        print(f"  Resistance: {min(i+len(batch), len(samples))}/{len(samples)}")
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="results/esconv_labeled.json")
    parser.add_argument("--output", default="results/esconv_fine_labeled.json")
    parser.add_argument("--resistance-model", default="/data5/zxj/llm_simu_client/ClientResistance-Model-Share/only_resistance_share_model")
    parser.add_argument("--gpu", default="4")
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--skip-cbs", action="store_true")
    args = parser.parse_args()
    
    print(f"Using GPU: {os.environ.get('CUDA_VISIBLE_DEVICES')}")
    
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"Total samples: {len(data)}")
    
    resistance_samples = [s for s in data if s.get("binary_label") == "阻抗"]
    coop_samples = [s for s in data if s.get("binary_label") == "合作"]
    
    print(f"Resistance: {len(resistance_samples)}, Cooperative: {len(coop_samples)}")
    
    output_data = []
    
    # 处理阻抗样本
    if resistance_samples:
        print("\nLoading resistance model...")
        tokenizer = AutoTokenizer.from_pretrained(args.resistance_model, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            args.resistance_model,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            trust_remote_code=True,
        )
        print(f"Model loaded: {model.device}")
        
        resistance_results = predict_resistance(model, tokenizer, resistance_samples, args.batch_size)
        output_data.extend(resistance_results)
        
        # 统计
        print("\nResistance distribution:")
        for label, count in Counter([r["fine_category"] for r in resistance_results]).most_common():
            print(f"  {label}: {count}")
    
    # 保存合作样本待处理
    if coop_samples and not args.skip_cbs:
        print(f"\n{len(coop_samples)} cooperative samples to be processed with CBS classification")
        # 保存中间结果
        temp_output = args.output.replace(".json", "_temp.json")
        with open(temp_output, "w", encoding="utf-8") as f:
            json.dump({
                "resistance": output_data,
                "cooperative_pending": coop_samples,
            }, f, ensure_ascii=False, indent=2)
        print(f"Temp saved to: {temp_output}")
        print("\nRun CBS classification:")
        print(f"  python scripts/classify_cbs_coop.py --input {temp_output} --output {args.output}")
    elif resistance_samples:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"\nSaved to: {args.output}")


if __name__ == "__main__":
    main()
