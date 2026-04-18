"""
MESC 数据集完整细粒度标注流程
- 步骤1: 阻抗样本 → PsyFIRE 13类 (GPU 4)
- 步骤2: 合作样本 → CBS 2-8类 (API)
"""

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "4"

import json
import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from collections import Counter
from tqdm import tqdm

from psychfire_resistance_fine_prompt import build_resistance_fine_user_prompt

# ============ 配置 ============
INPUT_FILE = "results/mesc_labeled.json"
RES_OUTPUT = "results/mesc_resistance_fine.json"
CBS_OUTPUT = "results/mesc_coop_cbs.json"
MODEL_PATH = "/data5/zxj/llm_simu_client/ClientResistance-Model-Share/only_resistance_share_model"
SAVE_EVERY = 100

# PsyFIRE 标签映射 (支持中文和代码)
LABELS_MAP = {
    # 中文 → 代码
    "争辩-挑战": "A1", "争辩-贬低": "A2",
    "否认-责怪": "B1", "否认-不认同": "B2", "否认-找借口": "B3",
    "否认-最小化": "B4", "否认-悲观": "B5", "否认-犹豫": "B6", "否认-不愿改变": "B7",
    "回避-最小的回应": "C1", "回避-界限设定": "C2",
    "忽视-不关注": "D1", "忽视-岔开话题": "D2",
    # 代码 → 代码 (直接输出代码的情况)
    "A1": "A1", "A2": "A2",
    "B1": "B1", "B2": "B2", "B3": "B3", "B4": "B4", "B5": "B5", "B6": "B6", "B7": "B7",
    "C1": "C1", "C2": "C2",
    "D1": "D1", "D2": "D2",
}

# CBS 提示词
CBS_PROMPT = """你是心理咨询标注专家。对来访者话语进行CBS 2-8分类。

类别: CBS2-认同, CBS3-请求, CBS4-叙述, CBS5-认知探索, CBS6-情感探索, CBS7-领悟, CBS8-改变
优先级: 改变>领悟>请求>情感探索>认知探索>认同>叙述

输出JSON: {"cbs_type": "CBS2-认同"}"""


def format_context(ctx, max_turns=2):
    if isinstance(ctx, str):
        return ctx
    if not ctx:
        return ""
    lines = []
    for turn in ctx[-max_turns:]:
        spk = turn.get("speaker", turn.get("role", ""))
        txt = turn.get("content", turn.get("text", "")).strip()
        if spk and txt:
            spk_cn = "咨询师" if spk in ["therapist", "supporter", "user"] else "来访者"
            lines.append(f"{spk_cn}: {txt}")
    return "\n".join(lines)


def classify_resistance(model, tokenizer, samples):
    """阻抗样本分类"""
    results = []
    for i, sample in enumerate(tqdm(samples, desc="Resistance")):
        ctx = format_context(sample.get("context", []))
        tgt = sample.get("target", "")
        
        prompt = build_resistance_fine_user_prompt(ctx, tgt)
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1536)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=15, do_sample=False, 
                                     pad_token_id=tokenizer.eos_token_id)
        
        result = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True).strip()
        raw = result.split("\n")[0].strip()
        if "#" in raw:
            raw = raw.split("#")[0].strip()
        label = raw[:20].strip()
        cat = LABELS_MAP.get(label, "Unknown")
        # 如果映射失败，尝试提取代码
        if cat == "Unknown":
            for code in ["A1","A2","B1","B2","B3","B4","B5","B6","B7","C1","C2","D1","D2"]:
                if code in label:
                    cat = code
                    break
        
        results.append({
            "sample_id": sample["sample_id"],
            "binary_label": "阻抗",
            "fine_label": label,
            "fine_category": cat,
            "response": tgt,
        })
        
        if (i + 1) % SAVE_EVERY == 0:
            with open(RES_OUTPUT, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"  Saved: {len(results)}")
    
    with open(RES_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return results


def classify_cbs_api(samples):
    """合作样本 CBS 分类"""
    from openai import OpenAI
    
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("请设置 DASHSCOPE_API_KEY")
    
    client = OpenAI(api_key=api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
    
    results = []
    for i, sample in enumerate(tqdm(samples, desc="CBS")):
        ctx = format_context(sample.get("context", []))
        tgt = sample.get("target", "")
        
        msg = f"对话:\n{ctx}\n\n来访者: {tgt}\n\n请输出CBS分类JSON。"
        
        try:
            resp = client.chat.completions.create(
                model="qwen-turbo",
                messages=[{"role": "system", "content": CBS_PROMPT}, 
                          {"role": "user", "content": msg}],
                temperature=0.1, max_tokens=50,
            )
            content = resp.choices[0].message.content.strip()
            try:
                cbs = json.loads(content).get("cbs_type", "Unknown")
            except:
                cbs = "Unknown"
        except Exception as e:
            print(f"API Error: {e}")
            cbs = "Error"
        
        results.append({
            "sample_id": sample["sample_id"],
            "binary_label": "合作",
            "cbs_type": cbs,
            "response": tgt,
        })
        
        if (i + 1) % SAVE_EVERY == 0:
            with open(CBS_OUTPUT, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"  Saved: {len(results)}")
        
        time.sleep(0.3)
    
    with open(CBS_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return results


def main():
    print(f"使用 GPU: {os.environ.get('CUDA_VISIBLE_DEVICES')}")
    
    # 加载数据
    print(f"\n加载: {INPUT_FILE}")
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)
    
    # 按标签分组，添加sample_id
    for i, s in enumerate(data):
        if "sample_id" not in s:
            s["sample_id"] = f"mesc_{i}"
    
    res_samples = [s for s in data if s.get("prediction") == "阻抗"]
    coop_samples = [s for s in data if s.get("prediction") == "合作"]
    print(f"总: {len(data)}, 阻抗: {len(res_samples)}, 合作: {len(coop_samples)}")
    
    # ============ 步骤1: 阻抗分类 ============
    if res_samples and not os.path.exists(RES_OUTPUT):
        print(f"\n{'='*40}")
        print("步骤1: 阻抗样本 13类分类")
        print(f"{'='*40}")
        
        print(f"加载模型...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_PATH, torch_dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
        print(f"模型加载: {model.device}")
        
        res_results = classify_resistance(model, tokenizer, res_samples)
        
        print(f"\n阻抗分布:")
        for cat, cnt in Counter([r["fine_category"] for r in res_results]).most_common():
            print(f"  {cat}: {cnt}")
    elif os.path.exists(RES_OUTPUT):
        print(f"\n✓ 阻抗结果已存在: {RES_OUTPUT}")
    
    # ============ 步骤2: CBS分类 ============
    if coop_samples and not os.path.exists(CBS_OUTPUT):
        print(f"\n{'='*40}")
        print("步骤2: 合作样本 CBS 2-8分类")
        print(f"{'='*40}")
        
        cbs_results = classify_cbs_api(coop_samples)
        
        print(f"\nCBS分布:")
        for cat, cnt in Counter([r["cbs_type"] for r in cbs_results]).most_common():
            print(f"  {cat}: {cnt}")
    elif os.path.exists(CBS_OUTPUT):
        print(f"\n✓ CBS结果已存在: {CBS_OUTPUT}")
    
    print(f"\n{'='*40}")
    print("全部完成!")
    print(f"{'='*40}")


if __name__ == "__main__":
    main()
