"""
RECAP 模型简化测试脚本
只测试二分类模型（阻抗/合作），避免显存不足
"""

import sys
import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# 模型路径
BINARY_MODEL_PATH = "../ClientResistance-Model-Share/binary_share_model"

# Prompt 模板
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


class RecapBinaryModel:
    def __init__(self, model_path, device="cuda:2"):
        """加载 RECAP 二分类模型"""
        model_path = os.path.abspath(model_path)
        print(f"Loading model from: {model_path}")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model path not found: {model_path}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
        
        # 使用 4-bit 量化
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
        self.model.eval()
        print(f"Model loaded. Device: {self.model.device}")
    
    def generate(self, prompt, max_new_tokens=20):
        """生成回复"""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
            )
        
        response = self.tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
        return response.strip()


def format_dialogue(dialogue):
    """格式化对话"""
    lines = []
    for turn in dialogue[:-1]:
        if turn["role"] == "user":
            lines.append(f"咨询师：{turn['content']}")
        else:
            lines.append(f"来访者：{turn['content']}")
    return "\n".join(lines)


def test_recap_data(model, n_samples=10):
    """测试 RECAP 数据"""
    print("\n" + "=" * 80)
    print(f"测试 RECAP 数据标注一致性 (n={n_samples})")
    print("=" * 80)
    
    with open("dataset/RECAP.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 混合选择样本
    resistance_samples = [d for d in data if d.get("resistance_label", {}).get("has_resistance", False)]
    cooperation_samples = [d for d in data if not d.get("resistance_label", {}).get("has_resistance", False)]
    test_samples = resistance_samples[:n_samples//2] + cooperation_samples[:n_samples//2]
    
    correct = 0
    results = []
    
    for i, sample in enumerate(test_samples):
        label = sample.get("resistance_label", {})
        has_resistance = label.get("has_resistance", False)
        true_label = "阻抗" if has_resistance else "合作"
        
        context = format_dialogue(sample.get("dialogue", []))
        response = sample.get("target_utterance", "")
        
        prompt = BINARY_INSTRUCTION.format(context=context, response=response)
        pred = model.generate(prompt, max_new_tokens=10)
        
        match = true_label in pred or pred in true_label
        if match:
            correct += 1
        
        results.append({
            "idx": sample.get("_recap_idx", i),
            "target": response[:50],
            "true": true_label,
            "pred": pred,
            "match": match,
        })
        
        status = "✅" if match else "❌"
        print(f"[{i+1}/{len(test_samples)}] {status} 预测: {pred} | 真实: {true_label}")
        print(f"       发言: {response[:60]}...")
    
    print(f"\n准确率: {correct}/{len(test_samples)} = {correct/len(test_samples)*100:.1f}%")
    return results


def test_esconv_data(model, n_samples=5):
    """测试 ESConv 数据"""
    print("\n" + "=" * 80)
    print(f"测试 ESConv 数据零样本能力 (n={n_samples})")
    print("=" * 80)
    
    try:
        with open("dataset/ESConv.json", "r", encoding="utf-8") as f:
            esconv_data = json.load(f)
    except FileNotFoundError:
        print("❌ ESConv.json 不存在")
        return None
    
    test_samples = esconv_data[:n_samples]
    results = []
    
    for i, sample in enumerate(test_samples):
        dialog = sample.get("dialog", [])
        if not dialog:
            continue
        
        # 找最后一句来访者发言
        last_idx = None
        for j, turn in enumerate(dialog):
            if turn.get("speaker") == "seeker":
                last_idx = j
        
        if last_idx is None or last_idx == 0:
            continue
        
        # 格式化
        context_lines = []
        for j in range(last_idx):
            turn = dialog[j]
            speaker = "咨询师" if turn.get("speaker") == "supporter" else "来访者"
            context_lines.append(f"{speaker}：{turn.get('content', '')}")
        context = "\n".join(context_lines)
        response = dialog[last_idx].get("content", "")
        
        prompt = BINARY_INSTRUCTION.format(context=context, response=response)
        pred = model.generate(prompt, max_new_tokens=10)
        
        results.append({
            "dialog_id": sample.get("dialog_id", i),
            "target": response[:50],
            "pred": pred,
        })
        
        print(f"[{i+1}] 预测: {pred}")
        print(f"    发言: {response[:60]}...")
        print()
    
    return results


def main():
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(2)}")
        print(f"GPU memory: {torch.cuda.get_device_properties(2).total_memory / 1e9:.1f} GB")
    
    # 加载模型
    print("\n" + "=" * 80)
    print("加载 RECAP 二分类模型")
    print("=" * 80)
    model = RecapBinaryModel(BINARY_MODEL_PATH, device="cuda:2")
    print(f"✅ 模型加载成功，显存使用: {torch.cuda.memory_allocated('cuda:2') / 1e9:.1f} GB")
    
    # 测试 RECAP 数据
    recap_results = test_recap_data(model, n_samples=10)
    
    # 测试 ESConv 数据
    esconv_results = test_esconv_data(model, n_samples=5)
    
    # 保存结果
    output = {
        "recap_results": recap_results,
        "esconv_results": esconv_results,
    }
    
    os.makedirs("results", exist_ok=True)
    with open("results/recap_model_test_simple.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 结果已保存: results/recap_model_test_simple.json")


if __name__ == "__main__":
    main()
