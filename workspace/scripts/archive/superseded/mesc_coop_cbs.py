"""MESC 合作样本 CBS 分类"""
import os, json, time
from collections import Counter
from tqdm import tqdm

INPUT_FILE = "results/mesc_labeled.json"
OUTPUT_FILE = "results/mesc_coop_cbs.json"
SAVE_EVERY = 100

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

def main():
    from openai import OpenAI
    
    # 读取API key
    api_key = None
    try:
        with open(".env", "r") as f:
            for line in f:
                if line.startswith("QWEN_API_KEY="):
                    api_key = line.strip().split("=", 1)[1]
                    break
    except:
        pass
    if not api_key:
        raise ValueError("需要 QWEN_API_KEY")
    
    client = OpenAI(api_key=api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
    
    # 加载数据
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)
    
    # 筛选合作样本并添加ID
    coop_samples = [s for s in data if s.get("prediction") == "合作"]
    for i, s in enumerate(coop_samples):
        if "sample_id" not in s:
            s["sample_id"] = f"mesc_{i}"
    
    # 检查已有进度
    results = []
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            results = json.load(f)
        done_ids = {r["sample_id"] for r in results}
        coop_samples = [s for s in coop_samples if s["sample_id"] not in done_ids]
    
    print(f"总合作样本: 16828, 待处理: {len(coop_samples)}")
    
    for i, sample in enumerate(tqdm(coop_samples, desc="MESC CBS")):
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
            print(f"\nAPI Error: {e}")
            cbs = "Error"
        
        results.append({
            "sample_id": sample["sample_id"],
            "binary_label": "合作",
            "cbs_type": cbs,
            "response": tgt,
        })
        
        if (i + 1) % SAVE_EVERY == 0:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"  已保存: {len(results)}")
        
        time.sleep(0.3)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 完成! 总计: {len(results)} 条")
    cats = Counter([r["cbs_type"] for r in results])
    print("分布:")
    for k, v in cats.most_common():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
