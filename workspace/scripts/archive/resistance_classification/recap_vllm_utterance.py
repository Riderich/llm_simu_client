"""
RECAP vLLM 逐句标注脚本（支持断点续传）
对 ESConv 中每句 seeker 发言进行标注
每20批自动保存一次，支持从中断处继续
"""

import os
import sys
import json
import argparse
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

# 官方 Prompt
BINARY_INSTRUCTION = """# 角色：
你是一位非常专业的心理咨询师，你能够敏锐地察觉到来访者在心理咨询对话中产生的阻抗行为，区分来访者的行为是阻抗还是合作。

# 任务：
下面你将会被给到一段咨询师和来访者之间的心理咨询对话片段，包括上下文和来访者回应，以及来访者阻抗行为和合作行为的定义。
请仔细品读上下文，判断来访者回应的行为类型为阻抗还是合作。

# 输入
## 阻抗：是指来访者的行为偏离、阻碍咨询师提出的咨询方向。
具体的阻抗行为包括来访者质疑咨询师的专业性或诚信，对咨询师的资格或经验进行挑战性回应，对咨询师在咨询中所做的事的正确性表示怀疑，或认为咨询师不知道自己（来访者）在做什么，表达对咨询师的不满意（争辩）；
来访者表现出不愿意认识问题、不合作、不愿意接受责任或采纳建议，无法配合咨询师的回应（否认）；
来访者表现出对某个话题的逃避，不愿意讨论某个议题（回避）；
来访者表现出忽视或不跟随咨询师的迹象。在"忽视"行为下，来访者的回常常给人一种感觉为，没有跟随咨询师的指导，来访者似乎完全没有听到咨询师的话，或表现得好像咨询师什么也没说/问（忽视）。

## 合作：来访者遵从咨询师设定的方向进行回应。

## 心理咨询对话：
### 上下文：
{0}

### 来访者回应：
{1}

# 输出格式
判断来访者的回应为"阻抗"或是"合作"。请输出一行，不要输出任何其他内容。
"""


@dataclass
class UtteranceSample:
    """单句样本"""
    dialog_id: str
    turn_idx: int
    context: str
    response: str


@dataclass
class UtteranceResult:
    """单句结果"""
    dialog_id: str
    turn_idx: int
    binary_label: str
    raw_output: str = ""


class RecapVLLMInference:
    """vLLM 推理器"""
    
    def __init__(self, model_path: str, max_model_len: int = 4096):
        from vllm import LLM, SamplingParams
        
        print(f"Loading model from: {model_path}")
        self.llm = LLM(
            model=model_path,
            tensor_parallel_size=1,
            gpu_memory_utilization=0.55,
            max_model_len=max_model_len,
            dtype="bfloat16",
            trust_remote_code=True,
            enforce_eager=True,
        )
        self.sampling_params = SamplingParams(temperature=0, max_tokens=10)
        print(f"Model loaded")
    
    def _create_prompt(self, context: str, response: str) -> str:
        return BINARY_INSTRUCTION.format(context, response)
    
    def _extract_label(self, text: str) -> str:
        first_line = text.split('\n')[0].strip()
        if "阻抗" in first_line:
            return "阻抗"
        elif "合作" in first_line:
            return "合作"
        return first_line[:20]
    
    def infer_batch(self, samples: List[UtteranceSample], batch_size: int = 32, 
                    start_batch: int = 0, save_every: int = 20,
                    checkpoint_file: str = None) -> List[UtteranceResult]:
        """
        批量推理，支持断点续传和定期保存
        
        Args:
            samples: 所有样本
            batch_size: 批大小
            start_batch: 从第几批开始（断点续传）
            save_every: 每多少批保存一次
            checkpoint_file: 检查点文件路径
        """
        from vllm import SamplingParams
        
        results = []
        total_batches = (len(samples) + batch_size - 1) // batch_size
        
        print(f"Total batches: {total_batches}, starting from batch {start_batch}")
        
        for i in range(start_batch * batch_size, len(samples), batch_size):
            batch = samples[i:i + batch_size]
            batch_num = i // batch_size + 1
            
            prompts = [self._create_prompt(s.context, s.response) for s in batch]
            outputs = self.llm.generate(prompts, self.sampling_params)
            
            for sample, output in zip(batch, outputs):
                text = output.outputs[0].text
                label = self._extract_label(text)
                results.append(UtteranceResult(
                    dialog_id=sample.dialog_id,
                    turn_idx=sample.turn_idx,
                    binary_label=label,
                    raw_output=text,
                ))
            
            # 定期保存检查点
            if batch_num % save_every == 0 or batch_num == total_batches:
                print(f"  Progress: {batch_num}/{total_batches} batches, {len(results)}/{len(samples)} samples - Saving checkpoint...")
                if checkpoint_file:
                    self._save_checkpoint(results, batch_num, checkpoint_file)
            else:
                print(f"  Progress: {batch_num}/{total_batches} batches, {len(results)}/{len(samples)} samples")
        
        return results
    
    def _save_checkpoint(self, results: List[UtteranceResult], batch_num: int, checkpoint_file: str):
        """保存检查点"""
        checkpoint = {
            'batch_num': batch_num,
            'results': [asdict(r) for r in results]
        }
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, ensure_ascii=False, indent=2)
        print(f"    Checkpoint saved: {checkpoint_file} (batch {batch_num})")


