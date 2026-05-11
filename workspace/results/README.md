# `workspace/results/` 产出说明

心理咨询模拟患者项目：**平表标注、对话视图、Profile、CoT、RECAP/ExTES 实验** 的统一输出根目录。  
命名规则：**子目录按用途分栏**；文件名 = `{数据集}_{内容}`，避免版本号堆在文件名里（版本记在 Git 与本文）。

---

## 目录一览

| 目录 | 含义 |
|------|------|
| **`labeled/`** | **平表**：一行一样本（二分类 / PsyFIRE 阻抗 / CBS 合作等），供训练与统计。 |
| **`views/`** | **整段对话视图**：按 `character_id` 聚合，轮级带标签（与平表可对齐）。 |
| **`cot/`** | **内心独白（CoT）** 生成结果。 |
| **`profiles/`** | **来访者 Background Profile**（LLM 抽取）。 |
| **`recap/`** | RECAP 专项：整段对话、重标队列与日志。 |
| **`extes/`** | ExTES 专项：`binary.json`（大文件，见 `.gitignore`）、`resist_fine.json`、`experiments/` 下消融与对比。 |
| **`reports/`** | 抽检与 spotcheck 说明（Markdown）。 |
| **`logs/`** | 跑批日志（含 `logs/profiles/`）。 |

---

## 核心文件速查

### 平表 `labeled/`

| 文件 | 内容 |
|------|------|
| `annomi_binary.json` | AnnoMI 全量二分类（来访者 utterance 级） |
| `annomi_resist.json` / `annomi_coop.json` | 阻抗 PsyFIRE / 合作 CBS |
| `esconv_utterances.json` | ESConv 全量 utterance + 二分类，供 CBS 脚本筛「合作」 |
| `esconv_resist.json` / `esconv_coop.json` | ESConv 阻抗细粒度 / CBS（合作侧） |
| `mesc_binary.json` | MESC 平衡二分类子集 |
| `mesc_resist.json` | MESC 阻抗 PsyFIRE（与 `views/mesc.json` 一致，**主统计用**） |
| `mesc_resist_legacy.json` | 旧流水线局部跑出的阻抗平表（条数可能偏少） |
| `mesc_coop.json` | 自视图导出的合作 CBS（与 fine 对齐） |
| `mesc_coop_all.json` | 历史全量 CBS API 跑批（条数多） |
| `recap_resist.json` / `recap_coop.json` | RECAP 阻抗映射 / 合作 CBS（抽样） |

### 对话视图 `views/`

| 文件 | 内容 |
|------|------|
| `annomi.json` / `esconv.json` / `mesc.json` | 各数据集整段对话 + 轮级标签 |

### 其它

| 路径 | 内容 |
|------|------|
| `cot/{annomi,esconv,mesc}.json` | CoT 样本 |
| `profiles/{annomi,esconv,mesc,recap,recap_dedup}.json` | Profile；`recap_dedup` 为按 dialogue 去重后的推荐版本 |
| `recap/dialogues.json` | RECAP 全量对话 + 部分句有标签 |
| `extes/resist_fine.json` | ExTES 阻抗细粒度 |
| `extes/binary.json` | ExTES 二分类平表（~129MB，**不提交 Git**） |

---

## 旧文件名对照（迁移用）

| 旧名 | 新名 |
|------|------|
| `annomi_full_binary_recap.json` | `labeled/annomi_binary.json` |
| `annomi_character_view.json` | `views/annomi.json` |
| `esconv_character_view.json` | `views/esconv.json` |
| `mesc_character_view.json` / `mesc_fine_labeled.json`（曾重复） | `views/mesc.json`（唯一） |
| `mesc_binary_clean.json` | `labeled/mesc_binary.json` |
| `recap_dialogues_fine.json` | `recap/dialogues.json` |
| `extes_binary.json` | `extes/binary.json` |
| `extes_resistance_fine.json` | `extes/resist_fine.json` |
| `profiles/*_profiles_v3b*.json` | `profiles/{annomi,esconv,mesc,recap,recap_dedup}.json` |
| `*_cot.json`（根目录） | `cot/*.json` |

---

## 维护脚本

| 脚本 | 作用 |
|------|------|
| `data_scripts/prepare_training_splits.py` | 从 `labeled/` / `views/` / `cot/` / `recap/` / `profiles/` 物化 `training_splits/` |
| `data_scripts/generate_recap_labeled_cot.py` | RECAP 监督轮 `<internal>` COT 批生成（→ `recap/recap_labeled_cot.json`） |
| `data_scripts/extract_mi_profile_pilot.py` | MI Profile 试点（→ `profiles/pilot_mi/`） |
| `data_scripts/extes_audit_and_review_packet.py` | ExtES 审计 + 人工复核包（→ `extes/extes_*_report.md`） |
| `workspace/scripts/run_profile_extraction.py` | Profile 抽取主入口（→ `profiles/*.json`） |

历史的 `build_character_view.py` / `export_*_flat.py` 等已在 git 历史中归档；当前 `labeled/` 与 `views/` 文件直接作为快照维护。

---

## 更新记录

| 日期 | 内容 |
|------|------|
| 2026-05-11 | training_splits/ 重组（`_queues/` + `_reports/`）；MI Profile pilot 归入 `profiles/pilot_mi/` |
| 2026-04-18 | 目录化（labeled/views/cot/…）、缩短文件名、合并重复 MESC 视图、ExTES 归入 `extes/` |
