from __future__ import annotations

from .types import Language

# ── English (AnnoMI / ESConv / MESC) ─────────────────────────────────────────

SYSTEM_EN = (
    "You are building a character profile from a therapy transcript. "
    "Your goal is to help a language model realistically simulate this client "
    "in future conversations. Every field must be filled — a complete profile "
    "is always more useful than a partial one. "
    "Use the transcript as your primary source. When the transcript does not "
    "provide enough evidence for a field, make a reasonable inference based on "
    "the client's emotional tone, problem type, and situation — and prefix that "
    "content with '(inferred)' so it can be distinguished from direct evidence."
)

USER_TEMPLATE_EN = """\
Read the full therapy transcript below, then return a JSON object with exactly \
these six fields. Every field must be filled — never return null or [].

RULES:
1. Prefer direct evidence: extract what the client explicitly states or \
strongly implies.
2. When direct evidence is absent for a field, infer a plausible value from \
the client's emotional state, problem context, and situation — and prefix it \
with "(inferred)".
3. Use the client's own framing and language — especially for \
"self_view_of_problem".
4. Be specific and concrete. Never write vague phrases like \
"has personal challenges".
5. Return ONLY the JSON object. No explanation, no markdown fences.
6. AVOID REDUNDANCY across fields: each field captures a different dimension. \
Do not restate the same idea in multiple fields with different wording.
7. AVOID REDUNDANCY within each list field: each item must capture a \
DISTINCT, NON-OVERLAPPING aspect. If the same underlying mechanism or pattern \
appears across multiple topics (e.g., client minimizes their drinking, their \
isolation, and their anger), collapse it into ONE item that names the pattern \
("uses minimization across multiple domains when confronted"), not three \
instances of it. If two items feel similar, merge them.

FIELD BOUNDARIES (critical — read before filling):
- "resistance_drivers": HOW and WHEN resistance activates — the mechanism or \
trigger (e.g., "deflects when therapist challenges self-image"). Name the \
PATTERN, not each instance of it. NOT what they value. MAX 3 items.
- "ambivalence.against_change": the INTERNAL EMOTIONAL PULL away from change \
— fear, attachment, identity threat. NOT a list of valued things. 1 sentence.
- "values_and_stakes": the CONCRETE OBJECTS AT RISK — specific relationships, \
roles, or outcomes they would lose by changing. NOT the mechanism or feeling. \
MAX 3 items.
- "key_facts": only facts that predict the client's next response — skip \
therapist statements, background trivia, and any fact that duplicates a \
pattern already named in resistance_drivers. ONE sentence each. MAX 3 items.

JSON SCHEMA:
{{
  "background": "<1-2 sentences: who this person is — occupation, family, \
life situation. If not stated, infer from problem context and prefix with \
'(inferred)'.>",

  "self_view_of_problem": "<1-2 sentences: how the CLIENT defines or frames \
the problem in their own reasoning and language. If not explicit, infer from \
their emotional tone and behavior and prefix with '(inferred)'.>",

  "resistance_drivers": [
    "<trigger/mechanism 1 — how and when resistance activates. Prefix if inferred.>",
    "<trigger/mechanism 2 — must differ from item 1. Omit if no second distinct mechanism.>",
    "<trigger/mechanism 3 — must differ from items 1-2. Omit if no third distinct mechanism. STOP — max 3.>"
  ],

  "ambivalence": {{
    "for_change": "<The internal pull toward change — a specific fear, desire, \
or admission. 1 sentence. Prefix with '(inferred)' if not explicit.>",
    "against_change": "<The internal pull away from change — a specific \
emotional attachment or identity threat. 1 sentence. Prefix if inferred.>"
  }},

  "values_and_stakes": [
    "<concrete stake 1 — a specific thing/relationship/role at risk. Prefix if inferred.>",
    "<concrete stake 2 — must differ from item 1. Omit if no second distinct stake.>",
    "<concrete stake 3 — must differ from items 1-2. Omit if no third. STOP — max 3.>"
  ],

  "key_facts": [
    "<fact 1 — a specific event, number, or behavior that predicts next response. 1 sentence.>",
    "<fact 2 — must predict something different from fact 1. Omit if no second distinct fact.>",
    "<fact 3 — must predict something different from facts 1-2. Omit if no third. STOP — max 3. \
No pattern summaries here (those belong in resistance_drivers). \
No therapist statements. No background trivia.>"
  ]
}}

TRANSCRIPT:
{transcript}
"""

# ── Chinese (RECAP) ───────────────────────────────────────────────────────────

