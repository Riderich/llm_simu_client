# MI 取向最终 Profile 设计讲解报告

> **版本**：v1.0（讨论稿，可随实现与论文叙事迭代）  
> **定位**：进入训练数据集的 **最终 Profile**（来访者侧、MI 理论对齐）；与仅用于生成 COT 的 **background profile** 区分。  
> **日期**：2026-04-26

---

## 1. 报告目的

本报告说明：

1. **为何**以 **动机式访谈（Motivational Interviewing, MI）** 作为最终 Profile 的**唯一主理论轴线**；  
2. **Profile 长什么样**（字段、枚举、长度与稳定性约束）；  
3. **与 CoT（Belief / Intention）及 DBIA 叙事**如何分工；  
4. **标注与生成时**的注意点及**完整示例**。

---

## 2. 背景：我们要 Profile 解决什么问题

本项目的模拟对象是 **咨询情境下的来访者**。训练目标之一是：模型在生成外显回复前，经历 **与角色一致的内在过程**（如 Belief → Intention），使阻抗/合作等行为 **可解释、可条件化、可复现**。

因此，Profile 需要承载的是：

- **跨轮次相对稳定**的「这个人是谁、在乎什么、在变与不变之间如何拉扯、对哪些沟通方式敏感」；  
- 而不是某一两句对话的临时情绪（后者更适合放在 **每轮 CoT** 里）。

---

## 3. 为何主理论选 MI（而非默认采用 CBT 式「列法」）

### 3.1 文献中常见的 CBT/CCD 式做法

大量工作（例如基于 Beck **认知概念化图 CCD** 的患者模拟）将 profile 组织为 **核心信念、中间信念、自动思维、情绪、行为** 等条目。其优势是 **临床教科书结构清晰、易对照 Beck 体系**。

### 3.2 为何本项目仍以 MI 为主组织 Profile

本项目核心任务贴近 **咨询互动中的阻抗与合作、动机的矛盾与不和谐（discord）**。在 **角色扮演与条件化提示** 的视角下：

- **MI 的核心构造**（矛盾心理、价值、目标、不和谐敏感点）更贴近 **来访者主观体验与对话策略敏感点**，便于以 **第一人称心理内容** 约束模型；  
- **CBT 概念化**在常见写法上更偏 **治疗师侧解构工具**（第三人称、机制拆解）。并非不能改写为第一人称后使用，但默认「列法」容易让模型输出 **分析报告口吻** 而非 **活人说话**。

**论文中可表述的设计原则**：Profile 选取 **最能表征来访者主观动机场与互动敏感点** 的理论语言；故采用 **MI 对齐结构**。同时可承认文献中 CBT/CCD 路线的普遍性，并说明本项目为 **任务对齐** 所作的有理由选择。

---

## 4. 概念边界：三类产物不要混

| 名称 | 用途 | 理论主轴线 |
|------|------|------------|
| **最终 Profile（本文）** | 写入数据集、作为 **Desire** 层稳定条件 | **MI** |
| **Background profile（若保留）** | 中间态，用于辅助生成/补标 COT；可迭代 | 可与最终 Profile 不同，但需命名区分 |
| **CoT（Belief / Intention）** | 每轮动态推理，对齐 DBIA 中的 B、I | 过程层，不替代 Profile |

---

## 5. MI Profile 顶层结构（四块）

为兼顾 **学术可读性** 与 **短、稳、可解析**，采用 **外层四块 + 块内短槽位**：

1. `demographics` — 人口学与最小社会背景（非 MI 专有，但为通用临床记录层）  
2. `focus_of_change` — **改变焦点**（MI：在谈「什么」上的改变或犹豫）  
3. `mi_core` — **MI 核心心理构造**（矛盾、价值、不和谐敏感点）  
4. `style` — **外显对话风格**（增强自然度，非 MI 理论核心但实用）

---

## 6. 字段说明与填写规范

### 6.1 `demographics`

| 子字段 | 类型 | 说明 |
|--------|------|------|
| `age_band` | 枚举 | `child` \| `teen` \| `young_adult` \| `adult` \| `older_adult` \| `unknown` |
| `gender` | 枚举 | `female` \| `male` \| `nonbinary` \| `unknown` \| `prefer_not` |
| `role_context` | 短句 | 职业/身份/处境，**≤60 字**（中文）或等价英文长度 |
| `social_situation_tags` | 标签数组 | 如 `work`, `family`, `relationship`, `health`, `legal`, `financial`，**2～5 个** |

缺证据时：在句末标注 `(inferred)`。

---

### 6.2 `focus_of_change`

对应 MI 中会谈的 **改变议题焦点**（不一定是「已决定改变」）。

| 子字段 | 类型 | 说明 |
|--------|------|------|
| `target_behavior_or_outcome` | 1 句 | 来访者在考虑或摇摆的 **具体改变对象**（行为/状态/决定） |
| `why_now` | 0～1 句 | 为何 **此刻** 进入对话（可选） |

---

### 6.3 `mi_core`（MI 理论主承载）

#### （1）`ambivalence` — 矛盾心理两侧

MI 强调 **change talk** 与 **sustain talk** 所反映的 **矛盾**（非对错判断，而是共存动机）。

| 子字段 | 类型 | 说明 |
|--------|------|------|
| `sustain_talk_themes` | 2～4 条 bullet | **维持现状**的理由、顾虑、恐惧（每条 ≤40 字为宜） |
| `change_talk_themes` | 1～4 条 bullet | **倾向改变**的愿望、好处、担忧的另一侧（每条 ≤40 字） |

