# llm_simu_client

心理咨询模拟患者（Inner Monologue）研究项目 — 基于 Inner Monologue 的动机推理框架，训练 LLM 真实模拟心理咨询患者（含阻抗行为）。

---

## 目录结构

```
llm_simu_client/
├── workspace/          ← 主代码仓库
│   ├── scripts/        ← 数据生成、训练辅助脚本
│   ├── src/            ← 核心推理引擎（context_inference.py）
│   ├── train_config/   ← LLaMA-Factory 训练 YAML 配置
│   ├── dataset/        ← workspace 用到的数据（AnnoMI-labeled.json 等）
│   └── results/        ← 生成结果（inner_monologue_dataset.json 等）
│
├── data/               ← 原始数据统一目录
│   ├── raw/
│   │   ├── AnnoMI/     ← AnnoMI 原始 CSV（附带独立 git 历史）
│   │   └── RED/        ← Reddit 情感数据集原始 CSV（大文件）
│   ├── processed/      ← 处理后的 AnnoMI- JSON 文件
│   └── docs/           ← 数据处理过程文档与报告
│
├── data_scripts/       ← 数据预处理脚本
│   ├── csv_to_json.py
│   ├── filter_high_resistance.py
│   ├── extract_simple_resistance.py
│   └── psyfire_labeling.py
│
├── notes/              ← 研究笔记（Obsidian vault）
├── paper/              ← 相关文献 PDF
└── README.md
```

---

## 研究方向

**核心假设**：在心理咨询中，患者的阻抗行为（Resistance）来自于内在的心理动机，而非随机的语言输出。通过显式地建模患者在说话之前的内心独白（Inner Monologue），可以让 LLM 更真实地模拟患者行为。

**技术路径**：
1. 用 GPT/DeepSeek 逆向生成 Inner Monologue 数据（Phase 1-2 ✅）
2. 用 SFT 将"先想后说"能力蒸馏到小模型（Phase 3 🚧）
3. 用 DPO 修正"治愈幻觉"（内心挣扎 → 最终仍顺从），强化阻抗一致性

---

## 快速开始

### 生成 Inner Monologue 数据集

```bash
cd workspace
pip install openai python-dotenv

# 全量生成（stride=5，约 402 条）
python scripts/verify_psyfire_prompt.py --all-cases --stride 5
```

### 准备训练数据

```bash
# 转换为 LLaMA-Factory 格式
python scripts/prepare_sft_data.py --output-dir ~/LLaMA-Factory/data/
```

### 服务器训练

```bash
# 1. SSH 进服务器后一键配环境
bash workspace/scripts/setup_env.sh

# 2. 开始 SFT 训练
llamafactory-cli train workspace/train_config/qwen25_7b_sft.yaml
```

---

## 数据集说明

| 数据集 | 位置 | 说明 |
|---|---|---|
| AnnoMI-labeled.json | `workspace/dataset/` | PsyFIRE 阻抗标注，32 个 transcripts |
| inner_monologue_dataset.json | `workspace/results/` | 生成的 Inner Monologue 训练集（402条）|
| AnnoMI 原始 CSV | `data/raw/AnnoMI/` | 原始数据（含 git 历史）|
| RED 原始数据 | `data/raw/RED/` | Reddit 情感数据集（大文件，约 4GB）|
