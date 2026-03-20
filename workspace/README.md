# LLM 心理咨询模拟患者 — Inner Monologue 训练框架

基于 AnnoMI 数据集，构建"先想后说"Inner Monologue 训练数据，并微调开源 LLM 使其能够真实模拟心理咨询患者（含阻抗行为）。

---

## 项目结构

```
workspace/
├── dataset/
│   ├── AnnoMI-labeled.json        # 主数据集（PsyFIRE 阻抗标注）
│   ├── ESConv.json
│   └── MESC_merged.json
├── src/
│   ├── context_inference.py       # 核心 API 推理引擎
│   └── test_case_selector.py
├── scripts/
│   ├── verify_psyfire_prompt.py   # Inner Monologue 数据集生成主脚本
│   ├── prepare_sft_data.py        # 数据格式转换（→ LLaMA-Factory alpaca）
│   ├── setup_env.sh               # 服务器一键配环境脚本（Linux）
│   ├── analyze_psyfire_results.py
│   └── run_tests.py
├── train_config/                  # LLaMA-Factory 训练 YAML 配置
│   ├── qwen25_7b_sft.yaml         # Qwen2.5-7B SFT（推荐首跑）
│   ├── deepseek_r1_7b_sft.yaml    # DeepSeek-R1-Distill SFT
│   ├── gemma2_9b_sft.yaml         # Gemma-2-9B SFT
│   └── qwen25_7b_dpo.yaml         # DPO 偏好对齐
├── results/
│   ├── inner_monologue_dataset.json  # ★ 生成的训练数据集（402条）
│   └── verify_inner_monologue.json
├── test_cases/
├── .env
└── README.md
```

---

## 数据集生成

### 环境配置

```bash
pip install openai python-dotenv
```

`.env` 配置：
```
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://yunwu.ai/v1
```

### 生成 Inner Monologue 数据集

```bash
# 验证模式（3条，确认输出格式）
python scripts/verify_psyfire_prompt.py --num-cases 3

# 全量生成（stride=5 采样，约 402 条）
python scripts/verify_psyfire_prompt.py --all-cases --stride 5

# 重跑 internal/gt 比值过高的案例（修正过长独白）
python scripts/verify_psyfire_prompt.py --rerun-high-ratio 20

# 对 ground_truth ≤ 5 词的案例重跑（使用 SHORT prompt）
python scripts/verify_psyfire_prompt.py --rerun-short-gt
```

**Prompt 策略（自动分流）：**
- `ground_truth ≤ 5 词` → `PROMPT_TEMPLATE_SHORT`：1-2 句即时情绪冲动
- `ground_truth > 5 词` → `PROMPT_TEMPLATE`：三层推理链

**数据输出格式：**
```
Context (对话历史) → <internal>内心独白</internal> → Response (ground_truth)
```

---

## 模型训练（LLaMA-Factory）

### 服务器环境搭建（4× NVIDIA A2000 12GB）

```bash
# SSH 进服务器后一键配环境
bash scripts/setup_env.sh
```

### 数据格式转换

```bash
# 本地执行：上传数据到服务器
scp results/inner_monologue_dataset.json user@server:~/LLaMA-Factory/data/

# 服务器执行：转换为 alpaca 格式
python scripts/prepare_sft_data.py \
  --output-dir ~/LLaMA-Factory/data/ \
  --llamafactory-dir ~/LLaMA-Factory   # 自动注册 dataset_info.json
```

### SFT 训练

```bash
# Qwen2.5-7B（推荐首跑，单卡 QLoRA 4bit，约 30-60 分钟）
CUDA_VISIBLE_DEVICES=0 llamafactory-cli train train_config/qwen25_7b_sft.yaml

# DeepSeek-R1-Distill-Qwen-7B（CoT 蒸馏模型，适合 <internal> 格式）
CUDA_VISIBLE_DEVICES=1 llamafactory-cli train train_config/deepseek_r1_7b_sft.yaml

# Gemma-2-9B（推理能力强，建议双卡）
llamafactory-cli train train_config/gemma2_9b_sft.yaml
```

### DPO 对齐

```bash
# 在 SFT checkpoint 基础上做偏好对齐（修正"治愈幻觉"）
llamafactory-cli train train_config/qwen25_7b_dpo.yaml
```

---

## 技术细节

### 角色映射
- `user` → 咨询师（Therapist）
- `assistant` → 患者（Patient/Client）

### 数据集统计（stride=5）
- 总条数：402
- normal：376 / resistance：26
- Short GT（≤5词）：172 条，使用 SHORT prompt
- Long GT（>5词）：230 条，使用 LONG prompt

### PsyFIRE 阻抗分类体系
争辩（质疑/贬低）/ 否认（责备/不同意/找借口/轻视/悲观/犹豫）/ 回避（极简对话/设限）/ 忽略（注意力不足/偏题）

---

## 许可证

研究项目，仅供学术使用。
