# workspace/scripts

脚本按职责分组，`archive/` 存放已完成的一次性脚本。

---

## CLI 入口

| 脚本 | 用途 |
|------|------|
| `run_profile_extraction.py` | Background Profile 提取（支持 annomi / esconv / mesc / recap）|
| `run_binary_resistance_classification.py` | 二分类阻抗检测（RECAP 本地模型）|

---

## Pipeline 模块

| 目录 | 说明 |
|------|------|
| `profile_pipeline/` | Profile 提取：loaders, prompts, extractor, runner, client |
| `resistance_pipeline/` | 二分类：loaders, inference, runner |

---

## 数据集标注脚本

### 阻抗细粒度（A1-D2，RECAP 本地模型，GPU）

| 脚本 | 数据集 | 输出 |
|------|--------|------|
| `annomi_resistance_fine.py` | AnnoMI | `results/annomi_resistance.json` |
| `esconv_resistance_fine.py` | ESConv | `results/esconv_resistance.json` |
| `mesc_resistance_fine.py` | MESC | `results/mesc_resistance.json` |

### 合作细粒度（CBS2-8，Qwen API）

| 脚本 | 数据集 | 输出 |
|------|--------|------|
| `annomi_coop_cbs.py` | AnnoMI | `results/annomi_coop.json` |
| `esconv_coop_cbs.py` | ESConv | `results/esconv_coop.json` |
| `mesc_coop_cbs.py` | MESC | `results/mesc_coop.json` |
| `recap_coop_cbs.py` | RECAP | `results/recap_coop.json` |

---

## 生成与训练

| 脚本 | 用途 | 状态 |
|------|------|------|
| `generate_recap_inner_monologue.py` | RECAP 中文 Inner Monologue 生成 | 待启动 |
| `evaluate_inner_monologue.py` | LLM-as-a-Judge 质量评估 | 可用 |
| `merge_results.py` | 合并多数据集结果 | 工具 |
| `prepare_sft_data.py` | 组装 SFT 训练数据（`{context, internal, response}`）| 待启动 |

---

## 环境

| 脚本 | 用途 |
|------|------|
| `activate_recap_vllm.sh` | 激活 recap_vllm conda 环境（含 torch）|
| `setup_vllm_env.sh` | 初始化 vLLM 环境 |

---

## archive/

| 子目录 | 内容 |
|--------|------|
| `one_off/` | 已完成的一次性 fix / 分析脚本 |
| `cbs_classification/` | CBS 分类早期迭代版本 |
| `resistance_classification/` | 阻抗分类早期版本 |
| `data_processing/` | 原始数据预处理脚本 |
| `test/` | 早期测试脚本 |
