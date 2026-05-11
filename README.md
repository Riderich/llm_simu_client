# llm_simu_client

训练 LLM 真实模拟心理咨询来访者阻抗行为。  
核心链路：**细粒度标注 → Background Profile → Inner Monologue (COT) → SFT → DPO**

---

## 目录结构

```
llm_simu_client/
├── workspace/
│   ├── scripts/
│   │   ├── profile_pipeline/      ← Background Profile 提取 pipeline
│   │   ├── resistance_pipeline/   ← 二分类阻抗检测 pipeline（RECAP 模型）
│   │   ├── run_profile_extraction.py       ← Profile 提取 CLI 入口
│   │   ├── run_binary_resistance_classification.py  ← 二分类 CLI 入口
│   │   ├── {dataset}_resistance_fine.py    ← 各数据集 A1-D2 细粒度标注
│   │   ├── {dataset}_coop_cbs.py           ← 各数据集 CBS2-8 合作标注
│   │   ├── generate_recap_inner_monologue.py  ← RECAP 中文 IM 生成
│   │   ├── prepare_sft_data.py             ← SFT 数据组装
│   │   └── archive/               ← 已完成的一次性脚本
│   ├── dataset/                   ← 数据集文件（ESConv, MESC, AnnoMI 等）
│   ├── results/
│   │   ├── profiles/              ← Background Profile 输出
│   │   └── *.json                 ← 标注结果
│   └── prompts/                   ← Prompt 版本存档
│
├── data/
│   ├── raw/                       ← 原始数据（AnnoMI CSV 等）
│   └── processed/                 ← 处理后的 JSON（AnnoMI-full.json）
│
├── notes/                         ← 研究笔记（Obsidian vault）
│   └── meetings/                  ← 讨论日志 + 会议报告
│
├── ClientResistance-Model-Share/  ← RECAP 本地阻抗分类模型
└── paper/                         ← 参考文献
```

---

## 当前进展

→ 详见 [`notes/README.md`](notes/README.md)

| 数据集 | 二分类 | 阻抗细粒度 (A1-D2) | 合作细粒度 (CBS2-8) | Profile |
|--------|-------|------------------|------------------|---------|
| ESConv | ✅ 19,372 | ✅ 5,609 | ✅ 13,763 | ✅ 全量 |
| MESC | ✅ 18,436 | ✅ 1,608 | ✅ 16,828 | ✅ 全量 |
| AnnoMI | ✅ 6,708 | ✅ 1,290 | ✅ 5,418 | ✅ 全量（带标注上下文）|
| RECAP | ✅ 5,154 | ✅ 4,154 | ✅ 1,000 | — |

---

## 快速开始

### 环境

```bash
# 激活 recap_vllm conda 环境（含 torch / transformers）
source workspace/scripts/activate_recap_vllm.sh

# API Key（Qwen / DeepSeek）
cp workspace/.env.example workspace/.env  # 填入 key
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

### Background Profile 提取

```bash
python scripts/run_profile_extraction.py \
    --input  dataset/AnnoMI-full.json \
    --output results/profiles/annomi_profiles_full.json \
    --data-format annomi          # 自动加载细粒度标注作为上下文
```

### 细粒度标注（A1-D2 / CBS2-8）

```bash
# 阻抗（GPU 4，RECAP 本地模型）
python scripts/annomi_resistance_fine.py

# 合作（Qwen API）
DASHSCOPE_API_KEY=sk-xxx python scripts/annomi_coop_cbs.py
```

---

## 行为分类体系

→ 详见 [`notes/行为空间框架.md`](notes/行为空间框架.md)

- **阻抗（A1-D2，11类）**：A1-A2 争辩、B1-B7 否认、C1-C2 回避、D1-D2 忽视
- **合作（CBS2-8，7类）**：认同、请求、叙述、认知探索、情感探索、领悟、改变
