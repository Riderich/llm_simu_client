"""
ExTES Unknown 子集：两行输出（大类 + 小类）prompt 小批量对比实验。
不写 code；后处理拼接为 PsyFIRE 中文标签再查 LABELS_MAP。
"""
from __future__ import annotations

import json
import random
import re
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_PATH = "/data5/zxj/llm_simu_client/ClientResistance-Model-Share/only_resistance_share_model"
FINE_PATH = Path("/data5/zxj/llm_simu_client/workspace/results/extes/resist_fine.json")
BINARY_PATH = Path("/data5/zxj/llm_simu_client/workspace/results/extes/binary.json")
OUT_PATH = Path("/data5/zxj/llm_simu_client/workspace/results/extes/experiments/two_line_smoketest.json")

# 与仓库内细标脚本一致（仅中文键）
LABELS_MAP = {
    "争辩-挑战": "A1",
    "争辩-贬低": "A2",
    "否认-责怪": "B1",
    "否认-不认同": "B2",
    "否认-找借口": "B3",
    "否认-最小化": "B4",
    "否认-悲观": "B5",
    "否认-犹豫": "B6",
    "否认-不愿改变": "B7",
    "回避-最小的回应": "C1",
    "回避-界限设定": "C2",
    "忽视-不关注": "D1",
    "忽视-岔开话题": "D2",
}

MICRO_BY_MACRO: dict[str, tuple[str, ...]] = {
    "争辩": ("挑战", "贬低"),
    "否认": ("责怪", "不认同", "找借口", "最小化", "悲观", "犹豫", "不愿改变"),
    "回避": ("最小的回应", "界限设定"),
    "忽视": ("不关注", "岔开话题"),
}

MACROS = tuple(MICRO_BY_MACRO.keys())

TWO_LINE_PROMPT = """你是心理咨询师，为来访者阻抗行为分类。

大类只能是：争辩、否认、回避、忽视。

各大类对应小类（小类必须属于当前大类，禁止自创组合）：
争辩的小类：挑战、贬低
否认的小类：责怪、不认同、找借口、最小化、悲观、犹豫、不愿改变
回避的小类：最小的回应、界限设定
忽视的小类：不关注、岔开话题

阅读下面的【上下文】与【来访者回应】，选出最合适的一大类、一小类。

输出要求（必须严格遵守）：
只输出两行纯文本，不要标题、不要解释、不要编号、不要 Markdown、不要复述对话、不要输出英文。
第一行：只写一个大类词（争辩 或 否认 或 回避 或 忽视）
第二行：只写一个小类词（必须从上面该大类下列出的小类里选）
"""


def strip_line_prefix(line: str) -> str:
    s = line.strip()
    s = re.sub(r"^(第一行|第二行|大类|小类)[:：]\s*", "", s)
    return s.strip()


def _is_noise_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    if s.startswith("###") or s.startswith("#"):
        return True
    if re.match(r"^【.+】$", s):
        return False
    if "上下文" in s and len(s) > 20:
        return True
    if "来访者" in s and len(s) > 25 and ("回应" in s or "回答" in s):
        return True
    if s.startswith("任务") or s.startswith("输出") or s.startswith("选项"):
        return True
    return False


def parse_two_lines(text: str) -> tuple[str, str]:
    """在续写中收集所有「大类 + 其后窗口内合法小类」对，取最后一对（模型常先胡写再自纠）。"""
    raw_lines = (text or "").strip().splitlines()
    lines = [strip_line_prefix(x) for x in raw_lines]
    lines = [x for x in lines if x and not _is_noise_line(x)]

    pairs: list[tuple[str, str]] = []
    for i, line in enumerate(lines):
        if line not in MICRO_BY_MACRO:
            continue
        macro = line
        allowed = MICRO_BY_MACRO[macro]
        for w in lines[i + 1 : i + 8]:
            if w in allowed:
                pairs.append((macro, w))
    return pairs[-1] if pairs else ("", "")


def validate_and_join(macro: str, micro: str) -> tuple[str, str, str]:
    """返回 (combined_label, fine_category, parse_note)"""
    if macro not in MICRO_BY_MACRO:
        return "", "Unknown", f"invalid_macro:{macro!r}"
    allowed = MICRO_BY_MACRO[macro]
    if micro not in allowed:
        return "", "Unknown", f"invalid_micro_for_{macro}:{micro!r}"
    combined = f"{macro}-{micro}"
    cat = LABELS_MAP.get(combined, "Unknown")
    if cat == "Unknown":
        return combined, "Unknown", "not_in_LABELS_MAP"
    return combined, cat, "ok"


def main() -> None:
    random.seed(42)
    n_sample = 48

    fine = json.loads(FINE_PATH.read_text(encoding="utf-8"))
    binary = json.loads(BINARY_PATH.read_text(encoding="utf-8"))
    by_id = {r["sample_id"]: r for r in binary}

    unk = [r for r in fine if r.get("fine_category") == "Unknown"]
    sample = random.sample(unk, min(n_sample, len(unk)))

    tok = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH, torch_dtype=torch.bfloat16, trust_remote_code=True
    ).to("cuda:0")
    model.eval()

    rows = []
    for r in sample:
        sid = r["sample_id"]
        src = by_id[sid]
        context = src.get("context", "")
        response = src.get("response", r.get("response", ""))

        prompt = (
            f"{TWO_LINE_PROMPT}\n\n【上下文】\n{context}\n\n"
            f"【来访者回应】\n{response}\n\n"
            "两行答案：\n"
        )

        inputs = tok(prompt, return_tensors="pt", truncation=True, max_length=1536)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        with torch.no_grad():
            out = model.generate(
                **inputs,
                max_new_tokens=32,
                do_sample=False,
                pad_token_id=tok.eos_token_id,
            )
        decoded = tok.decode(out[0][inputs["input_ids"].shape[1] :], skip_special_tokens=True)

        macro, micro = parse_two_lines(decoded)
        combined, new_cat, note = validate_and_join(macro, micro)

        rows.append(
            {
                "sample_id": sid,
                "old_fine_label": r.get("fine_label", ""),
                "old_fine_category": r.get("fine_category", "Unknown"),
                "new_raw_output": decoded.strip(),
                "parsed_macro": macro,
                "parsed_micro": micro,
                "new_fine_label": combined,
                "new_fine_category": new_cat,
                "parse_note": note,
                "response_preview": (response or "")[:200],
            }
        )

    solved = sum(1 for x in rows if x["new_fine_category"] != "Unknown")
    summary = {
        "n": len(rows),
        "seed": 42,
        "solved_from_unknown": solved,
        "solved_rate": solved / len(rows) if rows else 0.0,
        "parse_ok": sum(1 for x in rows if x["parse_note"] == "ok"),
    }

    out = {"summary": summary, "rows": rows}
    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
