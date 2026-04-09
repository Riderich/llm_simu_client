"""
process_recap.py
将 ClientResistance_decrypted.json 解析、规范化并保存为结构化 JSON 格式。
输出文件：dataset/ClientResistance_processed.json

输出字段约定：
- dialogue: 完整对话（包含最后一句来访者 target_utterance）
"""

import json
import os


# 原始中文标签 → (parent, category) 英文映射
LABEL_MAP = {
    # 争辩 Arguing
    "争辩-挑战":     ("Arguing",      "Challenging"),
    "争辩-贬低":     ("Arguing",      "Discounting"),

    # 否认 Denying
    "否认-责怪":     ("Denying",      "Blaming"),
    "否认-不认同":   ("Denying",      "Disagreeing"),
    "否认-找借口":   ("Denying",      "Excusing"),
    "否认-最小化":   ("Denying",      "Minimizing"),
    "否认-悲观":     ("Denying",      "Pessimism"),
    "否认-犹豫":     ("Denying",      "Reluctance"),
    "否认-不愿改变": ("Denying",      "Unwillingness"),

    # 回避 Avoiding
    "回避-最小的回应": ("Avoiding",   "Minimum Talk"),
    "回避-界限设定":   ("Avoiding",   "Limit Setting"),

    # 忽视 Ignoring
    "忽视-岔开话题": ("Ignoring",     "Topic Shift"),
    "忽视-不关注":   ("Ignoring",     "Inattention"),

    # 合作-未阻抗 No Resistance
    "合作-未阻抗":   ("No Resistance", "Cooperative"),
}


def parse_turns(text: str):
    """将原始对话文本解析为 [{role, content}] 轮次列表。"""
    turns = []
    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("来访者：") or line.startswith("来访者:"):
            turns.append({"role": "assistant", "content": line[4:].strip()})
        elif line.startswith("咨询师：") or line.startswith("咨询师:"):
            turns.append({"role": "user", "content": line[4:].strip()})
        else:
            # 无前缀的续行，拼接到上一轮
            if turns:
                turns[-1]["content"] += " " + line
    return turns


def process(raw_path: str, out_path: str):
    with open(raw_path, encoding="utf-8") as f:
        raw_data = json.load(f)

    processed = []
    skipped = 0

    for item in raw_data:
        text = item.get("text", "").strip()
        raw_label = item.get("label", ["合作-未阻抗"])[0]

        turns = parse_turns(text)

        if not turns:
            skipped += 1
            continue

        # 最后一轮必须是来访者（assistant）
        if turns[-1]["role"] != "assistant":
            skipped += 1
            continue

        target_utterance = turns[-1]["content"]
        no_context = len(turns) <= 1

        # 标签映射
        if raw_label in LABEL_MAP:
            parent, category = LABEL_MAP[raw_label]
        else:
            print(f"[WARN] Unknown label: {raw_label}, defaulting to Cooperative")
            parent, category = "No Resistance", "Cooperative"

        has_resistance = parent != "No Resistance"

        record = {
            "source": "RECAP",
            "dialogue": turns,
            "target_utterance": target_utterance,
            "no_context": no_context,
            "resistance_label": {
                "raw": raw_label,
                "parent": parent,
                "category": category,
                "has_resistance": has_resistance,
            },
        }
        processed.append(record)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(processed, f, ensure_ascii=False, indent=2)

    print(f"Processed {len(processed)} samples ({skipped} skipped).")
    no_ctx_count = sum(1 for r in processed if r["no_context"])
    print(f"No-context samples (marked): {no_ctx_count}")


if __name__ == "__main__":
    # script 在 workspace/scripts/ 下，向上两级到项目根目录
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    raw = os.path.join(base, "data", "raw", "ClientResistance_decrypted.json")
    out = os.path.join(base, "workspace", "dataset", "ClientResistance_processed.json")
    process(raw, out)
