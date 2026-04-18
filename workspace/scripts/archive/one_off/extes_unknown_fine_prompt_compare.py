"""
ExTES：`extes_resistance_fine.json` 中 fine_category=Unknown 的样本，对比

- **原先（落盘）**：该文件中保存的 fine_label / fine_category（均为历史推理结果）
- **旧 prompt 现场**：含 (A1) 代号 + `###` 模板（与改版前 esconv 细标脚本风格一致）
- **新 prompt 现场**：`scripts/psychfire_resistance_fine_prompt.py` 统一提示词 + `【】` 模板

上下文与来访者句：`extes_binary.json`。

用法（在 workspace 目录下或任意目录均可，路径已写死）：
  CUDA_VISIBLE_DEVICES=5 python scripts/archive/one_off/extes_unknown_fine_prompt_compare.py
"""
from __future__ import annotations

import json
import os
import random
import sys
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

_SCRIPTS = Path(__file__).resolve().parents[2]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from psychfire_resistance_fine_prompt import build_resistance_fine_user_prompt

WORKSPACE = Path("/data5/zxj/llm_simu_client/workspace")
FINE_PATH = WORKSPACE / "results" / "extes_resistance_fine.json"
BINARY_PATH = WORKSPACE / "results" / "extes_binary.json"
MODEL_PATH = "/data5/zxj/llm_simu_client/ClientResistance-Model-Share/only_resistance_share_model"
OUT_JSON = WORKSPACE / "results" / "extes_unknown_prompt_compare.json"
OUT_MD = WORKSPACE / "results" / "extes_unknown_prompt_compare.md"

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
ALL_CODES = ("A1", "A2", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "C1", "C2", "D1", "D2")

OLD_SYSTEM_PROMPT = """# 角色
你是专业心理咨询师，对来访者的阻抗行为进行分类。

# 阻抗行为定义与类别
## 争辩 (Challenging)
- 争辩-挑战(A1): 质疑咨询师所说内容的准确性、合理性和可能性
- 争辩-贬低(A2): 贬低咨询师的专业能力和作用

## 否认 (Denying)
- 否认-责怪(B1): 将问题归咎于他人或外部环境
- 否认-不认同(B2): 不认同咨询师的观点，没有提出替代方案
- 否认-找借口(B3): 为行为找借口，表达不会遵从咨询建议
- 否认-最小化(B4): 暗示咨询师夸大了问题的严重性
- 否认-悲观(B5): 做出悲观、消极的陈述，表示没有希望
- 否认-犹豫(B6): 对咨询师的建议持保留态度，犹豫是否采纳
- 否认-不愿改变(B7): 直接表明不愿意改变现状

## 回避 (Avoiding)
- 回避-最小的回应(C1): 以简短回答回避深入讨论
- 回避-界限设定(C2): 拒绝讨论某些话题，设定界限

## 忽视 (Ignoring)
- 忽视-不关注(D1): 沉浸在自己的话题，未关注咨询师
- 忽视-岔开话题(D2): 改变谈话方向，提出新话题

# 任务
根据对话上下文和来访者回应，判断属于以上哪一类阻抗行为。
直接输出类别名称（如"争辩-挑战"），不要输出其他内容。"""


def format_context(context, max_turns: int = 3) -> str:
    if isinstance(context, str):
        return context
    if not context:
        return ""
    lines = []
    for turn in context[-max_turns:]:
        speaker = turn.get("speaker", turn.get("role", ""))
        content = (turn.get("content") or turn.get("text") or "").strip()
        if speaker and content:
            speaker_cn = (
                "咨询师" if speaker in ("therapist", "supporter", "user") else "来访者"
            )
            lines.append(f"{speaker_cn}: {content}")
    return "\n".join(lines)


def build_old_style_prompt(system: str, context: str, target: str) -> str:
    return (
        f"{system}\n\n### 对话上下文:\n{context}\n\n"
        f"### 来访者回应:\n{target}\n\n### 阻抗类别:\n"
    )


