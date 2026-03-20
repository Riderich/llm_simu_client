# Inner Monologue 技术文档

> 整理人：王铮  
> 最后更新：2026-03-12  
> 本文档整合 Pipeline 改进计划 + Prompt 设计说明，供团队 review 和实施参考

---

## 一、当前状态与问题

### 现行实现（`verify_psyfire_prompt.py`）

**切换逻辑**：按词数区分两个模板

```python
SHORT_GT_THRESHOLD = 5
template = PROMPT_TEMPLATE_SHORT if gt_words <= SHORT_GT_THRESHOLD else PROMPT_TEMPLATE
```

**已知问题**：
| 问题 | 影响 |
|------|------|
| 切换依据是词数而非阻抗类别 | `"No."` 被归入最简模板，但这往往是最强烈的拒绝，需要深度分析 |
| 标注粒度是 transcript 级别 | 无法为不同 client 句子分配正确的 internal 策略 |
| 大锅饭式的 Prompt 约束 | 为不同类别注入单句 guidance 行不通（LLM容易将"深挖防御"和"简单配合"的指令混淆），导致长度和语气违和 |

---

## 二、目标架构：utterance 级标注 → 独立模板分配

```
每条 client utterance
    ↓ Step 1：阻抗类别标注（annotate_resistance.py）
    ↓ Step 2：按类别映射到 5 个具有刚性约束的专属 Prompt（select_template()）
    ↓ Step 3：生成 Inner Monologue（verify_psyfire_prompt.py）
```

---

## 三、新模块：`annotate_resistance.py`（新建）

**功能**：对每条 client utterance 独立调用 LLM，按 Client Behavior Space（14 类）进行分类，结果写回 JSON 中 `resistance_label` 字段。

**标注 Prompt（utterance 级别单句分类）**：

```
You are a clinical psychologist familiar with resistance in therapy.
Given the dialogue context below, classify the final CLIENT utterance.

# Client Behavior Categories
[A: Arguing] A1-Challenging, A2-Discounting
[B: Denying] B1-Blaming, B2-Disagreeing, B3-Excusing, B4-Minimizing,
             B5-Pessimism, B6-Reluctance, B7-Unwillingness
[C: Avoiding] C1-Minimum Talk, C2-Limit Setting, C3-Topic Shift, C4-Pseudo-Compliance
[D: Ignoring] D1-Inattention, D2-Sidetracking
[E: No Resistance] E1-Exploratory, E2-Cooperative, E3-Resolution
...
```

---

## 四、Prompt 模板体系（5 个完全独立的基准模板）

**设计动因**：不同行为的 internal 在核心任务、禁忌（Constraints）和语气上存在根本差异。使用同一个大模板外加条件 `if` 会导致 LLM 生成矛盾。必须按"心理动机特征"硬拆分为 5 个独立模板。

### 4.1 模板映射逻辑

```python
def select_template(case):
    category = case.get("resistance_label", {}).get("category", "")
    parent = case.get("resistance_label", {}).get("parent", "")
    
    if parent in ("A", "B"):
        return PROMPT_ACTIVE_DEFENSE
    elif parent in ("C", "D"):
        return PROMPT_EVASION
    elif category == "Exploratory":
        return PROMPT_VULNERABILITY
    elif category == "Cooperative":
        return PROMPT_SIMPLE_AGREEMENT
    elif category == "Resolution":
        return PROMPT_INSIGHT
    
    return PROMPT_SIMPLE_AGREEMENT # Fallback
```

并在所有 prompt 统一注入当前细分 behavior 帮助微调语气：`[Behavior Subtype]: {behavior_subtype}`。

---

### 4.2 模板 1：PROMPT_ACTIVE_DEFENSE（主动防御型：A1-A2, B1-B7）

- **诊断**：来访者在积极反驳、推卸责任或表达绝望。
- **核心任务**：挖掘他们的逻辑支点或情感防御机制。
- **模板约束 (Prompt 2.0 第一人称沉浸式)**：
```
# Role
You ARE the patient. You are sitting in the therapy room. You are not an AI, not an observer, and not a writer.

# Task
The dialogue is COMPLETE — it includes your final response at the end.
Infer the defensive inner monologue that ran through your mind BEFORE you spoke.

What is the raw emotion or fear behind your defensive walls right now? Write the thought naturally, as if you are talking to yourself.
You are NOT simply reacting — you are guarding something.

Please ensure the monologue is written entirely from the "I" perspective of the client, avoiding any clinical detachment or third-person summary.

# Your Context
[Problem Type]: {problem_type}
[Situation]: {situation}
[Your Persona/Background]: {persona_summary}
[Behavior Subtype]: {behavior_subtype}
```

---

### 4.3 模板 2：PROMPT_EVASION（回避脱离型：C1-C4, D1-D2）

