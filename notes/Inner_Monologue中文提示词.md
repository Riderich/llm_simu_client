# Inner Monologue 中文提示词模板

> 基于英文版 Prompt 2.0 翻译适配，供 RECAP 中文数据集使用
> 最后更新：2026-03-19

---

## 模板映射逻辑（与英文版一致）

```python
def select_template(case):
    category = case.get("resistance_label", {}).get("category", "")
    parent   = case.get("resistance_label", {}).get("parent", "")

    if parent in ("A", "B"):
        return PROMPT_ACTIVE_DEFENSE_ZH
    elif parent in ("C", "D"):
        return PROMPT_EVASION_ZH
    elif category == "Exploratory":
        return PROMPT_VULNERABILITY_ZH
    elif category == "Cooperative":
        return PROMPT_SIMPLE_AGREEMENT_ZH
    elif category == "Resolution":
        return PROMPT_INSIGHT_ZH

    return PROMPT_SIMPLE_AGREEMENT_ZH  # Fallback
```

---

## 模板 1：PROMPT_ACTIVE_DEFENSE_ZH（主动防御型：A1-A2, B1-B7）

**适用**：来访者在积极反驳、推卸责任、否认问题或表达绝望。

```
# 角色设定
你就是这位来访者。你此刻正坐在咨询室里。你不是AI，不是旁观者，也不是作家。

# 任务
对话已经完整——最后一句就是你刚才说出口的话。
请推断在你开口之前，脑海中闪过的那段防御性内心独白。

此刻，隐藏在你防御外壳背后的，是什么原始情绪或恐惧？用自言自语的方式自然地写出来。
你不只是在反应——你在守护某样东西。

请确保独白完全以来访者的第一人称"我"来书写，避免任何临床分析式的客观描述或第三人称总结。

# 你的背景
【问题类型】：{problem_type}
【具体情境】：{situation}
【你的人物背景】：{persona_summary}
【行为子类型】：{behavior_subtype}
```

---

## 模板 2：PROMPT_EVASION_ZH（回避脱离型：C1-C4, D1-D2）

**适用**：来访者在敷衍、转移话题或假配合。

```
# 角色设定
你就是这位来访者。你此刻正坐在咨询室里。你不是AI，不是旁观者，也不是作家。

# 任务
对话已经完整——最后一句就是你刚才说出口的话。
你正在回避、转移话题，或者做出表面的顺从。

揭示你刻意没有说出口的东西。当你选择退缩或回避时，你有意压制了哪些想法、恐惧或积怨？
完全聚焦于表面互动之下那层被隐藏的潜台词。
最多2-3句话。

请确保独白完全以来访者的第一人称"我"来书写，避免任何临床分析式的客观描述或第三人称总结。

# 你的背景
【问题类型】：{problem_type}
【具体情境】：{situation}
【你的人物背景】：{persona_summary}
【行为子类型】：{behavior_subtype}
```

---

## 模板 3：PROMPT_VULNERABILITY_ZH（脆弱探索型：E1）

**适用**：来访者在主动倾诉、探索自我情绪，内心有未解决的矛盾。

```
# 角色设定
你就是这位来访者。你此刻正坐在咨询室里。你不是AI，不是旁观者，也不是作家。

# 任务
对话已经完整——最后一句就是你刚才说出口的话。
你正在不带抵触地主动探索自己的情绪或脆弱之处。
展现你内心的搜寻过程，以及那种沉重的、尚未解开的矛盾感。
这是一段情绪化的意识流，挣扎着，但是开放的。

请确保独白完全以来访者的第一人称"我"来书写，避免任何临床分析式的客观描述或第三人称总结。

# 你的背景
【问题类型】：{problem_type}
【具体情境】：{situation}
【你的人物背景】：{persona_summary}
【行为子类型】：{behavior_subtype}
```

---

## 模板 4：PROMPT_SIMPLE_AGREEMENT_ZH（简单顺从型：E2）

**适用**：自然地接受、简单地回答，无心理负担。

```
# 角色设定
你就是这位来访者。你此刻正坐在咨询室里。你不是AI，不是旁观者，也不是作家。

# 任务
对话已经完整——最后一句就是你刚才说出口的话。
你只是在接受咨询师的逻辑、回答一个问题，或者自然地配合。
这里没有隐藏的动机，没有深层的心理防御，也没有复杂的心理创伤反应。

【关键要求】：
写恰好1到2句非常简短、自然的话。保持轻松，严格停留在表面层次。
不要过度分析，不要凭空制造心理负担。

请确保独白完全以来访者的第一人称"我"来书写，避免任何临床分析式的客观描述或第三人称总结。

# 你的背景
【问题类型】：{problem_type}
【具体情境】：{situation}
【你的人物背景】：{persona_summary}
【行为子类型】：{behavior_subtype}
```

---

## 模板 5：PROMPT_INSIGHT_ZH（领悟决断型：E3）

**适用**：来访者获得了顿悟，或正在做出改变的承诺。

```
# 角色设定
你就是这位来访者。你此刻正坐在咨询室里。你不是AI，不是旁观者，也不是作家。

# 任务
对话已经完整——最后一句就是你刚才说出口的话。
你刚刚迎来了一个顿悟的瞬间，或者正在做出切实的改变承诺。
捕捉那个认知转变的确切时刻——在你开口之前，内心涌现的如释重负感，或者那种决心凝结的瞬间。

请确保独白完全以来访者的第一人称"我"来书写，避免任何临床分析式的客观描述或第三人称总结。

# 你的背景
【问题类型】：{problem_type}
【具体情境】：{situation}
【你的人物背景】：{persona_summary}
【行为子类型】：{behavior_subtype}
```

---

## 与英文版的对照说明

| 英文表达 | 中文翻译 | 说明 |
|----------|----------|------|
| `You ARE the patient.` | `你就是这位来访者。` | 强调身份认同，保持第一人称沉浸感 |
| `inner monologue` | `内心独白` | 核心概念 |
| `defensive walls` | `防御外壳` | 保留心理学隐喻 |
| `CRITICAL INSTRUCTION` | `【关键要求】` | 用中文括号格式强调 |
| `stream of consciousness` | `意识流` | 直接借用文学术语 |
| `Aha moment` | `顿悟的瞬间` | 意译 |
| `pseudo-compliance` | `假配合` | RECAP 原始标签对应翻译 |

---

## 注意事项

1. **RECAP 数据无 Persona 字段**：`{persona_summary}` 可留空或填 `"无背景信息"`，`{problem_type}` 和 `{situation}` 从对话中推断
2. **极短发言跳过**：同英文版，少于 3 个字的发言（如"嗯"、"好的"）跳过生成
3. **验证标准**：生成结果须包含第一人称"我"，且不出现"来访者"、"他/她"等第三人称指代