def decode_label(tokenizer, model, prompt: str) -> tuple[str, str, str]:
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1536)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=15,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    raw = tokenizer.decode(out[0][inputs["input_ids"].shape[1] :], skip_special_tokens=True).strip()
    line0 = raw.split("\n")[0].strip()
    if "#" in line0:
        line0 = line0.split("#")[0].strip()
    fine_label = line0[:24].strip()
    cat = LABELS_MAP.get(fine_label, "Unknown")
    if cat == "Unknown":
        for code in ALL_CODES:
            if code in fine_label:
                cat = code
                break
    return fine_label, cat, raw


def main() -> None:
    random.seed(42)
    n_sample = int(os.environ.get("EXTES_UNKNOWN_COMPARE_N", "40"))

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
        ctx = format_context(src.get("context", ""))
        tgt = src.get("response", r.get("response", ""))

        p_old = build_old_style_prompt(OLD_SYSTEM_PROMPT, ctx, tgt)
        p_new = build_resistance_fine_user_prompt(ctx, tgt)

        old_lab, old_cat, _ = decode_label(tok, model, p_old)
        new_lab, new_cat, _ = decode_label(tok, model, p_new)

        rows.append(
            {
                "sample_id": sid,
                "stored_fine_label": r.get("fine_label"),
                "stored_fine_category": r.get("fine_category"),
                "old_prompt_live_label": old_lab,
                "old_prompt_live_category": old_cat,
                "new_prompt_live_label": new_lab,
                "new_prompt_live_category": new_cat,
                "new_resolved": new_cat != "Unknown",
                "old_resolved": old_cat != "Unknown",
                "old_vs_new_same_label": old_lab == new_lab,
                "response_preview": (tgt or "")[:160],
            }
        )

    n = len(rows)
    summary = {
        "pool_unknown_total": len(unk),
        "n_sampled": n,
        "seed": 42,
        "new_resolved_count": sum(1 for x in rows if x["new_resolved"]),
        "new_resolved_rate": sum(1 for x in rows if x["new_resolved"]) / n if n else 0.0,
        "old_resolved_count": sum(1 for x in rows if x["old_resolved"]),
        "old_resolved_rate": sum(1 for x in rows if x["old_resolved"]) / n if n else 0.0,
        "old_vs_new_same_label_rate": sum(1 for x in rows if x["old_vs_new_same_label"]) / n
        if n
        else 0.0,
    }

    payload = {"summary": summary, "rows": rows}
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    s = summary
    lines_md = [
        "# ExTES Unknown（420 池）细标 prompt 抽样对比",
        "",
        f"- Unknown 池总数: **{s['pool_unknown_total']}**",
        f"- 本次抽样: **{s['n_sampled']}**（`seed=42`，可用环境变量 `EXTES_UNKNOWN_COMPARE_N` 改条数）",
        "- **原先（落盘）**：`extes_resistance_fine.json` 中该条的 `fine_label`（当时映射为 Unknown）",
        "- **旧 prompt 现场**：含 `(A1)` + `###` 模板",
        "- **新 prompt 现场**：`psychfire_resistance_fine_prompt.py` 统一提示词 + `【】` 模板",
        "",
        "## 汇总",
        "",
        "| 指标 | 值 |",
        "|------|-----|",
        f"| 新 prompt 映射非 Unknown | {s['new_resolved_count']}/{s['n_sampled']}（{s['new_resolved_rate']:.1%}） |",
        f"| 旧 prompt 现场非 Unknown | {s['old_resolved_count']}/{s['n_sampled']}（{s['old_resolved_rate']:.1%}） |",
        f"| 旧现场 vs 新现场标签字符串相同 | {s['old_vs_new_same_label_rate']:.1%} |",
        "",
        "## 逐条（前 30 条）",
        "",
        "| sample_id | 落盘(原) | 旧 prompt 现场 | 新 prompt 现场 | 新已映射 |",
        "|-----------|----------|----------------|----------------|----------|",
    ]
    for x in rows[:30]:
        ok = "是" if x["new_resolved"] else "否"
        lines_md.append(
            f"| `{x['sample_id']}` | {x['stored_fine_label']} | {x['old_prompt_live_label']} | "
            f"{x['new_prompt_live_label']} | {ok} |"
        )
    lines_md += ["", f"完整 JSON：`{OUT_JSON}`", ""]
    OUT_MD.write_text("\n".join(lines_md), encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")


if __name__ == "__main__":
    main()
