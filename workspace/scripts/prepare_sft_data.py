"""
prepare_sft_data.py
将 inner_monologue_dataset.json 转换为 LLaMA-Factory 的 alpaca SFT 格式。

输出:
  - data/inner_monologue_sft.json    (SFT 格式)
  - data/inner_monologue_dpo.json    (DPO preference 格式，仅 resistance cases)

用法:
  python scripts/prepare_sft_data.py [--input results/inner_monologue_dataset.json]
"""

import json
import re
import argparse
import os
import random

SYSTEM_PROMPT = (
    "You are roleplaying as a therapy patient. "
    "When responding, first generate your inner monologue inside <internal>...</internal> tags, "
    "capturing your immediate thoughts and emotional state. "
    "Then give your actual spoken response."
)

def extract_internal(prediction: str) -> tuple[str, str]:
    """从 prediction 中分离 <internal> 和最终 response。"""
    m = re.search(r'<internal>(.*?)</internal>', prediction, re.DOTALL)
    if m:
        internal = m.group(1).strip()
        # response 在 </internal> 之后
        after = prediction[m.end():].strip()
        return internal, after
    return "", prediction.strip()



def convert_to_sft(data: list[dict]) -> tuple[list[dict], dict[int, dict]]:
    """
    转换为 alpaca SFT 格式。

    Returns:
        (sft_records, sft_map):
          sft_records — 按顺序的 SFT 列表
          sft_map     — {原始索引 -> SFT 记录}，用于 DPO 对齐
    """
    sft_records = []
    sft_map: dict[int, dict] = {}
    skipped = 0

    for orig_idx, record in enumerate(data):
        prediction = record.get("prediction", "").strip()
        ground_truth = record.get("ground_truth", "").strip()

        # 跳过空 prediction
        if not prediction or prediction == "[SKIPPED - API error]":
            skipped += 1
            continue

        internal, _ = extract_internal(prediction)

        # output = <internal>...</internal> + ground_truth (response)
        if internal:
            output = f"<internal>\n{internal}\n</internal>\n{ground_truth}"
        else:
            output = ground_truth

        # input = 对话历史（context字段已是注入 prompt 后的格式，需还原对话）
        # 从存储的 prompt context 中提取 dialogue_history 部分
        raw_context = record.get("context", [])
        if raw_context:
            stored_prompt = raw_context[0].get("content", "")
            m = re.search(r'# Dialogue.*?\n(.*)', stored_prompt, re.DOTALL)
            if m:
                dialogue_history = m.group(1).strip()
                dialogue_history = re.sub(
                    r'\s*Write the (inner monologue|immediate inner reaction) now:\s*$',
                    '', dialogue_history
                ).strip()
                # 去掉最后一行 "Patient: {ground_truth}"（那是 output，不是 input）
                lines = dialogue_history.split('\n')
                if lines and lines[-1].strip().startswith("Patient:") and ground_truth in lines[-1]:
                    lines = lines[:-1]
                input_text = "\n".join(lines).strip()
            else:
                input_text = ""
        else:
            input_text = ""

        entry = {
            "instruction": SYSTEM_PROMPT,
            "input": input_text,
            "output": output,
            # 保留元数据方便调试
            "_meta": {
                "transcript_id": record.get("transcript_id"),
                "turn_index": record.get("turn_index"),
                "behavior_type": record.get("behavior_type"),
                "resistance_parent": record.get("resistance_parent"),
                "resistance_category": record.get("resistance_category"),
                "gt_words": len(ground_truth.split()),
            }
        }
        sft_records.append(entry)
        sft_map[orig_idx] = entry

    print(f"SFT: 转换 {len(sft_records)} 条，跳过 {skipped} 条")
    return sft_records, sft_map


