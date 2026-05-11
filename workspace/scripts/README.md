# workspace/scripts

在 `workspace/` 下执行的脚本（仓库根执行的脚本在 [`data_scripts/`](../../data_scripts/)）。

## CLI 入口

| 脚本 | 用途 | 接口 |
|------|------|------|
| `run_profile_extraction.py` | Background Profile 提取（mesc / esconv / annomi / recap） | API LLM |
| `run_binary_resistance_classification.py` | 二分类阻抗检测 | RECAP 本地模型（GPU） |
| `run_resistance_fine_labeling.py` | 阻抗 A1-D2 细粒度标注 | RECAP 本地模型（GPU） |
| `run_cbs_labeling.py` | 合作 CBS2-8 细粒度标注 | Qwen / DeepSeek API |
| `evaluate_inner_monologue.py` | CoT 质量 LLM-as-Judge 评估 | API LLM |
| `prepare_sft_data.py` | 组装 SFT 训练数据（→ LLaMA-Factory alpaca 格式） | 离线 |
| `psychfire_resistance_fine_prompt.py` | 阻抗细粒度 prompt 工具（被 pipeline 引用） | 库 |

## ExtES 本地筛选

```bash
bash extes_local_screen_sharded_start.sh         # 启动分片本地筛选
bash extes_local_screen_sharded_monitor_loop.sh  # 持续监控进度
```

## 模块化 pipeline

| 目录 | 内容 |
|------|------|
| `profile_pipeline/` | loaders / prompts / extractor / runner / io_utils；共享 `LLMClient` 自 `workspace/src/llm_client.py` re-export |
| `resistance_pipeline/` | loaders / inference / runner / fine_prompts |

## 环境脚本

| 脚本 | 用途 |
|------|------|
| `activate_recap_vllm.sh` | 激活 recap_vllm conda 环境 |
| `setup_vllm_env.sh` | 初始化 vLLM 环境 |

## archive/

已完成或被取代的一次性脚本，仅供参考、不再维护：

| 子目录 | 内容 |
|--------|------|
| `cbs_classification/` | CBS 分类早期迭代版本（15 份） |
| `resistance_classification/` | 阻抗分类早期版本（5 份） |
| `data_processing/` | 早期数据预处理（3 份） |
| `superseded/` | 被新 CLI 取代的 per-dataset 入口（8 份） |
| `one_off/` | 一次性 fix / 分析脚本（10 份） |
| `test/` | 早期测试脚本（8 份） |
