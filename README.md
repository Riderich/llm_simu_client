# llm_simu_client

训练 LLM 真实模拟心理咨询来访者的阻抗行为。  
核心链路：**细粒度标注 → Background Profile → Inner Monologue (COT) → SFT → DPO**

> 完整背景、设计与进度见 [`notes/`](notes/)（建议入门读 [`notes/入门指南.md`](notes/入门指南.md)）。

---

## 目录结构

```
llm_simu_client/
├── data_scripts/                  ← 仓库根执行的数据脚本
│   ├── prepare_training_splits.py        训练划分
│   ├── generate_recap_labeled_cot.py     RECAP 监督轮 COT
│   ├── extract_mi_profile_pilot.py       MI Profile 试点
│   └── extes_audit_and_review_packet.py  ExtES 审计 + 人工复核包
│
├── workspace/                     ← 主工作区（在此目录下执行的脚本）
│   ├── dataset/                   ← 数据集（ESConv / MESC / AnnoMI / RECAP / ExTES / _raw/）
│   ├── prompts/                   ← Prompt 模板（profile_extraction / mi_profile）
│   ├── schemas/                   ← Schema 定义
│   ├── results/                   ← 标注、Profile、CoT、训练划分等真源（详见目录内 README）
│   ├── scripts/
│   │   ├── run_profile_extraction.py             ← Profile 提取 CLI
│   │   ├── run_binary_resistance_classification.py ← 二分类阻抗
│   │   ├── run_resistance_fine_labeling.py       ← 阻抗细粒度
│   │   ├── run_cbs_labeling.py                   ← CBS 合作标注
│   │   ├── evaluate_inner_monologue.py           ← CoT 质量评估
│   │   ├── prepare_sft_data.py                   ← SFT 数据组装
│   │   ├── extes_local_screen_sharded_*.sh       ← ExTES 本地分片筛选
│   │   ├── profile_pipeline/                     ← Profile 提取模块
│   │   ├── resistance_pipeline/                  ← 阻抗 pipeline 模块
│   │   └── archive/                              ← 已完成/被取代的一次性脚本
│   ├── src/                       ← 共享代码（llm_client / context_inference）
│   ├── test_cases/                ← 历史测试用例
│   └── train_config/              ← LLaMA-Factory 训练 YAML
│
├── notes/                         ← 研究笔记（Obsidian vault）
├── paper/                         ← 论文与参考资料
└── ClientResistance-Model-Share/  ← RECAP 本地阻抗分类模型（不入 git）
```

---

## 当前进展

| 数据集 | 二分类 | 阻抗细粒度 (A1-D2) | 合作细粒度 (CBS2-8) | Profile |
|--------|-------|------------------|------------------|---------|
| ESConv | ✅ 19,372 | ✅ 5,609 | ✅ 13,763 | ✅ 全量 |
| MESC | ✅ 18,436 | ✅ 1,608 | ✅ 16,828 | ✅ 全量 |
| AnnoMI | ✅ 6,708 | ✅ 1,290 | ✅ 5,418 | ✅ 全量 |
| RECAP | ✅ 5,154 | ✅ 4,154 | ✅ 1,000 | ✅ + 监督轮 COT 4,929 |

下一步：MI Profile 设计验证 + ExtES 筛选子集与同构总装。详见 [`notes/README.md`](notes/README.md)。

---

## 快速开始

### 环境

```bash
source workspace/scripts/activate_recap_vllm.sh   # conda 环境（含 torch / transformers）
cp .env.example .env                              # 填入 DEEPSEEK_API_KEY / QWEN_API_KEY 等
```

### 二分类阻抗检测（RECAP 本地模型）

```bash
cd workspace
python scripts/run_binary_resistance_classification.py \
    --data-format annomi \
    --input dataset/AnnoMI-full.json \
    --output results/labeled/annomi_binary.json \
    --gpu 4
```

### Background Profile 提取（API LLM）

```bash
cd workspace
python scripts/run_profile_extraction.py --dataset annomi          # mesc / esconv / annomi / recap
```

### RECAP 监督轮 Inner Monologue（仓库根）

```bash
nohup python3 -u data_scripts/generate_recap_labeled_cot.py --workers 4 --sleep 0.15 \
  >> workspace/results/recap/recap_labeled_cot_nohup.log 2>&1 &
```

### MI Profile pilot

```bash
python3 data_scripts/extract_mi_profile_pilot.py --dry-run
python3 data_scripts/extract_mi_profile_pilot.py --max-dialogues 10 --seed 42
```

---

## 行为分类体系

→ 详见 [`notes/行为空间框架.md`](notes/行为空间框架.md)

- **阻抗（A1-D2，11 类）**：A1-A2 争辩、B1-B7 否认、C1-C2 回避、D1-D2 忽视
- **合作（CBS2-8，7 类）**：认同、请求、叙述、认知探索、情感探索、领悟、改变
