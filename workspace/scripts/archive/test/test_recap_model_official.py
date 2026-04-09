"""
RECAP 模型测试脚本（使用官方 Prompt）
使用 ClientResistance-Model-Share/example.py 中的官方 prompt
"""

import sys
import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

# 模型路径
BINARY_MODEL_PATH = "../ClientResistance-Model-Share/binary_share_model"
RESISTANCE_MODEL_PATH = "../ClientResistance-Model-Share/only_resistance_share_model"

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


class RecapModel:
    """RECAP 官方模型封装"""
    def __init__(self, model_path, device="cuda:2"):
        model_path = os.path.abspath(model_path)
        print(f"Loading model from: {model_path}")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model path not found: {model_path}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
        
        # 4-bit 量化
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
    
    def generate(self, prompt, max_new_tokens=50):
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
    
    def unload(self):
        """卸载模型"""
        del self.model
        del self.tokenizer
        torch.cuda.empty_cache()


def format_dialogue(dialogue):
    """格式化对话为官方格式"""
    lines = []
    for turn in dialogue[:-1]:  # 去掉最后一句
        if turn["role"] == "user":
            lines.append(f"咨询师：{turn['content']}")
        else:
            lines.append(f"来访者：{turn['content']}")
    return "\n".join(lines)


def extract_first_line(text):
    """提取第一行作为结果"""
    return text.split('\n')[0].strip()


def test_recap_binary(model, n_samples=10):
    """测试二分类模型"""
    print("\n" + "=" * 80)
    print(f"测试：RECAP 二分类 (n={n_samples})")
    print("=" * 80)
    
    with open("dataset/RECAP.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 混合采样
    resistance = [d for d in data if d.get("resistance_label", {}).get("has_resistance", False)]
    cooperation = [d for d in data if not d.get("resistance_label", {}).get("has_resistance", False)]
    test_samples = resistance[:n_samples//2] + cooperation[:n_samples//2]
    
    correct = 0
    results = []
    
    for i, sample in enumerate(test_samples):
        label = sample.get("resistance_label", {})
        has_resistance = label.get("has_resistance", False)
        true_label = "阻抗" if has_resistance else "合作"
        
        # 使用官方 prompt 格式
        context = format_dialogue(sample.get("dialogue", []))
        response = sample.get("target_utterance", "")
        prompt = BINARY_INSTRUCTION.format(context, response)
        
        pred_raw = model.generate(prompt, max_new_tokens=10)
        pred = extract_first_line(pred_raw)
        
        match = true_label in pred or pred in true_label
        if match:
            correct += 1
        
        results.append({
            "idx": sample.get("_recap_idx", i),
            "target": response[:50],
            "true": true_label,
            "pred_raw": pred_raw[:100],
            "pred_clean": pred,
            "match": match,
        })
        
        status = "✅" if match else "❌"
        print(f"[{i+1}/{len(test_samples)}] {status} 预测: {pred} | 真实: {true_label}")
    
    accuracy = correct / len(test_samples) * 100
    print(f"\n准确率: {correct}/{len(test_samples)} = {accuracy:.1f}%")
    return results


def test_recap_fine_grained(binary_model, resistance_model, n_samples=5):
    """测试细分类模型（仅对预测为阻抗的样本）"""
    print("\n" + "=" * 80)
    print(f"测试：RECAP 细分类 (n={n_samples})")
    print("=" * 80)
    
    with open("dataset/RECAP.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 只取阻抗样本
    resistance_samples = [d for d in data if d.get("resistance_label", {}).get("has_resistance", False)]
    test_samples = resistance_samples[:n_samples]
    
    results = []
    
    for i, sample in enumerate(test_samples):
        context = format_dialogue(sample.get("dialogue", []))
        response = sample.get("target_utterance", "")
        true_label = sample.get("resistance_label", {}).get("raw", "未知")
        
        # 先用二分类确认是阻抗
        binary_prompt = BINARY_INSTRUCTION.format(context, response)
        binary_pred = extract_first_line(binary_model.generate(binary_prompt, max_new_tokens=10))
        
        if "阻抗" not in binary_pred:
            print(f"[{i+1}] 二分类预测非阻抗，跳过细分类")
            continue
        
        # 细分类
        fine_prompt = RESISTANCE_INSTRUCTION.format(context, response)
        fine_pred_raw = resistance_model.generate(fine_prompt, max_new_tokens=20)
        fine_pred = extract_first_line(fine_pred_raw)
        
        # 匹配判断
        match = fine_pred in true_label or true_label in fine_pred
        
        results.append({
            "idx": sample.get("_recap_idx", i),
            "target": response[:50],
            "true": true_label,
            "pred": fine_pred,
            "match": match,
        })
        
        status = "✅" if match else "❌"
        print(f"[{i+1}] {status} 预测: {fine_pred}")
        print(f"    真实: {true_label}")
    
    return results


def test_esconv(binary_model, n_samples=5):
    """测试 ESConv 数据"""
    print("\n" + "=" * 80)
    print(f"测试：ESConv 零样本 (n={n_samples})")
    print("=" * 80)
    
    try:
        with open("dataset/ESConv.json", "r", encoding="utf-8") as f:
            esconv_data = json.load(f)
    except FileNotFoundError:
        print("ESConv.json 不存在")
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
        
        prompt = BINARY_INSTRUCTION.format(context, response)
        pred = extract_first_line(binary_model.generate(prompt, max_new_tokens=10))
        
        results.append({
            "dialog_id": sample.get("dialog_id", i),
            "target": response[:50],
            "pred": pred,
        })
        
        print(f"[{i+1}] 预测: {pred}")
        print(f"    发言: {response[:60]}...")
    
    return results


def main():
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(2)}")
    
    # ========== 测试1：二分类模型 ==========
    print("\n" + "=" * 80)
    print("加载：RECAP 二分类模型")
    print("=" * 80)
    binary_model = RecapModel(BINARY_MODEL_PATH, device="cuda:2")
    
    # 测试 RECAP 二分类
    binary_results = test_recap_binary(binary_model, n_samples=10)
    
    # 测试 ESConv
    esconv_results = test_esconv(binary_model, n_samples=5)
    
    binary_model.unload()
    print("\n二分类模型已卸载")
    
    # ========== 测试2：细分类模型 ==========
    import time
    time.sleep(2)
    torch.cuda.empty_cache()
    
    print("\n" + "=" * 80)
    print("加载：RECAP 细分类模型")
    print("=" * 80)
    
    try:
        resistance_model = RecapModel(RESISTANCE_MODEL_PATH, device="cuda:2")
        
        # 重新加载二分类模型（需要同时用）
        print("\n重新加载二分类模型...")
        binary_model2 = RecapModel(BINARY_MODEL_PATH, device="cuda:2")
        
        # 测试细分类
        fine_results = test_recap_fine_grained(binary_model2, resistance_model, n_samples=5)
        
        binary_model2.unload()
        resistance_model.unload()
    except Exception as e:
        print(f"细分类模型加载失败: {e}")
        print("显存不足，跳过细分类测试")
        fine_results = None
    
    # 保存结果
    output = {
        "binary_results": binary_results,
        "esconv_results": esconv_results,
        "fine_results": fine_results,
    }
    
    os.makedirs("results", exist_ok=True)
    with open("results/recap_model_official_test.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 结果已保存: results/recap_model_official_test.json")


if __name__ == "__main__":
    main()