def build_dpo_pairs(data: list[dict], sft_map: dict[int, dict]) -> list[dict]:
    """
    构建 DPO 偏好对 (chosen / rejected)。

    Args:
        data: 原始 inner_monologue_dataset.json 的列表。
        sft_map: {原始索引 -> SFT 记录} 的映射，避免因跳过记录导致的 zip 错位 bug。

    策略：对 resistance cases，用真实数据作为 chosen；
    用去除 <internal> 的纯 response 作为 rejected（合成负样本）。
    后续可换成 SFT 模型生成的 rejected。
    """
    dpo_records = []

    for idx, record in enumerate(data):
        if record.get("behavior_type") != "resistance":
            continue
        if idx not in sft_map:
            continue  # 该记录在 SFT 时被跳过（API 错误等）

        sft = sft_map[idx]
        chosen = sft["output"]  # <internal>...</internal>\nresponse

        # 合成 rejected：去掉 <internal>，直接说 response（无推理过程）
        ground_truth = record.get("ground_truth", "")
        rejected = ground_truth  # 纯 response，无 internal

        dpo_records.append({
            "instruction": sft["instruction"],
            "input": sft["input"],
            "chosen": chosen,
            "rejected": rejected,
            "_meta": sft.get("_meta", {}),
        })

    print(f"DPO: 构建 {len(dpo_records)} 条偏好对（resistance cases）")
    return dpo_records


def register_to_dataset_info(llamafactory_dir: str):
    """在 LLaMA-Factory 的 data/dataset_info.json 中注册数据集。"""
    dataset_info_path = os.path.join(llamafactory_dir, "data", "dataset_info.json")
    if not os.path.exists(dataset_info_path):
        print(f"  [Warning] dataset_info.json 不存在: {dataset_info_path}")
        return

    with open(dataset_info_path, "r", encoding="utf-8") as f:
        info = json.load(f)

    # 注册 SFT 数据集
    info["inner_monologue_sft"] = {
        "file_name": "inner_monologue_sft.json",
        "formatting": "alpaca",
        "columns": {
            "prompt": "instruction",
            "query": "input",
            "response": "output"
        }
    }

    # 注册 DPO 数据集
    info["inner_monologue_dpo"] = {
        "file_name": "inner_monologue_dpo.json",
        "formatting": "alpaca",
        "ranking": True,
        "columns": {
            "prompt": "instruction",
            "query": "input",
            "chosen": "chosen",
            "rejected": "rejected"
        }
    }

    with open(dataset_info_path, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    print(f"  ✓ 已注册到 {dataset_info_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="results/inner_monologue_dataset.json")
    parser.add_argument("--output-dir", default="data", help="LLaMA-Factory 的 data 目录路径")
    parser.add_argument("--llamafactory-dir", default=None, help="LLaMA-Factory 根目录（用于注册 dataset_info）")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)

    # 读取原始数据
    print(f"读取 {args.input}...")
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"共 {len(data)} 条记录")

    # 转换格式
    sft_records, sft_map = convert_to_sft(data)
    dpo_records = build_dpo_pairs(data, sft_map)

    # 输出到指定目录
    os.makedirs(args.output_dir, exist_ok=True)

    sft_path = os.path.join(args.output_dir, "inner_monologue_sft.json")
    dpo_path = os.path.join(args.output_dir, "inner_monologue_dpo.json")

    with open(sft_path, "w", encoding="utf-8") as f:
        json.dump(sft_records, f, ensure_ascii=False, indent=2)
    print(f"✓ SFT 数据已保存: {sft_path}")

    with open(dpo_path, "w", encoding="utf-8") as f:
        json.dump(dpo_records, f, ensure_ascii=False, indent=2)
    print(f"✓ DPO 数据已保存: {dpo_path}")

    # 打印摘要
    bt_dist = {}
    for r in data:
        bt = r.get("behavior_type", "unknown")
        bt_dist[bt] = bt_dist.get(bt, 0) + 1

    print("\n=== 数据摘要 ===")
    print(f"SFT 总条数: {len(sft_records)}")
    print(f"DPO 对比对: {len(dpo_records)} (resistance cases)")
    print(f"behavior_type 分布: {bt_dist}")

    if args.llamafactory_dir:
        register_to_dataset_info(args.llamafactory_dir)


if __name__ == "__main__":
    main()
