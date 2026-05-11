# LLM 模拟来访者 · 项目笔记

> 训练一个能真实模拟心理咨询来访者阻抗行为的 LLM。  
> 核心链路：**细粒度标注 → Background Profile → Inner Monologue (COT) → SFT → DPO**

---

## 当前状态（2026-05-10）

**阶段：RECAP 监督轮 COT 已落地；ExtES 筛选与 COT、最终总装待做**

| 任务 | 状态 |
|------|------|
| ESConv 细粒度标注（A1-D2 + CBS2-8） | ✅ 完成 |
| MESC 细粒度标注（A1-D2 + CBS2-8） | ✅ 完成 |
| ESConv Profile 生成（全量 1300条） | ✅ 完成 |
| MESC Profile 生成（全量 1019条） | ✅ 完成 |
| AnnoMI 细粒度标注（阻抗 A1-D2，1290条） | 🔄 后台运行（GPU 4） |
| AnnoMI 细粒度标注（合作 CBS2-8，5418条） | 🔄 后台运行（Qwen API） |
| AnnoMI Profile 生成（带标注版） | ⏳ 等标注完成后重跑 |
| **RECAP**：`profiles/recap.json` → 训练行 `profile_used` | ✅ 已并入 `prepare_training_splits` 产出 |
| **RECAP**：监督来访轮（阻抗/合作）`<internal>` COT | ✅ `recap/recap_labeled_cot.json`（4929 条）+ 划分 JSON 已合并字段 |

**下一步（数据总装）**：ExtES 质量筛选子集 → ExtES 的 Profile / COT（或与现有标签对齐的弱 COT）→ 与 RECAP + 临床 `cot/*.json` 统一 schema 后写入最终训练包 / dataloader 采样策略（`prepare_training_splits` 当前仍**不**合并 ExtES，见脚本内 `extes_note`）。

查看后台进度：
```bash
tail -5 workspace/results/profiles/logs/annomi_resistance_nohup.log
tail -3 workspace/results/profiles/logs/annomi_coop_nohup.log
```

---

## 数据概况

| 数据集 | 语言 | 二分类 | 阻抗细粒度 | 合作细粒度 | Profile |
|--------|------|-------|----------|----------|---------|
| ESConv | EN | ✅ 19,372 | ✅ 5,609 | ✅ 13,763 | ✅ 全量 |
| MESC | EN | ✅ 18,436 | ✅ 1,608 | ✅ 16,828 | ✅ 全量 |
| AnnoMI | EN | ✅ 6,708 | 🔄 1,290 | 🔄 5,418 | ⏳ 待重跑 |
| RECAP | ZH | ✅ 5,154 | ✅ 4,154 | ✅ 1,000 | ✅ `profiles/recap.json`（与划分合并） |

详细分布、文件路径 → [`数据集.md`](数据集.md)

---

## 文件导航

| 文档 | 内容 | 更新频率 |
|------|------|---------|
| [`研究总览.md`](研究总览.md) | 研究问题、理论框架、整体 pipeline 设计 | 里程碑级 |
| [`行为空间框架.md`](行为空间框架.md) | 14 类行为分类定义（A1-D2 / CBS2-8） | 框架变动时 |
| [`数据集.md`](数据集.md) | 各数据集状态、标注覆盖、文件路径 | 数据更新时 |
| [`技术方案演进.md`](技术方案演进.md) | 方案迭代历程、IM prompt 体系、经验教训 | 阶段性 |
| [`meetings/讨论日志.md`](meetings/讨论日志.md) | 内部讨论、工作记录时间线（追加） | 随时 |
| [`meetings/会议报告_*.md`](meetings/) | 对外正式报告 | 按会议 |

---

## 关键里程碑

| 日期 | 事件 |
|------|------|
| 2026-04-09 | AnnoMI 细粒度标注后台启动；notes 目录重构 |
| 2026-05-10 | RECAP：`recap_labeled_cot.json` 全量生成；`prepare_training_splits` 合并 `profile_used` + `internal` / `raw_cot` / `cot_prompt_key` |
| 2026-04-10 | [会议报告：Profile 设计与数据进展](meetings/会议报告_20260410.md) |
| 2026-03-26 | ESConv / MESC / RECAP profile 全量生成完成 |
| 2026-03-26 | ESConv + MESC 细粒度标注全量完成（100% 准确率）|
| 2026-03-19 | RECAP 数据入库；合作样本 E1/E2/E3 细分完成 |
| 2026-03-10 | ExTES 质量评估完成（阻抗率 6%，定为辅助语料）|

---

## 代码路径速查

| 内容 | 路径 |
|------|------|
| 训练划分与 RECAP COT 批处理 | `data_scripts/prepare_training_splits.py`、`data_scripts/generate_recap_labeled_cot.py`（仓库根执行） |
| 脚本 | `workspace/scripts/` |
| 数据集 | `workspace/dataset/` |
| 标注结果 | `workspace/results/` |
| Profile 结果 | `workspace/results/profiles/` |
| 后台日志 | `workspace/results/profiles/logs/` |
| 本地模型 | `ClientResistance-Model-Share/only_resistance_share_model` |
