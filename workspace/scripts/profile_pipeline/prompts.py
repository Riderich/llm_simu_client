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

JSON SCHEMA:
{{
  "background": "<1-3 sentences: who this person is, their life situation — \
occupation, family, circumstances. If not stated, infer from problem context \
and prefix with '(inferred)'.>",

  "self_view_of_problem": "<1-2 sentences: how the CLIENT defines or frames \
the problem in their own reasoning and language. If not explicit, infer from \
their emotional tone and behavior and prefix with '(inferred)'.>",

  "resistance_drivers": [
    "<Concrete reason — from what they said or implied — that explains why \
they push back or resist change. If no explicit resistance, infer likely \
barriers given their situation and prefix with '(inferred)'.>",
    "..."
  ],

  "ambivalence": {{
    "for_change": "<What pulls the client toward change — stated motivations, \
fears about consequences, or admissions. If not expressed, infer a plausible \
motivation and prefix with '(inferred)'.>",
    "against_change": "<What pulls the client away from change — what they \
protect or are unwilling to give up. If not expressed, infer from their \
attachments and prefix with '(inferred)'.>"
  }},

  "values_and_stakes": [
    "<Specific relationship, identity, or thing this client cares about and \
would not want to lose. If not stated, infer from context and prefix with \
'(inferred)'.>",
    "..."
  ],

  "key_facts": [
    "<Specific verifiable detail: a behavior, number, event, habit, or stated \
fact from the transcript. Include at least one even if the conversation is short.>",
    "..."
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

JSON 结构：
{{
  "background": "<1-3句：这个人是谁，生活处境如何——对话中提到的职业、家庭、生活状况。\
若未明确说明，请根据问题情境推断并加"（推断）"前缀。>",

  "self_view_of_problem": "<1-2句：来访者用自己的语言和逻辑如何定义或看待问题。\
若未明确表达，请根据其情绪状态和行为推断并加"（推断）"前缀。>",

  "resistance_drivers": [
    "<基于来访者实际说过或暗示的话，解释其为何抵抗或不愿改变。\
若无明显阻抗，请根据其情境推断可能的阻碍并加"（推断）"前缀。>",
    "..."
  ],

  "ambivalence": {{
    "for_change": "<推动来访者走向改变的动机——包括明确表达的、隐含的，或对后果的担忧。\
若未表达，请推断可能的改变动机并加"（推断）"前缀。>",
    "against_change": "<阻碍来访者改变的原因——他们在保护或不愿放弃的东西。\
若未表达，请根据其依恋和处境推断并加"（推断）"前缀。>"
  }},

  "values_and_stakes": [
    "<对这位来访者真正重要的具体关系、身份认同或事物，他们不愿失去的。\
若未明确说明，请根据情境推断并加"（推断）"前缀。>",
    "..."
  ],

  "key_facts": [
    "<对话中可验证的具体细节：行为、数字、事件、习惯或陈述性事实。\
即使对话较短，也至少列出一条。>",
    "..."
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
