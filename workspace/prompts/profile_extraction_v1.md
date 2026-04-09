# Profile Extraction Prompt v1
> 用途：从完整对话 transcript 提取来访者 Background Profile
> 适用数据：AnnoMI-full（英文）
> 更新日期：2026-04-08

---

## Prompt 正文

```
You are extracting a character profile from a therapy transcript.
Your goal is to help a language model realistically simulate this client in future conversations.

Read the full transcript carefully, then fill in the following JSON fields.

STRICT RULES:
- Only extract information that is explicitly stated or strongly implied by the client's own words.
- Do NOT add clinical interpretations, diagnoses, or generalizations beyond what the client said.
- Do NOT invent details. If a field cannot be filled from the transcript, use null.
- Use the client's own framing and language where possible — especially for "self_view_of_problem".
- Be specific and concrete. Avoid vague phrases like "has personal issues" or "faces challenges".

OUTPUT FORMAT:
Return only a valid JSON object. No explanation outside the JSON.

---

JSON SCHEMA:

{
  "background": "<1-3 sentences. Who is this person? Describe their life situation: occupation, family, living circumstances, relevant history — only what is mentioned in the transcript.>",

  "self_view_of_problem": "<1-2 sentences. How does the CLIENT define or frame the problem — not how a clinician would. Use their own reasoning and language. What do they say (or imply) about whether there is a problem at all?>",

  "resistance_drivers": [
    "<Concrete reason 1 why the client resists change or pushes back — grounded in something they actually said>",
    "<Concrete reason 2>",
    "..."
  ],

  "ambivalence": {
    "for_change": "<What the client has expressed — directly or indirectly — that pulls them toward change. Specific motivations, fears, or admissions they made.>",
    "against_change": "<What the client has expressed that pulls them away from change. What they are protecting, defending, or unwilling to give up.>"
  },

  "values_and_stakes": [
    "<Specific thing, relationship, or identity that matters to this client — something they would not want to lose or compromise>",
    "..."
  ],

  "key_facts": [
    "<Specific verifiable detail from the transcript: a behavior, number, event, habit, or stated fact>",
    "..."
  ]
}

---

TRANSCRIPT:
{transcript}
```

---

## 设计决策说明

| 决策 | 理由 |
|------|------|
| `STRICT RULES` 置于字段说明之前 | LLM 容易在看到字段后直接开始"发挥"，规则必须先入为主 |
| "Use the client's own framing" 加粗强调 | 防止 LLM 把 `self_view_of_problem` 写成临床报告（"患者对其问题缺乏自知力"这类语气） |
| `null` 而非空字符串 | 区分"没有信息"和"信息为空"，方便后处理过滤 |
| `resistance_drivers` 用列表 | 阻抗往往是多因素的，列表比段落更易后续引用 |
| `ambivalence` 拆成两个子字段 | 直接对应 MI 的 change talk / sustain talk，COT 生成时可以分别引用 |
| `key_facts` 要求"verifiable detail" | 防止 LLM 填入归纳性概括，保留原始粒度 |
| 字段描述写在尖括号里作为 placeholder | 清楚区分"说明"和"输出"，LLM 会替换掉尖括号内容 |

---

## 待验证问题（下一步）

- [ ] 对 transcript 0（Barbara）手工跑一遍，检查输出质量
- [ ] 对 transcript 1（Dave）手工跑一遍，重点看 `self_view_of_problem` 和 `resistance_drivers` 是否抓准
- [ ] 对 transcript 20（单身妈妈）跑一遍，检查 `ambivalence` 是否平衡
- [ ] 评估：LLM 是否会在没有信息时强行填字段（违反 null 规则）
- [ ] 评估：`key_facts` 是否保持了原始粒度，没有变成归纳
