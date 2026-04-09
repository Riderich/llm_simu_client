"""
RECAP 模型 vLLM 推理脚本
使用 vLLM 进行高效的批量推理

使用方法:
    # Dry run (不加载模型，测试代码)
    python recap_vllm_inference.py --dry-run
    
    # 实际推理
    python recap_vllm_inference.py --input dataset/ESConv.json --output results/esconv_labeled.json
"""

import os
import sys

# 必须在导入 torch/vllm 之前设置 GPU
# 从命令行参数解析 GPU ID
target_gpu = "4"  # 默认使用 GPU 4
if len(sys.argv) > 1:
    for i, arg in enumerate(sys.argv):
        if arg == "--gpu" and i + 1 < len(sys.argv):
            target_gpu = sys.argv[i + 1]
            break

# 强制设置 CUDA 可见设备（必须在任何 CUDA 操作之前）
os.environ["CUDA_VISIBLE_DEVICES"] = target_gpu
os.environ["VLLM_WORKER_MULTIPROC_METHOD"] = "spawn"
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"

print(f"Setting CUDA_VISIBLE_DEVICES={target_gpu}", flush=True)

# 验证设置
import torch
print(f"PyTorch sees {torch.cuda.device_count()} GPU(s)")
if torch.cuda.is_available():
    print(f"Device 0: {torch.cuda.get_device_name(0)}")
import json
import argparse
from typing import List, Dict, Optional
from dataclasses import dataclass

# ============ 官方 Prompt（来自 example.py）============

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

RESISTANCE_INSTRUCTION = """# 角色：
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
阻抗行为必须为"争辩-挑战""争辩-贬低""否认-责怪""否认-不认同""否认-找借口""否认-最小化""否认-悲观""否认-犹豫""否认-不愿改变""回避-最小的回应""回避-界限设定""忽视-不关注""忽视-岔开话题"中的一个。
"""

# =====================================================


@dataclass
class InferenceSample:
    """推理样本"""
    sample_id: str
    context: str
    response: str
    metadata: Optional[Dict] = None


@dataclass
class InferenceResult:
    """推理结果"""
    sample_id: str
    binary_label: str
    fine_label: Optional[str] = None
    raw_output_binary: str = ""
    raw_output_fine: str = ""


