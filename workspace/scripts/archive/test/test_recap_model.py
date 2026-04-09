"""
RECAP 模型测试脚本（内存优化版）
1. 验证模型加载和推理正常
2. 在 RECAP 数据上测试标注一致性
3. 在 ESConv 数据上测试零样本能力
"""

import sys
import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# 模型路径（相对于 workspace 目录）
BINARY_MODEL_PATH = "../ClientResistance-Model-Share/binary_share_model"
RESISTANCE_MODEL_PATH = "../ClientResistance-Model-Share/only_resistance_share_model"

# Prompt 模板（来自 example.py）
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
{context}

### 来访者回应：
{response}

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
{context}

### 来访者回应：
{response}

# 输出格式
请输出一行，直接输出阻抗行为类别，不要输出任何其他内容。
阻抗行为必须为"争辩-挑战""争辩-贬低""否认-责怪""否认-不认同""否认-找借口""否认-最小化""否认-悲观""否认-犹豫""否认-不愿改变""回避-最小的回应""回避-界限设定""忽视-不关注""忽视-岔开话题"中的一个。
"""


class RecapModel:
    def __init__(self, model_path, device="cuda:0"):
        """加载 RECAP 模型"""
        # 转换为绝对路径
        model_path = os.path.abspath(model_path)
        print(f"Loading model from: {model_path}")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model path not found: {model_path}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
        
        # 使用 4-bit 量化减少显存使用
        try:
            from transformers import BitsAndBytesConfig
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                quantization_config=quantization_config,
                device_map={"": device},
                local_files_only=True,
            )
            print("Using 4-bit quantization")
        except ImportError:
            # 如果没有 bitsandbytes，使用 bf16
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.bfloat16,
                device_map={"": device},
                local_files_only=True,
            )
        
        self.model.eval()
        print(f"Model loaded. Device: {self.model.device}")
    
    def generate(self, prompt, max_new_tokens=50):
        """生成回复"""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                temperature=None,
                top_p=None,
            )
        
        # 解码输出，去掉输入部分
        response = self.tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
        return response.strip()
    
    def unload(self):
        """卸载模型释放显存"""
        del self.model
        del self.tokenizer
        torch.cuda.empty_cache()


def format_dialogue(dialogue):
    """将对话格式化为文本"""
    lines = []
    for turn in dialogue[:-1]:  # 除了最后一句（目标发言）
        if turn["role"] == "user":
            lines.append(f"咨询师：{turn['content']}")
        else:
            lines.append(f"来访者：{turn['content']}")
    return "\n".join(lines)


def test_model_loading():
    """测试1：模型加载"""
    print("=" * 80)
    print("测试1：模型加载")
    print("=" * 80)
    
    try:
        binary_model = RecapModel(BINARY_MODEL_PATH, device="cuda:2")
        print("✅ 二分类模型加载成功")
        print(f"   显存使用: {torch.cuda.memory_allocated('cuda:2') / 1e9:.1f} GB")
        binary_model.unload()
        torch.cuda.empty_cache()
        print("   已卸载")
    except Exception as e:
        print(f"❌ 二分类模型加载失败: {e}")
        return False
    
    # 等待显存释放
    import time
    time.sleep(2)
    torch.cuda.empty_cache()
    
    try:
        resistance_model = RecapModel(RESISTANCE_MODEL_PATH, device="cuda:2")
        print("✅ 细分类模型加载成功")
        print(f"   显存使用: {torch.cuda.memory_allocated('cuda:2') / 1e9:.1f} GB")
        resistance_model.unload()
    except Exception as e:
        print(f"❌ 细分类模型加载失败: {e}")
        return False
    
    torch.cuda.empty_cache()
    return True


def test_recap_data(n_samples=10):
    """测试2：在 RECAP 数据上测试标注一致性"""
    print("\n" + "=" * 80)
    print(f"测试2：RECAP 数据标注一致性 (n={n_samples})")
    print("=" * 80)
    
    # 加载数据
    with open("dataset/RECAP.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 混合选择阻抗和非阻抗样本
    resistance_samples = [d for d in data if d.get("resistance_label", {}).get("has_resistance", False)]
    cooperation_samples = [d for d in data if not d.get("resistance_label", {}).get("has_resistance", False)]
    
    test_samples = resistance_samples[:n_samples//2] + cooperation_samples[:n_samples//2]
    
    results = []
    correct_binary = 0
    correct_fine = 0
    
    # 先加载二分类模型，处理所有样本
    print("\n加载二分类模型...")
    binary_model = RecapModel(BINARY_MODEL_PATH, device="cuda:0")
    
    binary_predictions = []
    for i, sample in enumerate(test_samples):
        label = sample.get("resistance_label", {})
        has_resistance = label.get("has_resistance", False)
        true_binary = "阻抗" if has_resistance else "合作"
        
        # 格式化对话
        context = format_dialogue(sample.get("dialogue", []))
        response = sample.get("target_utterance", "")
        
        # 二分类预测
        binary_prompt = BINARY_INSTRUCTION.format(context=context, response=response)
        pred_binary = binary_model.generate(binary_prompt, max_new_tokens=10)
        
        binary_match = true_binary in pred_binary or pred_binary in true_binary
        if binary_match:
            correct_binary += 1
        
        binary_predictions.append({
            "sample": sample,
            "true_binary": true_binary,
            "pred_binary": pred_binary,
            "binary_match": binary_match,
            "context": context,
            "response": response,
        })
        
        status = "✅" if binary_match else "❌"
        print(f"[{i+1}/{len(test_samples)}] {status} 二分类: {pred_binary} (真实: {true_binary})")
    
    binary_model.unload()
    
    # 再加载细分类模型，处理预测为阻抗的样本
    print("\n加载细分类模型...")
    resistance_model = RecapModel(RESISTANCE_MODEL_PATH, device="cuda:0")
    
    for i, pred in enumerate(binary_predictions):
        sample = pred["sample"]
        label = sample.get("resistance_label", {})
        has_resistance = label.get("has_resistance", False)
        true_fine = label.get("raw", "未知")
        
        # 细分类预测（仅对预测为阻抗的样本）
        pred_fine = "N/A"
        if "阻抗" in pred["pred_binary"]:
            resistance_prompt = RESISTANCE_INSTRUCTION.format(
                context=pred["context"], 
                response=pred["response"]
            )
            pred_fine = resistance_model.generate(resistance_prompt, max_new_tokens=20)
            
            fine_match = pred_fine in true_fine or true_fine in pred_fine
            if has_resistance and fine_match:
                correct_fine += 1
        else:
            fine_match = None
        
        results.append({
            "idx": sample.get("_recap_idx", i),
            "target": pred["response"][:50],
            "true_binary": pred["true_binary"],
            "pred_binary": pred["pred_binary"],
            "binary_match": pred["binary_match"],
            "true_fine": true_fine,
            "pred_fine": pred_fine,
            "fine_match": fine_match,
        })
        
        if has_resistance:
            fine_status = "✅" if fine_match else "❌"
            print(f"       {fine_status} 细分类: {pred_fine} (真实: {true_fine})")
    
    resistance_model.unload()
    
    # 统计
    print(f"\n二分类准确率: {correct_binary}/{len(test_samples)} = {correct_binary/len(test_samples)*100:.1f}%")
    resistance_count = sum(1 for r in results if r["true_binary"] == "阻抗")
    if resistance_count > 0:
        fine_correct = sum(1 for r in results if r["true_binary"] == "阻抗" and r["fine_match"])
        print(f"细分类准确率: {fine_correct}/{resistance_count} = {fine_correct/resistance_count*100:.1f}%")
    
    return results


def test_esconv_data(n_samples=5):
    """测试3：在 ESConv 数据上测试零样本能力"""
    print("\n" + "=" * 80)
    print(f"测试3：ESConv 数据零样本测试 (n={n_samples})")
    print("=" * 80)
    
    # 加载 ESConv 数据
    try:
        with open("dataset/ESConv.json", "r", encoding="utf-8") as f:
            esconv_data = json.load(f)
    except FileNotFoundError:
        print("❌ ESConv.json 不存在，跳过此测试")
        return None
    
    # 取前 n_samples 条对话
    test_samples = esconv_data[:n_samples]
    
    # 加载模型
    binary_model = RecapModel(BINARY_MODEL_PATH, device="cuda:0")
    resistance_model = RecapModel(RESISTANCE_MODEL_PATH, device="cuda:0")
    
    results = []
    
    for i, sample in enumerate(test_samples):
        # 获取对话
        dialog = sample.get("dialog", [])
        if not dialog:
            continue
        
        # 找到最后一句来访者发言
        last_client_idx = None
        for j, turn in enumerate(dialog):
            if turn.get("speaker") == "seeker":
                last_client_idx = j
        
        if last_client_idx is None or last_client_idx == 0:
            continue
        
        # 格式化上下文和回应
        context_lines = []
        for j in range(last_client_idx):
            turn = dialog[j]
            speaker = "咨询师" if turn.get("speaker") == "supporter" else "来访者"
            context_lines.append(f"{speaker}：{turn.get('content', '')}")
        context = "\n".join(context_lines)
        response = dialog[last_client_idx].get("content", "")
        
        # 预测
        binary_prompt = BINARY_INSTRUCTION.format(context=context, response=response)
        pred_binary = binary_model.generate(binary_prompt, max_new_tokens=10)
        
        pred_fine = "N/A"
        if "阻抗" in pred_binary:
            resistance_prompt = RESISTANCE_INSTRUCTION.format(context=context, response=response)
            pred_fine = resistance_model.generate(resistance_prompt, max_new_tokens=20)
        
        results.append({
            "dialog_id": sample.get("dialog_id", i),
            "target": response[:50],
            "pred_binary": pred_binary,
            "pred_fine": pred_fine,
        })
        
        print(f"[{i+1}] 二分类: {pred_binary}")
        if "阻抗" in pred_binary:
            print(f"    细分类: {pred_fine}")
        print(f"    来访者发言: {response[:60]}...")
        print()
    
    binary_model.unload()
    resistance_model.unload()
    
    return results


def main():
    # 检查 GPU
    if torch.cuda.is_available():
        print(f"GPU available: {torch.cuda.get_device_name(0)}")
        print(f"GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    else:
        print("⚠️ 没有GPU，推理可能会很慢")
    
    # 测试1：模型加载
    if not test_model_loading():
        print("\n模型加载失败，退出测试")
        return
    
    # 测试2：RECAP 数据标注一致性
    recap_results = test_recap_data(n_samples=10)
    
    # 测试3：ESConv 数据零样本测试
    esconv_results = test_esconv_data(n_samples=5)
    
    # 保存结果
    output = {
        "recap_results": recap_results,
        "esconv_results": esconv_results,
    }
    
    os.makedirs("results", exist_ok=True)
    with open("results/recap_model_test.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 测试结果已保存到: results/recap_model_test.json")


if __name__ == "__main__":
    main()
