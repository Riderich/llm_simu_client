"""
RECAP 模型 Transformers 推理脚本
使用 Transformers 在指定 GPU 上稳定推理
"""

import os
import sys
import json
import argparse
from typing import List, Dict
from tqdm import tqdm

# 设置 GPU
os.environ["CUDA_VISIBLE_DEVICES"] = sys.argv[sys.argv.index("--gpu") + 1] if "--gpu" in sys.argv else "4"

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

BINARY_INSTRUCTION = """# 角色：
你是一位非常专业的心理咨询师，你能够敏锐地察觉到来访者在心理咨询对话中产生的阻抗行为，区分来访者的行为是阻抗还是合作。

# 任务：
下面你将会被给到一段咨询师和来访者之间的心理咨询对话片段，包括上下文和来访者回应，以及来访者阻抗行为和合作行为的定义。
请仔细品读上下文，判断来访者回应的行为类型为阻抗还是合作。

# 输入
## 阻抗：是指来访者的行为偏离、阻碍咨询师提出的咨询方向。
## 合作：来访者遵从咨询师设定的方向进行回应。

## 心理咨询对话：
### 上下文：
{0}

### 来访者回应：
{1}

# 输出格式
判断来访者的回应为"阻抗"或是"合作"。请输出一行，不要输出任何其他内容。
"""

def load_data(filepath: str, data_format: str = "esconv") -> List[Dict]:
    """加载数据（Utterance 级别）"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    samples = []
    for conv in data:
        dialog = conv.get('dialog', conv.get('dialogue', []))
        conv_id = str(conv.get('problem', conv.get('dialogue_id', len(samples))))[:20]
        
        # 遍历所有 turn，为每句 seeker 生成样本
        for i, turn in enumerate(dialog):
            speaker = turn.get('speaker', turn.get('role', ''))
            if speaker in ['seeker', 'client', 'user']:
                # 跳过第一句（没有上下文）
                if i == 0:
                    continue
                context = dialog[:i]
                samples.append({
                    'context': context,
                    'target': turn.get('content', turn.get('text', '')),
                    'sample_id': f"{conv_id}_{i}",  # 唯一 ID
                })
    return samples


def load_existing_results(filepath: str) -> Dict[str, Dict]:
    """加载已有结果，返回 sample_id -> result 的映射"""
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {item.get('sample_id', ''): item for item in data if item.get('sample_id')}
    except:
        return {}

def format_context(context: List[Dict]) -> str:
    """格式化上下文"""
    lines = []
    for turn in context[-3:]:  # 只取最后3轮
        speaker = turn.get('speaker', '')
        content = turn.get('content', '')
        lines.append(f"{speaker}: {content}")
    return '\n'.join(lines)

def predict_batch(model, tokenizer, samples: List[Dict], batch_size: int = 8) -> List[str]:
    """批量预测"""
    results = []
    for i in tqdm(range(0, len(samples), batch_size), desc="Processing"):
        batch = samples[i:i+batch_size]
        prompts = []
        for sample in batch:
            context_str = format_context(sample['context'])
            prompt = BINARY_INSTRUCTION.format(context_str, sample['target'])
            prompts.append(prompt)
        
        # 单条处理避免 OOM
        for prompt in prompts:
            inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048).to(model.device)
            with torch.no_grad():
                outputs = model.generate(**inputs, max_new_tokens=10, do_sample=False, pad_token_id=tokenizer.eos_token_id)
            result = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()
            # 提取"阻抗"或"合作"
            if "阻抗" in result[:10]:
                results.append("阻抗")
            elif "合作" in result[:10]:
                results.append("合作")
            else:
                results.append(result.split('\n')[0][:10])
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="输入文件")
    parser.add_argument("--output", required=True, help="输出文件")
    parser.add_argument("--model", default="/data5/zxj/llm_simu_client/ClientResistance-Model-Share/binary_share_model")
    parser.add_argument("--gpu", default="4", help="GPU ID")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--data-format", default="esconv")
    parser.add_argument("--save-every", type=int, default=50, help="每多少条保存一次")
    args = parser.parse_args()
    
    print(f"Using GPU: {os.environ.get('CUDA_VISIBLE_DEVICES')}")
    print(f"Loading model from: {args.model}")
    
    # 加载模型
    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )
    
    print(f"Model loaded. Device: {model.device}")
    
    # 加载已有结果（断点续传）
    print(f"Checking existing results: {args.output}")
    existing_results = load_existing_results(args.output)
    print(f"  Found {len(existing_results)} existing results")
    
    # 加载数据
    print(f"Loading data from: {args.input}")
    all_samples = load_data(args.input, args.data_format)
    
    # 过滤已存在的样本
    samples = [s for s in all_samples if s['sample_id'] not in existing_results]
    
    print(f"Total: {len(all_samples)}, Already processed: {len(existing_results)}, Remaining: {len(samples)}")
    
    if not samples:
        print("\n✅ All samples already processed!")
        return
    
    # 准备输出（包含已有结果）
    results = list(existing_results.values())
    
    # 预测
    print(f"Starting inference (saving every {args.save_every} samples)...")
    total_done = len(existing_results)
    
    for i in range(0, len(samples), args.batch_size):
        batch = samples[i:i + args.batch_size]
        batch_preds = predict_batch(model, tokenizer, batch, len(batch))
        
        for sample, pred in zip(batch, batch_preds):
            results.append({
                'sample_id': sample['sample_id'],
                'context': sample['context'],
                'target': sample['target'],
                'prediction': pred,
            })
            total_done += 1
        
        # 定期保存
        if total_done % args.save_every < args.batch_size or i + len(batch) >= len(samples):
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"  💾 Saved ({total_done}/{len(all_samples)})")
    
    print(f"\n✅ 结果已保存: {args.output}")
    from collections import Counter
    predictions = [r['prediction'] for r in results]
    print(f"分布: {Counter(predictions)}")

if __name__ == "__main__":
    main()