- **诊断**：来访者在隐瞒、转移话题或假配合。
- **核心任务**：无视表面字眼的敷衍，深挖被刻意压制的未说之语。
- **模板约束 (Prompt 2.0 第一人称沉浸式)**：
```
# Task
The dialogue is COMPLETE — it includes your final response at the end.
You are answering evasively, changing the subject, or giving pseudo-compliance.

Reveal what you are deliberately NOT saying. What thoughts, fears, or resentments did you consciously suppress when you chose to retreat or evade?
Focus entirely on the HIDDEN subtext beneath the surface interaction.
2-3 sentences max.

Please ensure the monologue is written entirely from the "I" perspective of the client, avoiding any clinical detachment or third-person summary.
```

---

### 4.4 模板 3：PROMPT_VULNERABILITY（脆弱探索型：E1）

- **诊断**：来访者在倾诉，内心还有未解决的沉重矛盾。
- **核心任务**：展现痛苦的自我挖掘。
- **模板约束 (Prompt 2.0 第一人称沉浸式)**：
```
# Task
The dialogue is COMPLETE — it includes your final response at the end.
You are actively exploring your own emotions or vulnerabilities without resisting.
Show your internal searching process and the heavy, unresolved ambivalence you feel.
This is an emotional stream of consciousness, struggling but open.

Please ensure the monologue is written entirely from the "I" perspective of the client, avoiding any clinical detachment or third-person summary.
```

---

### 4.5 模板 4：PROMPT_SIMPLE_AGREEMENT（简单顺从型：E2）

- **诊断**：自然的接受，简单的回答，无心理负担。
- **核心任务**：只给出极简确认。
- **模板约束 (Prompt 2.0 第一人称沉浸式)**：
```
# Task
The dialogue is COMPLETE — it includes your final response at the end.
You are simply accepting the therapist's logic, answering a question, or cooperating.
There is NO hidden agenda, NO deep psychological defense, and NO complex trauma response here.

CRITICAL INSTRUCTION: 
Write EXACTLY 1 to 2 very short, natural sentences. Keep it light and strictly surface-level. 
DO NOT over-analyze or manufacture psychological burdens.

Please ensure the monologue is written entirely from the "I" perspective of the client, avoiding any clinical detachment or third-person summary.
```

---

### 4.6 模板 5：PROMPT_INSIGHT（领悟决断型：E3）

- **诊断**：来访者获得了顿悟或承诺改变。
- **核心任务**：捕捉视角转换的瞬间（"Aha moment"）。
- **模板约束 (Prompt 2.0 第一人称沉浸式)**：
```
# Task
The dialogue is COMPLETE — it includes your final response at the end.
You have just reached a moment of insight or are making a concrete commitment to change.
Capture the exact cognitive shift, the sense of relief, or the crystallization of determination that occurred internally just before you spoke.

Please ensure the monologue is written entirely from the "I" perspective of the client, avoiding any clinical detachment or third-person summary.
```

---

## 五、最新评估报告 (Prompt 2.0)

针对 Prompt 2.0 进行了全量跑测与 LLM-as-a-Judge 评估（详见 `evaluate_inner_monologue.py`）：
- **核心结论**：第一人称沉浸式视角（`You ARE the patient.`）彻底解决了此前 AI 出现的“学术分析”口吻，获得了 **3.9~4.3 / 5.0** 的极佳平均分。
- **优点**：能够精准控制在一两句话的表面附和（针对 Simple Agreement）或生成贴合语境的不满与内心活动（并非仅仅复述发言），且与最终脱口而出的话语无缝桥接。
- **待优化项**：
  1. 需要在 pipeline 前特判跳过极短的、无意义的寒暄（如只有“Hi.”），以防诱发模型产生动作幻觉。
  2. 修复 `verify_psyfire_prompt.py` 中对 AnnoMI `resistance_turn` 的抓取逻辑，确保覆盖对抗类对话。

---

## 六、文件变更列表

| 操作 | 文件 | 说明 |
|------|------|------|
| [NEW] | `workspace/scripts/annotate_resistance.py` | utterance 级别批量分类 |
| [NEW] | `workspace/scripts/extract_persona.py` | 读取全量 transcript 提取动态 Patient Persona |
| [NEW] | `workspace/scripts/evaluate_inner_monologue.py` | LLM-as-a-Judge 细粒度自动化校验新生成数据质量 |
| [MODIFY] | `workspace/scripts/verify_psyfire_prompt.py` | 重构为 5 个独立的第一人称沉浸式模板及新的选择器，并注入 Persona |

---

## 七、验证流程

```bash
# Step 1: 提取 Persona
python scripts/extract_persona.py

# Step 2: Inner Monologue 生成 (全量跑测)
python scripts/verify_psyfire_prompt.py --all-cases --stride 10

# Step 3: 自动化客观验证
python scripts/evaluate_inner_monologue.py --samples-per-class 10
```