class RecapVLLMInference:
    """
    RECAP vLLM 推理器
    
    支持两种模式：
    1. 二分类（阻抗/合作）
    2. 细分类（13类阻抗）
    """
    
    def __init__(
        self,
        binary_model_path: str,
        resistance_model_path: Optional[str] = None,
        tensor_parallel_size: int = 1,
        gpu_memory_utilization: float = 0.9,
        max_model_len: int = 4096,
    ):
        """
        初始化 vLLM 推理器
        
        Args:
            binary_model_path: 二分类模型路径
            resistance_model_path: 细分类模型路径（可选）
            tensor_parallel_size: 张量并行数（多卡时使用）
            gpu_memory_utilization: GPU 显存利用率
            max_model_len: 最大序列长度
        """
        self.binary_model_path = binary_model_path
        self.resistance_model_path = resistance_model_path
        
        # 延迟导入 vLLM（避免在 dry run 时导入失败）
        try:
            from vllm import LLM, SamplingParams
            self.vllm_available = True
        except ImportError:
            print("⚠️  vLLM not installed. Running in mock mode.")
            self.vllm_available = False
            return
        
        print(f"Loading binary model from: {binary_model_path}")
        # 强制 vLLM 使用 CUDA_VISIBLE_DEVICES 设置的 GPU
        import torch
        torch.cuda.set_device(0)  # CUDA_VISIBLE_DEVICES 设置后，0 就是目标 GPU
        
        # 强制使用当前可见的 GPU
        import torch
        visible_devices = os.environ.get("CUDA_VISIBLE_DEVICES", "")
        if visible_devices:
            print(f"  CUDA_VISIBLE_DEVICES={visible_devices}")
            print(f"  PyTorch sees GPUs: {torch.cuda.device_count()}")
        
        # 尝试直接使用单 GPU 模式，避免分布式 executor
        self.binary_llm = LLM(
            model=binary_model_path,
            tensor_parallel_size=1,  # 强制单卡
            gpu_memory_utilization=0.40,  # 降低显存使用
            max_model_len=1024,  # 降低最大长度
            dtype="auto",
            load_format="auto",
            trust_remote_code=True,
            enforce_eager=True,
            device="cuda:0",  # 明确指定 cuda:0 (在CUDA_VISIBLE_DEVICES后就是目标GPU)
        )
        
        if resistance_model_path and os.path.exists(resistance_model_path):
            print(f"Loading resistance model from: {resistance_model_path}")
            self.resistance_llm = LLM(
                model=resistance_model_path,
                tensor_parallel_size=1,
                gpu_memory_utilization=0.40,
                max_model_len=1024,
                dtype="auto",
                load_format="auto",
                trust_remote_code=True,
                enforce_eager=True,
                device="cuda:0",
            )
        else:
            self.resistance_llm = None
        
        # 采样参数（确定性输出）
        self.sampling_params = SamplingParams(
            temperature=0,  # 贪婪解码
            max_tokens=50,  # 输出长度限制
        )
    
    def _create_binary_prompts(self, samples: List[InferenceSample]) -> List[str]:
        """创建二分类 prompts"""
        return [
            BINARY_INSTRUCTION.format(s.context, s.response)
            for s in samples
        ]
    
    def _create_fine_prompts(self, samples: List[InferenceSample]) -> List[str]:
        """创建细分类 prompts"""
        return [
            RESISTANCE_INSTRUCTION.format(s.context, s.response)
            for s in samples
        ]
    
    def _extract_label(self, text: str, is_binary: bool = True) -> str:
        """从模型输出中提取标签"""
        first_line = text.split('\n')[0].strip()
        
        if is_binary:
            # 二分类：提取"阻抗"或"合作"
            if "阻抗" in first_line:
                return "阻抗"
            elif "合作" in first_line:
                return "合作"
            return first_line[:20]  # 兜底
        else:
            # 细分类：提取 13 类之一
            valid_labels = [
                "争辩-挑战", "争辩-贬低",
                "否认-责怪", "否认-不认同", "否认-找借口", "否认-最小化", 
                "否认-悲观", "否认-犹豫", "否认-不愿改变",
                "回避-最小的回应", "回避-界限设定",
                "忽视-不关注", "忽视-岔开话题"
            ]
            for label in valid_labels:
                if label in first_line:
                    return label
            return first_line[:20]  # 兜底
    
    def infer_batch(
        self,
        samples: List[InferenceSample],
        batch_size: int = 32,
        use_fine_grained: bool = True,
    ) -> List[InferenceResult]:
        """
        批量推理
        
        Args:
            samples: 样本列表
            batch_size: 批大小
            use_fine_grained: 是否进行细分类
        
        Returns:
            推理结果列表
        """
        if not self.vllm_available:
            # Mock 模式：返回随机结果（用于 dry run）
            import random
            return [
                InferenceResult(
                    sample_id=s.sample_id,
                    binary_label=random.choice(["阻抗", "合作"]),
                    fine_label=random.choice(["否认-不认同", "争辩-挑战"]) if use_fine_grained else None,
                )
                for s in samples
            ]
        
        results = []
        
        # 分批处理
        for i in range(0, len(samples), batch_size):
            batch = samples[i:i + batch_size]
            print(f"Processing batch {i//batch_size + 1}/{(len(samples)-1)//batch_size + 1} (size={len(batch)})")
            
            # 1. 二分类推理
            binary_prompts = self._create_binary_prompts(batch)
            binary_outputs = self.binary_llm.generate(binary_prompts, self.sampling_params)
            binary_texts = [o.outputs[0].text for o in binary_outputs]
            
            # 2. 细分类推理（如果需要且预测为阻抗）
            fine_texts = [None] * len(batch)
            if use_fine_grained and self.resistance_llm:
                # 找出预测为阻抗的样本
                resistance_indices = [
                    j for j, text in enumerate(binary_texts)
                    if "阻抗" in self._extract_label(text, is_binary=True)
                ]
                
                if resistance_indices:
                    resistance_samples = [batch[j] for j in resistance_indices]
                    fine_prompts = self._create_fine_prompts(resistance_samples)
                    fine_outputs = self.resistance_llm.generate(fine_prompts, self.sampling_params)
                    
                    for idx, output in zip(resistance_indices, fine_outputs):
                        fine_texts[idx] = output.outputs[0].text
            
            # 3. 组装结果
            for j, sample in enumerate(batch):
                binary_label = self._extract_label(binary_texts[j], is_binary=True)
                fine_label = self._extract_label(fine_texts[j], is_binary=False) if fine_texts[j] else None
                
                results.append(InferenceResult(
                    sample_id=sample.sample_id,
                    binary_label=binary_label,
                    fine_label=fine_label,
                    raw_output_binary=binary_texts[j],
                    raw_output_fine=fine_texts[j] or "",
                ))
        
        return results


