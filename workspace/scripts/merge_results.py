"""
合并 ESConv 和 MESC 的细粒度标注结果
生成最终统计报告
"""

import json
from collections import Counter, defaultdict


def merge_esconv():
    """合并 ESConv 结果"""
    print("=" * 60)
    print("ESConv 结果合并")
    print("=" * 60)
    
    # 加载二分类结果
    with open("results/esconv_labeled_utterance.json", "r") as f:
        binary_data = json.load(f)
    
    # 创建索引
    binary_map = {s["sample_id"]: s for s in binary_data}
    
    # 加载阻抗细粒度结果
    res_results = []
    if os.path.exists("results/esconv_resistance_fine_full.json"):
        with open("results/esconv_resistance_fine_full.json", "r") as f:
            res_results = json.load(f)
        print(f"✓ 阻抗细粒度: {len(res_results)} 条")
    else:
        print("✗ 阻抗细粒度: 未找到")
    
    # 加载 CBS 结果
    cbs_results = []
    if os.path.exists("results/esconv_coop_cbs_full.json"):
        with open("results/esconv_coop_cbs_full.json", "r") as f:
            cbs_results = json.load(f)
        print(f"✓ CBS合作: {len(cbs_results)} 条")
    else:
        print("✗ CBS合作: 未找到")
    
    # 合并结果
    merged = []
    
    # 添加阻抗结果
    for r in res_results:
        sample_id = r["sample_id"]
        base = binary_map.get(sample_id, {})
        merged.append({
            "sample_id": sample_id,
            "dataset": "ESConv",
            "binary_label": "阻抗",
            "fine_category": r["fine_category"],
            "fine_label": r["fine_label"],
            "context": base.get("context", []),
            "response": r.get("response", base.get("target", "")),
        })
    
    # 添加 CBS 结果
    for r in cbs_results:
        sample_id = r["sample_id"]
        base = binary_map.get(sample_id, {})
        merged.append({
            "sample_id": sample_id,
            "dataset": "ESConv",
            "binary_label": "合作",
            "fine_category": r["cbs_type"],
            "fine_label": r["cbs_type"],
            "context": base.get("context", []),
            "response": r.get("response", base.get("target", "")),
        })
    
    # 保存合并结果
    output = "results/esconv_fine_merged.json"
    with open(output, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"\n合并完成: {output} ({len(merged)} 条)")
    
    return merged


def merge_mesc():
    """合并 MESC 结果"""
    print("\n" + "=" * 60)
    print("MESC 结果合并")
    print("=" * 60)
    
    # 加载二分类结果
    with open("results/mesc_labeled.json", "r") as f:
        binary_data = json.load(f)
    
    binary_map = {s["sample_id"]: s for s in binary_data}
    
    # 加载阻抗细粒度结果
    res_results = []
    if os.path.exists("results/mesc_resistance_fine.json"):
        with open("results/mesc_resistance_fine.json", "r") as f:
            res_results = json.load(f)
        print(f"✓ 阻抗细粒度: {len(res_results)} 条")
    else:
        print("✗ 阻抗细粒度: 未找到")
    
    # 加载 CBS 结果
    cbs_results = []
    if os.path.exists("results/mesc_coop_cbs.json"):
        with open("results/mesc_coop_cbs.json", "r") as f:
            cbs_results = json.load(f)
        print(f"✓ CBS合作: {len(cbs_results)} 条")
    else:
        print("✗ CBS合作: 未找到")
    
    # 合并
    merged = []
    for r in res_results:
        sample_id = r["sample_id"]
        base = binary_map.get(sample_id, {})
        merged.append({
            "sample_id": sample_id,
            "dataset": "MESC",
            "binary_label": "阻抗",
            "fine_category": r["fine_category"],
            "fine_label": r["fine_label"],
            "context": base.get("context", []),
            "response": r.get("response", base.get("target", "")),
        })
    
    for r in cbs_results:
        sample_id = r["sample_id"]
        base = binary_map.get(sample_id, {})
        merged.append({
            "sample_id": sample_id,
            "dataset": "MESC",
            "binary_label": "合作",
            "fine_category": r["cbs_type"],
            "fine_label": r["cbs_type"],
            "context": base.get("context", []),
            "response": r.get("response", base.get("target", "")),
        })
    
    output = "results/mesc_fine_merged.json"
    with open(output, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"\n合并完成: {output} ({len(merged)} 条)")
    
    return merged


def generate_report(esconv_data, mesc_data):
    """生成统计报告"""
    print("\n" + "=" * 60)
    print("最终统计报告")
    print("=" * 60)
    
    # 二元分类统计
    print("\n【二分类分布】")
    for name, data in [("ESConv", esconv_data), ("MESC", mesc_data)]:
        binary = Counter([d["binary_label"] for d in data])
        total = len(data)
        print(f"  {name}: 总计 {total}")
        for k, v in binary.items():
            print(f"    - {k}: {v} ({v/total*100:.1f}%)")
    
    # 细粒度统计
    print("\n【阻抗细粒度分布】")
    for name, data in [("ESConv", esconv_data), ("MESC", mesc_data)]:
        res_data = [d for d in data if d["binary_label"] == "阻抗"]
        if not res_data:
            continue
        print(f"  {name} ({len(res_data)} 条):")
        cats = Counter([d["fine_category"] for d in res_data])
        for cat, cnt in cats.most_common():
            print(f"    - {cat}: {cnt}")
    
    print("\n【CBS分布】")
    for name, data in [("ESConv", esconv_data), ("MESC", mesc_data)]:
        cbs_data = [d for d in data if d["binary_label"] == "合作"]
        if not cbs_data:
            continue
        print(f"  {name} ({len(cbs_data)} 条):")
        cats = Counter([d["fine_category"] for d in cbs_data])
        for cat, cnt in cats.most_common():
            print(f"    - {cat}: {cnt}")


def main():
    import os
    os.chdir("/data5/zxj/llm_simu_client/workspace")
    
    esconv_data = merge_esconv() if os.path.exists("results/esconv_resistance_fine_full.json") else []
    mesc_data = merge_mesc() if os.path.exists("results/mesc_resistance_fine.json") else []
    
    if esconv_data or mesc_data:
        generate_report(esconv_data, mesc_data)
    
    print("\n" + "=" * 60)
    print("全部完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