不要求与逐字稿中的语言学分类一一对应；Profile 层是 **稳定主题归纳**。

#### （2）`values_and_goals` — 价值与目标

MI 常通过 **联结价值** 促发改变动机。

| 子字段 | 类型 | 说明 |
|--------|------|------|
| `core_values` | 2～4 条 bullet | 最在意的价值（如尊严、安全、关系、自主） |
| `goals_in_life_or_role` | 1～3 条 bullet | 与身份/人生阶段相关的目标 |

#### （3）`discord_profile` — 不和谐 / 防御敏感点（互动层）

对应 MI 中 **discord**（关系或对话中的张力、抵触体验），用于约束「咨询师怎么说容易炸/怎么更容易合作」。

| 子字段 | 类型 | 说明 |
|--------|------|------|
| `sensitive_triggers` | 2～4 条 bullet | 易触发防御、反驳、沉默、敷衍的 **沟通方式或内容** |
| `preferred_engagement` | 0～3 条 bullet | 更容易建立 **合作与安全感** 的沟通特征（可选） |

---

### 6.4 `style` — 对话风格（表现层）

**非 MI 核心理论**，但可提升 **同一角色跨轮一致性** 与 **自然度**。

| 子字段 | 类型 | 说明 |
|--------|------|------|
| `interaction_style` | 枚举 | `plain` \| `reserved` \| `verbose` \| `upset` \| `tangent` \| `pleasing` \| `mixed` |
| `tone_note` | 0～1 句 | 补充说明，可选 |

---

## 7. 稳定性、可解释性与论文叙事

1. **结构化**：关键心理内容以 **bullet + 上限** 为主，避免单块长散文漂移。  
2. **理论命名**：矛盾侧明确使用 **sustain / change talk themes**；互动敏感点使用 **discord** 语言，便于与 MI 文献对照。  
3. **与 CoT 分工**：Profile **不**承担「本轮咨询师具体说了什么」的推理；该部分在 **Belief** 中完成，并应 **引用** `mi_core` 中具体 bullet。  
4. **信息泄露**：`focus_of_change` 与 `mi_core` 只写 **当前叙事已可支撑** 或合理 `(inferred)` 的稳定内容；**不把后文才揭晓的情节**写进 Profile。

---

## 8. 与 DBIA 的对应（简述）

| DBIA 层 | 与 MI Profile 的关系 |
|---------|----------------------|
| **Desire** | 主要由 **MI Profile** 提供（价值观、矛盾侧、改变焦点、discord 敏感点） |
| **Belief** | 每轮：咨询师话语 → 解读与触发（应回扣 Profile 中的具体要点） |
| **Intention** | 每轮：选择反应策略（可与阻抗/合作细粒度标签对齐） |
| **Action** | 外显回复 |

---

## 9. 完整 JSON 示例（虚构）

```json
{
  "demographics": {
    "age_band": "young_adult",
    "gender": "female",
    "role_context": "互联网公司产品运营，近期团队变动与绩效压力较大。",
    "social_situation_tags": ["work", "health", "family"]
  },
  "focus_of_change": {
    "target_behavior_or_outcome": "是否在现阶段向公司申请调岗或先请短假休整，以缓解失眠与心慌。",
    "why_now": "上周例会上的公开对比让她感到羞辱与失控。"
  },
  "mi_core": {
    "ambivalence": {
      "sustain_talk_themes": [
        "一旦示弱会被边缘化，失去掌控感。",
        "担心休息或调岗影响收入与评价。 (inferred)"
      ],
      "change_talk_themes": [
        "不想再硬扛，希望睡眠与身体状态稳定。",
        "希望被理解不是偷懒。"
      ]
    },
    "values_and_goals": {
      "core_values": ["自尊与独立", "经济安全", "被公平对待"],
      "goals_in_life_or_role": ["在团队中保持可靠形象", "一年内恢复可持续工作节奏"]
    },
    "discord_profile": {
      "sensitive_triggers": [
        "被与其他人公开对比、被暗示不努力。",
        "未先共情就直接给建议或下结论。"
      ],
      "preferred_engagement": [
        "先肯定其付出与难处，再一起探索选项。"
      ]
    }
  },
  "style": {
    "interaction_style": "reserved",
    "tone_note": "话不多，被戳痛处时语气容易变尖锐。 (inferred)"
  }
}
```

---

## 10. 实施清单（供工程与标注）

- [ ] 定稿 JSON Schema（含 `maxItems`、字符串 `maxLength`）并在生成后做 **schema 校验**  
- [ ] Prompt 中为每个子字段附 **一句定义**（对齐 MI 术语，减少模型自创维度）  
- [ ] 抽样人工审：**discord** 是否与对话中实际阻抗模式一致；**ambivalence** 两侧是否 **同时存在**（否则不像 MI 意义上的矛盾）  
- [ ] 与 **RECAP 阻抗/合作标签** 做一致性抽查（Profile 不应与多数轮次的标签系统性冲突）

---

## 11. 参考文献（入门）

- Miller, W. R., & Rollnick, S. *Motivational Interviewing*（建议采用团队使用的版本，如第三版及以后）。  
- 与 **change / sustain talk**、**discord**、**values** 相关的章节可直接支撑本 Profile 各块命名与写法。

（具体版次与页码以团队统一引用为准。）

---

## 12. 修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-04-26 | 初稿：MI 主理论、四块结构、字段说明与示例 |