# ============ 数据加载器 ============

class RecapDataLoader:
    """RECAP 数据加载器"""
    
    @staticmethod
    def load_recap(file_path: str, max_samples: Optional[int] = None) -> List[InferenceSample]:
        """加载 RECAP 格式数据"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if max_samples:
            data = data[:max_samples]
        
        samples = []
        for item in data:
            dialogue = item.get("dialogue", [])
            context_lines = []
            for turn in dialogue[:-1]:
                if turn["role"] == "user":
                    context_lines.append(f"咨询师：{turn['content']}")
                else:
                    context_lines.append(f"来访者：{turn['content']}")
            
            samples.append(InferenceSample(
                sample_id=str(item.get("_recap_idx", len(samples))),
                context="\n".join(context_lines),
                response=item.get("target_utterance", ""),
                metadata=item,
            ))
        
        return samples
    
    @staticmethod
    def load_esconv(file_path: str, max_samples: Optional[int] = None) -> List[InferenceSample]:
        """加载 ESConv 格式数据（Utterance 级别 - 每句 seeker 都生成样本）"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if max_samples:
            data = data[:max_samples]
        
        samples = []
        for item in data:
            dialog = item.get("dialog", [])
            dialog_id = item.get("dialog_id") or item.get("problem") or str(len(samples))
            
            # 遍历所有 turn，为每句 seeker 生成样本
            for j, turn in enumerate(dialog):
                if turn.get("speaker") != "seeker":
                    continue
                
                # 跳过第一句（没有上下文）
                if j == 0:
                    continue
                
                # 格式化上下文（当前 turn 之前的所有对话）
                context_lines = []
                for k in range(j):
                    t = dialog[k]
                    speaker = "咨询师" if t.get("speaker") == "supporter" else "来访者"
                    content = t.get("content", "") or t.get("text", "")
                    context_lines.append(f"{speaker}：{content}")
                
                response = turn.get("content", "") or turn.get("text", "")
                
                samples.append(InferenceSample(
                    sample_id=f"{dialog_id}_{j}",  # 唯一 ID: dialog_id_turn_idx
                    context="\n".join(context_lines),
                    response=response,
                    metadata={
                        "dialog_id": dialog_id,
                        "turn_idx": j,
                        "original_data": item,
                    },
                ))
        
        return samples
    
    @staticmethod
    def load_existing_results(file_path: str) -> set:
        """加载已有结果，返回已存在的 sample_id 集合"""
        if not os.path.exists(file_path):
            return set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            existing_ids = {item.get("sample_id") for item in data if item.get("sample_id")}
            print(f"  发现已有结果: {len(existing_ids)} 条")
            return existing_ids
        except:
            return set()


# ============ 主函数 ============

