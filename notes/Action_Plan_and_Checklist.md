# Inner Monologue 模拟患者项目 - 任务追踪清单

> 整理人：王铮
> 最后更新：2026-03-19
> 本文档记录了 Inner Monologue 生成与对齐训练项目的详细 Checklist 与下一阶段行动计划，并会在工作推进时持续核销。

---

## 📅 Action Plan (短期行动计划)

### 🚨 紧急待办 (Priority 1)
- [x] **修缮数据抽取逻辑 (verify_psyfire_prompt.py)**
  - [x] 修复抓取 `AnnoMI-labeled.json` 数据遗漏 `resistance_label` 标签的匹配问题，通过 `clean_annomi_labels.py` 一次性将中文转换为英文统一规范，确保真正的阻抗（抵抗分类）能被送进 `ACTIVE_DEFENSE` 或 `EVASION` 模板。
  - [x] 增加长度阀值过滤，跳过类似 "Hi." / "Yeah." 这种纯为了寒暄而没什么实质内容的短句 (分词数 < 4 且无阻抗属性)，防止 LLM 被迫生造内心活动（引起行动幻觉）。

### 🚀 中期目标 (Priority 2)
- [x] **RECAP 数据集入库与预处理**
  - [x] 获取 RECAP 标注数据（5154 条中文心理咨询对话，已解密）
  - [x] 构建中文标签到 A/B/C/D/E 框架的映射关系
  - [x] 实现 `process_recap.py` 对原始数据进行规范化处理
  - [x] 用 Qwen 对 1000 条"合作-未阻抗"样本进行 E1/E2/E3 细分（100% 完成）
- [ ] **RECAP Inner Monologue 全量生成**
  - [ ] 基于 5 套模板对 RECAP 5154 条样本生成中文 Inner Monologue
  - [ ] 设计中文版 Prompt 模板（对应英文版 5 套）
  - [ ] 部署后台批处理任务（建议用 DeepSeek-v3 降低成本）
- [ ] **AnnoMI/ESConv/MESC Inner Monologue 生成**
  - [ ] 将代码同步至服务器环境
  - [ ] 对三大英文数据集挂机跑出完整 Inner Monologue
- [ ] **准备对接 RECAP 模型权重**
  - [ ] 签署数据共享协议并获取 RECAP 作者（李安琪）开源的模型权重
  - [ ] Zero-shot 评估 RECAP 模型对 ESConv/MESC 的阻抗分类性能

### ✨ 长期里程碑 (Priority 3)
- [ ] **开启 SFT 训练**
  - 对这几批跑完了内心独白的优质数据进行组装清洗：最终格式须转变为 `<context> -> <internal_monologue> -> <response>` 并带上对应的标签。
  - 送入模型进行初阶段 SFT 训练。
- [ ] **DPO 对齐准备**
  - 在初步跑通后提取 Hard cases（例如心理活动和回复明显割裂、或是依然在配合咨询师而不懂反抗）。
  - 根据张鑫洁后续补充的文档清洗这些失败样本进行 DPO 偏好对齐优化惩罚。

---

## ✅ Checklist 全览

### 1. 理论与基建筹备
- [x] 行为空间框架定稿（结合 PsyFIRE 与 CBS，整理出 14 类细分）
- [x] 数据集调研与入库（ESConv, MESC, ExTES, AnnoMI）
- [x] 确定 Inner Monologue "三段式"链条架构
- [x] 设计出并改良了带有 5 套专属约束体系的第一人称沉浸式模板 (Active Defense, Evasion, Vulnerability, Simple Agreement, Insight)

### 2. 自动标注 Pipeline
- [x] **RECAP 数据集整合与细分**
  - [x] 获取 RECAP 数据集（5154 条中文真实心理咨询对话）
  - [x] 建立中文标签到英文框架（A/B/C/D/E1/E2/E3）的完整映射
  - [x] 用 Qwen 3.5 自动细分 1000 条"合作-未阻抗"样本：E1(409) / E2(490) / E3(101)
  - [x] 输出规范化数据文件：`workspace/dataset/RECAP.json`
- [ ] **准备 RECAP 模型权重对接**
  - [ ] 签署数据共享协议并获取模型权重
  - [ ] 评估 RECAP 模型对 ESConv/MESC 的 Zero-shot 性能
- [ ] **重构标注流程**
  - [ ] 如 RECAP 模型表现优异，直接使用其对 ESConv/MESC 进行自动标注以降低开销
  - [ ] 针对 RECAP 无法处理或表现不佳的类别，使用 LLM Few-shot 标注脚本兜底
- [ ] **人工复核质检**
  - [ ] 对自动生成的标签进行人工 Review，形成高质量 Ground Truth

### 3. Inner Monologue 批量生成
- [x] 升级 `verify_psyfire_prompt.py`：实现核心 5 大基准模板的逻辑分发与内容注入
- [x] 本地全量 Smoke Test 采样跑通
- [x] 完成并使用了 LLM 校验脚本 (`evaluate_inner_monologue.py`) 细读验证生成的新数据质量（平均分 4.30/5.0，去除了分析调性）
- [x] **【Prompt 2.0】构建** `extract_persona.py` 成功实现提取患者人情世故的动态 Persona，解决原先由于无背景设定导致的模型严重"角色脱离出戏"问题
- [x] **【Prompt 2.0】重写** 5 大 Inner Monologue 基准模板，转为沉浸式第一人称视角（`You ARE the patient`），有效提升独白自然度
- [x] **修复数据脱落幻觉 Bug**：通过统一英文化标签及过滤 $<4$ 个单词的寒暄节点，彻底解决了长尾和边界报错
- [x] **AnnoMI 全量生成完成**：153 条样本（resistance 30 + normal 123），所有样本均包含完整 `<internal>` + `ground_truth`
- [ ] **RECAP 中文 Inner Monologue 生成**：5154 条样本待生成（需设计中文版 5 套模板）
- [ ] 部署到服务器进行 ESConv/MESC 的全量生产
- [ ] 为 non-resistance 侧（E1/E2/E3）补充或映射 utterance 级标签，避免所有 normal case 默认落入 `SIMPLE_AGREEMENT`，提升 Exploratory / Resolution 段落的一致性

### 4. 模型训练与评估
- [ ] 构造训练集：`上下文 -> <internal> -> 回复 (并带上阻抗类别标签)`。
- [ ] SFT（监督微调），让模型学会前置推理范式。
- [ ] 提取 Hard Case，进行 DPO 偏好对齐训练，惩罚“治愈幻觉”与“逻辑断裂”。
- [ ] 确立评估体系并跑测（PsyFIRE 维度盲测、行为一致性等对照实验）。
