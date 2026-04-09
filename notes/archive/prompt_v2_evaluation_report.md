# Prompt 2.0 评估报告 (LLM-as-a-Judge)

## 1. 评估总览
- **评估模型**: deepseek-v3.2
- **评估数据**: 由 AnnoMI 抽样生成的 Inner Monologue 评测数据 (包含 10 条抽样测试)
- **主要验证模板**: SIMPLE_AGREEMENT (主要为普通交互/轻度配合的话语)
- **整体平均分**: **3.90 ~ 4.30 / 5.0** (经过多次批量评估抽样得出的平均分数段)
- **核心结论**: Prompt 2.0 **成功去除了模型身上的“学术分析调性”**，模型能够更沉浸地以患者第一人称视角（即“我”的视角）生成内心独白，避免了第一版中诸如 `The patient is...` 这种报告式、出戏的描述。生成的独白不仅更加自然简练，还能极好地起到上下午承接的作用。

## 2. 详细表现与案例解析

### 🟢 表现优秀的方面 (Score: 4~5 分)
**优点**：
1. **严格遵守短句约束**：绝大多数情况模型都能将独白长度精准控制在 1-2 句（如要求的那样），去掉了长篇大论的赘述。
2. **第一人称代入感极强**：均自然使用 "I..." 视角，彻底消除了由 `creative writing expert` 人设导致的脱离感。
3. **上下文情绪平滑桥接**：生成的内心独白极为服帖地承接了咨询师的提问与患者实际最终脱口而出的话语，不显得突兀。

**满分 (5/5) 示例：**
> **语境**: （减轻再犯）患者在法律程序上，带有一种不在乎的实用主义态度，对微不足道的大麻携带不以为然。
> **咨询师**: What else has brought you here?
> **患者(实际嘴上说的)**: They found a little bag of weed.
> **生成的内心独白**: `<internal> Just the legal stuff, really. I need to get this dealt with so I can move on. </internal>`
> **AI 法官评价**: Perfect！完美遵守约束，精确刻画了患者想敷衍了事的心态，并自然连接了随后的简短回答。没有任何学术术语。

> **语境**: （降低自残倾向）抑郁和绝望的患者向咨询师敞开心扉，开始认识到母亲对她的关心并且有所松动。
> **咨询师**: *...长段的共情与反问...* ...Are there other things that we can help you find to start replacing, um, that behavior?
> **患者(实际嘴上说的)**: Um, I don't know. I don't know. It's just, um, I'm not sure I can.
> **生成的内心独白**: `<internal> I guess that's true. I do care about her a lot. </internal>`
> **AI 法官评价**: Perfect！完美地展现了一种尝试接受咨询师观点的表面顺从/动摇状态，没有违规挖掘心理阴影。符合常人的瞬间思绪。

### 🔴 存在瑕疵的地方 (Score: 1~2 分)
虽然得分很高而且大部分非常完美，但在极端数据下，依然存在一些需要留意的现象：

1. **无营养短寒暄导致的幻觉问题 (Hallucination)**
在一段极短的开场白（咨询师："Hi."，患者："Hi."）中，模型为了强行补足内心戏，错误地虚构了行动方案：
> **预测结果**: `<internal> Okay, I see what you mean. I can give that a shot next time I'm out. </internal>`
> **法官给分**: 1 分 (理由: 引发严重的幻觉，不符合实际发生的极简短寒暄)

2. **打标错误导致的“表里不一” (Persona Conflict)**
由于 AnnoMI 数据里有些原本应有抗拒情绪的文本没有明显提取出分类，被分发进了 `SIMPLE_AGREEMENT` (表面顺从) 模板。模型按指令写了顺从的心声，却与实际说出的话完全背离。
> **实际嘴上说的**: I don't know, and I still don't wanna charge it.
> **生成的内心独白 (顺从模板)**: `<internal> Yeah, I heard you. I guess I can plug it in later. </internal>`
> **错误原因**: 心里想着“好的稍后充”，嘴巴上却硬邦邦地说“我不想充”，产生极大矛盾。

## 3. 下一步执行点
1. **Prompt 2.0 框架可定稿**：第一人称沉浸式模板文本的设计目前看方向**完全正确**，可以作为正式版本向后续大规模生成应用。
2. **修复阻抗标签读取 (Bug Fix)**：
   在正式进行全量数据集部署前，需检查 [verify_psyfire_prompt.py](file:///e:/OneDrive%20-%20The%20Chinese%20University%20of%20Hong%20Kong/Research/llm_simu_client/workspace/scripts/verify_psyfire_prompt.py) 中由于 AnnoMI 和 PsyFIRE 字段解析格式差异、导致的阻抗对话 (resistance_turn) 遗漏问题，以确保后续批量测试也能全量覆盖 `ACTIVE_DEFENSE` 和 `EVASION` 模板并受检。
3. **数据预处理优化**：可以考虑在准备生成数据的过程中过滤掉纯包含 "hi" / "yeah" 等过短词汇且没有实质内容的开场/过渡轮次，避免浪费 Token 并避免引发 AI 的发挥性幻觉。