def main():
    parser = argparse.ArgumentParser(description="RECAP vLLM 推理")
    parser.add_argument("--input", type=str, help="输入数据文件")
    parser.add_argument("--output", type=str, help="输出结果文件")
    parser.add_argument("--data-format", type=str, choices=["recap", "esconv"], default="recap")
    parser.add_argument("--binary-model", type=str, default="/data5/zxj/llm_simu_client/ClientResistance-Model-Share/binary_share_model")
    parser.add_argument("--resistance-model", type=str, default="/data5/zxj/llm_simu_client/ClientResistance-Model-Share/only_resistance_share_model")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--max-samples", type=int, default=None)
    parser.add_argument("--no-fine-grained", action="store_true", help="不进行细分类")
    parser.add_argument("--dry-run", action="store_true", help="Dry run 模式（不加载模型）")
    parser.add_argument("--tp-size", type=int, default=1, help="张量并行大小")
    parser.add_argument("--gpu", type=int, default=2, help="使用的 GPU ID")
    args = parser.parse_args()
    
    # 设置 GPU
    os.environ["CUDA_VISIBLE_DEVICES"] = str(args.gpu)
    
    # Dry run 模式
    if args.dry_run:
        print("=" * 80)
        print("DRY RUN MODE (不加载模型)")
        print("=" * 80)
        
        # 创建 mock 推理器
        inferencer = RecapVLLMInference(
            binary_model_path=args.binary_model,
            resistance_model_path=None if args.no_fine_grained else args.resistance_model,
        )
        
        # 创建测试样本
        test_samples = [
            InferenceSample(
                sample_id="test_0",
                context="咨询师：你好，最近感觉怎么样？\n来访者：还是老样子。",
                response="我不想谈这个。",
            ),
            InferenceSample(
                sample_id="test_1",
                context="咨询师：我们可以试试这个方法。\n来访者：好的。",
                response="我觉得可以试试。",
            ),
        ]
        
        print(f"\n测试样本数: {len(test_samples)}")
        print(f"批大小: {args.batch_size}")
        print(f"是否细分类: {not args.no_fine_grained}")
        
        # Mock 推理
        results = inferencer.infer_batch(
            test_samples,
            batch_size=args.batch_size,
            use_fine_grained=not args.no_fine_grained,
        )
        
        print("\nMock 推理结果:")
        for r in results:
            print(f"  {r.sample_id}: {r.binary_label}", end="")
            if r.fine_label:
                print(f" / {r.fine_label}")
            else:
                print()
        
        print("\n✅ Dry run 完成！代码结构验证通过。")
        print(f"\n实际使用时运行:")
        print(f"  python {sys.argv[0]} --input dataset/ESConv.json --output results/esconv_labeled.json")
        return
    
    # 实际推理模式
    if not args.input:
        print("Error: --input is required (or use --dry-run)")
        return
    
    # 加载已有结果（断点续传）
    print(f"Checking existing results: {args.output}")
    existing_ids = RecapDataLoader.load_existing_results(args.output)
    
    # 加载数据
    print(f"Loading data from: {args.input}")
    if args.data_format == "recap":
        all_samples = RecapDataLoader.load_recap(args.input, args.max_samples)
    else:
        all_samples = RecapDataLoader.load_esconv(args.input, args.max_samples)
    
    # 过滤已存在的样本
    samples = [s for s in all_samples if s.sample_id not in existing_ids]
    
    print(f"Total samples: {len(all_samples)}")
    print(f"Already processed: {len(existing_ids)}")
    print(f"Remaining to process: {len(samples)}")
    
    if not samples:
        print("\n✅ All samples already processed!")
        return
    
    # 初始化推理器
    inferencer = RecapVLLMInference(
        binary_model_path=args.binary_model,
        resistance_model_path=None if args.no_fine_grained else args.resistance_model,
        tensor_parallel_size=args.tp_size,
    )
    
    # 加载已有结果数据
    output_data = []
    if existing_ids and os.path.exists(args.output):
        with open(args.output, 'r', encoding='utf-8') as f:
            output_data = json.load(f)
    
    # 分批推理并定期保存
    SAVE_EVERY = 50  # 每50条保存一次
    total_processed = len(existing_ids)
    
    print(f"\nStarting inference (saving every {SAVE_EVERY} samples)...")
    
    for i in range(0, len(samples), args.batch_size):
        batch = samples[i:i + args.batch_size]
        batch_num = i // args.batch_size + 1
        total_batches = (len(samples) - 1) // args.batch_size + 1
        
        print(f"\nBatch {batch_num}/{total_batches} (size={len(batch)})")
        
        # 推理
        results = inferencer.infer_batch(
            batch,
            batch_size=args.batch_size,
            use_fine_grained=not args.no_fine_grained,
        )
        
        # 组装结果
        for sample, result in zip(batch, results):
            item = {
                "sample_id": result.sample_id,
                "context": sample.context[:200] + "..." if len(sample.context) > 200 else sample.context,
                "response": sample.response,
                "binary_label": result.binary_label,
                "fine_label": result.fine_label,
            }
            if sample.metadata:
                item["metadata"] = sample.metadata
            output_data.append(item)
            total_processed += 1
        
        # 定期保存
        if total_processed % SAVE_EVERY < args.batch_size or batch_num == total_batches:
            os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            print(f"  💾 Saved ({total_processed} total)")
    
    print(f"\n✅ 结果已保存: {args.output}")
    print(f"   Total processed: {total_processed}")
    
    # 统计
    binary_counts = {}
    fine_counts = {}
    for item in output_data:
        binary_counts[item["binary_label"]] = binary_counts.get(item["binary_label"], 0) + 1
        if item.get("fine_label"):
            fine_counts[item["fine_label"]] = fine_counts.get(item["fine_label"], 0) + 1
    
    print("\n统计:")
    print(f"  二分类分布: {binary_counts}")
    if fine_counts:
        print(f"  细分类分布: {fine_counts}")


if __name__ == "__main__":
    main()
