"""
用本地模型 (only_resistance_share_model) 对阻抗样本进行细粒度分类
GPU: CUDA_VISIBLE_DEVICES=4
"""

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "4"

import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from collections import Counter

# 加载数据
with open("results/esconv_labeled.json", "r", encoding="utf-8") as f:
    data = json.load(f)

resistance = [s for s in data if s.get("binary_label") == "阻抗"]
print(f"找到 {len(resistance)} 条阻抗样本")

# 模型路径
model_path = "/data5/zxj/llm_simu_client/ClientResistance-Model-Share/only_resistance_share_model"

# 简化提示词
SYSTEM_PROMPT = """你是一位专业心理咨询师。对来访者的阻抗行为进行分类。

可选类别：
争辩-挑战、争辩-贬低、
否认-责怪、否认-不认同、否认-找借口、否认-最小化、否认-悲观、否认-犹豫、否认-不愿改变、
回避-最小的回应、回避-界限设定、
忽视-不关注、忽视-岔开话题

请直接输出类别名称。"""

labels_map = {
    "争辩-挑战": "A1", "争辩-贬低": "A2",
    "否认-责怪": "B1", "否认-不认同": "B2", "否认-找借口": "B3",
    "否认-最小化": "B4", "否认-悲观": "B5", "否认-犹豫": "B6", "否认-不愿改变": "B7",
    "回避-最小的回应": "C1", "回避-界限设定": "C2",
    "忽视-不关注": "D1", "忽视-岔开话题": "D2",
}

print("加载模型...")
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    trust_remote_code=True,
)
print(f"模型加载完成，设备: {model.device}")

results = []
for i, sample in enumerate(resistance):
    context = sample.get("context", "")[:200]
    response = sample.get("response", "")
    
    # 构建 prompt
    prompt = f"{SYSTEM_PROMPT}\n\n对话上下文：\n{context}\n\n来访者回应：\n{response}\n\n阻抗类别："
    
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=15,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    
    result = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True).strip()
    fine_label = result.split("\n")[0][:15].strip()
    fine_category = labels_map.get(fine_label, "Unknown")
    
    results.append({
        "sample_id": sample.get("sample_id", ""),
        "binary_label": "阻抗",
        "fine_label": fine_label,
        "fine_category": fine_category,
        "response": response,
    })
    
    print(f"[{i+1:2d}/{len(resistance)}] {fine_label:12s} -> {fine_category}")

# 保存结果
with open("results/esconv_resistance_fine.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n结果已保存到 results/esconv_resistance_fine.json")
print("\n分布统计:")
for cat, count in Counter([r["fine_category"] for r in results]).most_common():
    print(f"  {cat}: {count}")
