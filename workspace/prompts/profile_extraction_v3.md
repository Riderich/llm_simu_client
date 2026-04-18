# Profile Extraction Prompt v3
> 用途：从完整对话 transcript 提取来访者 Background Profile
> 适用数据：AnnoMI / ESConv / MESC / RECAP
> 更新日期：2026-04-10

---

## 版本演进

| 版本 | 核心变化 | 问题 |
|------|---------|------|
| v1（strict/null 版） | 无证据则返回 null | MESC 产生大量 null，不可用 |
| v2（no-null/inferred 版） | 无证据则推断 + `(inferred)` 标注 | 解决了 null 问题，但字段边界模糊导致重复 |
| **v3（field-boundary 版）** | 在 v2 基础上：① 明确三个重叠字段的边界；② 加入数量上限 | 当前版本 |

---

## v3 核心修改

### 问题根源（v2 的缺陷）

`resistance_drivers` / `ambivalence.against_change` / `values_and_stakes` 三个字段语义高度相近，
LLM 倾向于从三个角度重复表达同一件事。例如，"intellectual independence" 这个概念会同时出现在：
- `resistance_drivers`：为什么他反抗咨询师
- `ambivalence.against_change`：他不愿放弃什么
- `values_and_stakes`：他珍视什么

### v3 的字段边界定义

| 字段 | 关注点 | 回答的问题 | 不包含 |
|------|--------|-----------|--------|
| `resistance_drivers` | **触发机制** | 什么情境/咨询师行为激活阻抗？如何表现？ | 来访者珍视什么 |
| `ambivalence.against_change` | **内心情感力量** | 远离改变的情感拉力是什么？ | 具体失去什么 |
| `values_and_stakes` | **具体失去的对象** | 改变后会失去什么关系/角色/结果？ | 阻抗机制或情绪 |

### v3 的数量限制

| 字段 | v2 | v3 |
|------|-----|-----|
| `resistance_drivers` | 无上限 | **max 3** |
| `values_and_stakes` | 无上限 | **max 3** |
| `key_facts` | 无上限 | **max 5**，且只保留能预测下一句话的细节 |
| `ambivalence` | 无约束 | **各 1 句话** |

---

## Prompt 正文（EN）

见 `workspace/scripts/profile_pipeline/prompts.py` → `USER_TEMPLATE_EN`

---

## 设计决策说明

| 决策 | 理由 |
|------|------|
| 加入 FIELD BOUNDARIES 段落 | LLM 需要明确的任务边界才能不重复；只靠字段名和简短描述不够 |
| `resistance_drivers` 定义为"触发机制" | 区别于"价值观"，让字段内容直接服务于行为预测 |
| `key_facts` 加过滤标准 | "能预测下一句话"比"任何可验证细节"更贴合 COT 生成的用途；排除咨询师陈述和 resistance_drivers 已命名的模式实例 |
| `ambivalence` 各限 1 句 | 两个子字段说清楚张力的两端即可，多了就是重复 |
| 数量上限写进 prompt | 不写上限 LLM 会"尽量多写"，上限是最直接的控制手段 |
| 字段内部正交性规则（规则 7） | LLM 倾向于把同一个模式的每个实例都列出来（如最小化饮酒、最小化孤独、最小化愤怒），规则 7 要求合并为一条描述该模式的总结 |