SYSTEM_ZH = (
    "你正在为心理咨询对话记录构建来访者档案。"
    "你的目标是帮助语言模型在后续对话中真实地模拟这位来访者。"
    "每个字段都必须填写——完整的档案始终比残缺的更有价值。"
    "以对话内容为主要依据；当某字段的证据不足时，请基于来访者的情绪状态、"
    "问题类型和情境做出合理推断，并在该内容前加上'（推断）'前缀，以便与直接证据区分。"
)

USER_TEMPLATE_ZH = """\
请仔细阅读下方的心理咨询对话，然后返回一个包含以下六个字段的 JSON 对象。\
每个字段都必须填写，不得返回 null 或空列表 []。

规则：
1. 优先使用直接证据：提取来访者明确陈述或强烈暗示的内容。
2. 当某字段缺乏直接证据时，根据来访者的情绪状态、问题背景和情境推断合理的内容，\
并在该内容前加上"（推断）"前缀。
3. 使用来访者自己的表述方式——尤其是 "self_view_of_problem" 字段。
4. 要具体、有细节，不要写"有个人问题"这类模糊表述。
5. 只返回 JSON 对象本身，不要有任何解释或 markdown 代码块。
6. 避免字段间内容重复：每个字段捕捉不同维度，不要用不同措辞在多个字段中表达同一个意思。
7. 避免字段内部条目重叠：每个列表字段的每一条必须捕捉不同、互不重叠的方面。\
如果同一个底层模式在多个话题上都有体现（如来访者对饮酒、孤独、愤怒都采取最小化应对），\
则归并为一条描述该模式的总结（"面对质疑时惯用最小化应对"），而不是分别列出三个例子。\
如果两条感觉相似，合并它们。

字段边界（填写前必读）：
- "resistance_drivers"：阻抗的触发机制——什么情境或咨询师的话激活阻抗，以及如何表现。\
写出模式本身，而非模式的每一个实例。不要写来访者珍视什么。最多 3 条。
- "ambivalence.against_change"：远离改变的内心情感力量——恐惧、依恋、认同威胁。\
不是具体失去什么的列举。1 句话。
- "values_and_stakes"：改变后将失去的具体对象——特定关系、角色或结果。\
不是阻抗机制或情绪状态。最多 3 条。
- "key_facts"：只列出能预测来访者下一句话的细节——跳过咨询师的陈述、无关背景细节、\
以及 resistance_drivers 中已命名的模式的具体实例。每条一句话，最多 3 条。

JSON 结构：
{{
  "background": "<1-2句：这个人是谁——职业、家庭、生活处境。\
若未明确说明，请根据问题情境推断并加"（推断）"前缀。>",

  "self_view_of_problem": "<1-2句：来访者用自己的语言和逻辑如何定义或看待问题。\
若未明确表达，请根据其情绪状态和行为推断并加"（推断）"前缀。>",

  "resistance_drivers": [
    "<触发机制 1——什么情境或咨询师的话激活阻抗，以及如何表现。推断内容加（推断）前缀。>",
    "<触发机制 2——必须与第 1 条不同。若无第二个独立机制则省略此条。>",
    "<触发机制 3——必须与前两条不同。若无第三个则省略。停止——最多 3 条。>"
  ],

  "ambivalence": {{
    "for_change": "<推动改变的内心力量——一种具体的恐惧、渴望或承认。1 句话。\
若非明确表达请加（推断）前缀。>",
    "against_change": "<阻碍改变的内心力量——一种具体的情感依恋或认同威胁。1 句话。\
若非明确表达请加（推断）前缀。>"
  }},

  "values_and_stakes": [
    "<具体风险 1——改变后将失去的具体事物、关系或角色。推断内容加（推断）前缀。>",
    "<具体风险 2——必须与第 1 条不同。若无第二个独立风险则省略。>",
    "<具体风险 3——必须与前两条不同。若无第三个则省略。停止——最多 3 条。>"
  ],

  "key_facts": [
    "<关键事实 1——能预测来访者下一句话的具体事件、数字或行为。1 句话。>",
    "<关键事实 2——必须预测与第 1 条不同的内容。若无则省略。>",
    "<关键事实 3——必须预测与前两条不同的内容。若无则省略。停止——最多 3 条。\
不写模式概括（属于 resistance_drivers）。不写咨询师陈述。不写无关背景细节。>"
  ]
}}

对话记录：
{transcript}
"""


def get_prompts(language: Language) -> tuple[str, str]:
    """Return (system_prompt, user_template) for the given language."""
    if language == "zh":
        return SYSTEM_ZH, USER_TEMPLATE_ZH
    return SYSTEM_EN, USER_TEMPLATE_EN
