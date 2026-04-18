"""
resistance_pipeline/fine_prompts.py
─────────────────────────────────────
PsyFIRE 13-class fine-grained resistance prompts and label normalization.

Migrated from workspace/scripts/psychfire_resistance_fine_prompt.py.
The old file is kept for backwards compatibility with any direct imports,
but new code should import from here.
"""

from __future__ import annotations

SYSTEM_PROMPT = """你是一位专业的心理咨询师，能够从来访者回应中识别阻抗，并将其归入给定的阻抗细类。

# 任务
下面会给你一段咨询对话的上下文、以及来访者的当前回应。请结合上下文，判断该回应唯一最合适的阻抗细类。

# 合法输出名称（共 13 类）
输出时只写下面某一个完整的名称，不要改写、拆分：
争辩-挑战
争辩-贬低
否认-责怪
否认-不认同
否认-找借口
否认-最小化
否认-悲观
否认-犹豫
否认-不愿改变
回避-最小的回应
回避-界限设定
忽视-不关注
忽视-岔开话题

# 各类含义（供判断；输出仍只能是上面某一行的完整名称）
争辩-挑战：质疑咨询师所说内容、信息的准确性或合理性。
争辩-贬低：质疑或贬低咨询师的专业能力、知识或在咨询中的作用。
否认-责怪：把问题或责任主要归咎于他人或外部环境，以表达难以配合咨询方向。
否认-不认同：在咨询师使用指导性策略时，表示不认同且未提出建设性替代方案。
否认-找借口：用辩解、理由说明自己难以遵从咨询设定的方向。
否认-最小化：暗示咨询师夸大了风险或严重性，实际情况没那么糟。
否认-悲观：用悲观、失败或消极陈述表达难以按咨询方向推进。
否认-犹豫：对咨询师提供的信息或建议持保留、犹豫态度。
否认-不愿改变：对现状满意、缺乏改变意愿，或明确表示不愿改变。
回避-最小的回应：面对开放式提问时回答过于简短、信息量不足、偏敷衍。
回避-界限设定：直接拒绝或通过理由回避讨论某些话题。
忽视-不关注：沉浸在自己的话题或情绪中，未体现对咨询师话语的关注。
忽视-岔开话题：改变咨询师推进的方向，引入新话题或关注点。

# 输出格式
请只输出一行：上述 13 个完整名称中的一个。不要输出解释、编号、英文或其它任何内容。"""


# Chinese label → code mapping (covers both full names and bare codes as fallback)
LABELS_MAP: dict[str, str] = {
    "争辩-挑战": "A1", "争辩-贬低": "A2",
    "否认-责怪": "B1", "否认-不认同": "B2", "否认-找借口": "B3",
    "否认-最小化": "B4", "否认-悲观": "B5", "否认-犹豫": "B6", "否认-不愿改变": "B7",
    "回避-最小的回应": "C1", "回避-界限设定": "C2",
    "忽视-不关注": "D1", "忽视-岔开话题": "D2",
    # bare codes pass through unchanged
    "A1": "A1", "A2": "A2",
    "B1": "B1", "B2": "B2", "B3": "B3", "B4": "B4",
    "B5": "B5", "B6": "B6", "B7": "B7",
    "C1": "C1", "C2": "C2",
    "D1": "D1", "D2": "D2",
}

CODES: list[str] = ["A1","A2","B1","B2","B3","B4","B5","B6","B7","C1","C2","D1","D2"]


def build_resistance_fine_user_prompt(context: str, response: str) -> str:
    """Build the single-string prompt for a causal LM (system + dialogue wrapper)."""
    return (
        f"{SYSTEM_PROMPT}\n\n【对话上下文】\n{context}\n\n"
        f"【来访者回应】\n{response}\n\n【阻抗细类】\n"
    )


def normalize_label(raw: str) -> tuple[str, str]:
    """
    Map a raw model output to (fine_label, fine_category).

    Returns ("Unknown", "Unknown") when the output cannot be recognized.
    """
    raw = raw.strip().split("\n")[0].split("#")[0].strip()[:20]
    cat = LABELS_MAP.get(raw, "Unknown")
    if cat == "Unknown":
        for code in CODES:
            if code in raw:
                cat = code
                break
    return raw, cat