def load_esconv_utterances(file_path: str) -> List[UtteranceSample]:
    """加载 ESConv 数据，返回每句 seeker 发言"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    samples = []
    
    for dialog in data:
        dialog_id = str(dialog.get("dialog_id", "unknown"))
        dialog_turns = dialog.get("dialog", [])
        
        # 遍历每句 seeker 发言
        for i, turn in enumerate(dialog_turns):
            if turn.get("speaker") != "seeker":
                continue
            
            # 构建上下文（该句之前的所有对话）
            context_lines = []
            for j in range(i):
                t = dialog_turns[j]
                speaker = "咨询师" if t.get("speaker") == "supporter" else "来访者"
                content = t.get("content", "").strip()
                if content:
                    context_lines.append(f"{speaker}：{content}")
            
            response = turn.get("content", "").strip()
            if not response:
                continue
            
            samples.append(UtteranceSample(
                dialog_id=dialog_id,
                turn_idx=i,
                context="\n".join(context_lines),
                response=response,
            ))
    
    return samples


def load_checkpoint(checkpoint_file: str) -> tuple:
    """加载检查点，返回 (batch_num, results)"""
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r', encoding='utf-8') as f:
            checkpoint = json.load(f)
        batch_num = checkpoint.get('batch_num', 0)
        results = [UtteranceResult(**r) for r in checkpoint.get('results', [])]
        print(f"Resuming from checkpoint: {checkpoint_file} (batch {batch_num}, {len(results)} samples)")
        return batch_num, results
    return 0, []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default="../ClientResistance-Model-Share/binary_share_model")
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--max-samples", type=int, default=None)
    parser.add_argument("--save-every", type=int, default=20, help="每多少批保存一次检查点")
    parser.add_argument("--checkpoint", type=str, default=None, help="检查点文件路径")
    args = parser.parse_args()
    
    # 默认检查点文件
    if args.checkpoint is None:
        args.checkpoint = args.output + ".checkpoint"
    
    # 加载数据
    print(f"Loading data from: {args.input}")
    samples = load_esconv_utterances(args.input)
    
    if args.max_samples:
        samples = samples[:args.max_samples]
    
    print(f"Total utterances to process: {len(samples)}")
    
    # 尝试加载检查点
    start_batch, existing_results = load_checkpoint(args.checkpoint)
    
    if existing_results:
        print(f"Found existing checkpoint with {len(existing_results)} results")
        print(f"Will resume from batch {start_batch}")
    
    # 初始化模型
    inferencer = RecapVLLMInference(args.model)
    
    # 推理（支持断点续传）
    print("Starting inference...")
    new_results = inferencer.infer_batch(
        samples, 
        batch_size=args.batch_size,
        start_batch=start_batch,
        save_every=args.save_every,
        checkpoint_file=args.checkpoint
    )
    
    # 合并结果
    all_results = existing_results + new_results
    
    # 保存最终结果
    output_data = []
    # 重建 sample 信息
    sample_idx = 0
    for result in all_results:
        # 找到对应的 sample
        if sample_idx < len(samples):
            sample = samples[sample_idx]
            output_data.append({
                "dialog_id": result.dialog_id,
                "turn_idx": result.turn_idx,
                "context": sample.context[:200] + "..." if len(sample.context) > 200 else sample.context,
                "response": sample.response,
                "binary_label": result.binary_label,
                "raw_output": result.raw_output[:100],
            })
            sample_idx += 1
    
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Results saved to: {args.output}")
    print(f"Total processed: {len(all_results)} samples")
    
    # 清理检查点文件
    if os.path.exists(args.checkpoint):
        os.remove(args.checkpoint)
        print(f"Checkpoint cleaned: {args.checkpoint}")
    
    # 统计
    binary_counts = {}
    for r in all_results:
        binary_counts[r.binary_label] = binary_counts.get(r.binary_label, 0) + 1
    print(f"Distribution: {binary_counts}")


if __name__ == "__main__":
    main()
