# RECAP vLLM 推理环境配置指南

> 用于高效批量标注 ESConv/MESC 数据

---

## 📋 方案概述

### 为什么用 vLLM？

| 特性 | Transformers (当前) | vLLM (新方案) |
|------|---------------------|---------------|
| 推理速度 | ~2-3秒/条 | ~0.1秒/条 (提升 20-30倍) |
| 批处理 | 需手动实现 | 内置 Continuous Batching |
| 显存效率 | 一般 | PagedAttention 优化 |
| 多卡并行 | 复杂 | 内置 Tensor Parallelism |

### 架构图

```
输入数据 (JSON)
    ↓
数据加载器 (RecapDataLoader)
    ↓
vLLM 推理引擎 (RecapVLLMInference)
    ├── 二分类模型 (binary_share_model)
    │       └── 阻抗 / 合作
    └── 细分类模型 (only_resistance_share_model)
            └── 13类阻抗细分类别
    ↓
输出结果 (JSON)
```

---

## 🔧 环境配置

### 前置条件

- Python 3.8+ (已配置在 `/data5/zxj/llama_3_1/`)
- CUDA 11.8+ 或 12.1+ (当前系统: CUDA 12.x)
- GPU 显存: 单卡 ≥ 16GB（推荐 24GB+）

### 安装步骤

```bash
# 1. 运行配置脚本
bash workspace/scripts/setup_vllm_env.sh

# 或者手动安装
data5/zxj/llama_3_1/bin/pip install vllm --extra-index-url https://download.pytorch.org/whl/cu121
```

### 验证安装

```bash
# 使用指定环境运行 dry run
data5/zxj/llama_3_1/bin/python workspace/scripts/recap_vllm_inference.py --dry-run
```

预期输出：
```
================================================================================
DRY RUN MODE (不加载模型)
================================================================================
⚠️  vLLM not installed. Running in mock mode.
...
✅ Dry run 完成！代码结构验证通过。
```

---

## 🚀 使用方法

### 1. 快速测试（Dry Run）

```bash
cd /data5/zxj/llm_simu_client/workspace
/data5/zxj/llama_3_1/bin/python scripts/recap_vllm_inference.py --dry-run
```

### 2. 标注 ESConv 数据

```bash
cd /data5/zxj/llm_simu_client/workspace

# 基础用法（二分类 + 细分类）
/data5/zxj/llama_3_1/bin/python scripts/recap_vllm_inference.py \
    --input dataset/ESConv.json \
    --output results/esconv_labeled.json \
    --data-format esconv \
    --batch-size 32

# 只二分类（更快）
/data5/zxj/llama_3_1/bin/python scripts/recap_vllm_inference.py \
    --input dataset/ESConv.json \
    --output results/esconv_binary.json \
    --data-format esconv \
    --no-fine-grained
```

### 3. 标注 MESC 数据

```bash
/data5/zxj/llama_3_1/bin/python scripts/recap_vllm_inference.py \
    --input dataset/MESC_merged.json \
    --output results/mesc_labeled.json \
    --data-format esconv \
    --batch-size 32
```

### 4. 多卡并行（需要 2 张卡）

```bash
# 使用 2 张 GPU 并行
/data5/zxj/llama_3_1/bin/python scripts/recap_vllm_inference.py \
    --input dataset/ESConv.json \
    --output results/esconv_labeled.json \
    --tp-size 2 \
    --batch-size 64
```

---

## 📊 性能预估

### 单卡 A6000 (48GB)

| 数据量 | 批大小 | 预计时间 | 显存占用 |
|--------|--------|----------|----------|
| 1,000 条 | 32 | ~2 分钟 | ~16GB |
| 10,000 条 | 32 | ~20 分钟 | ~16GB |
| 30,000 条 | 64 | ~50 分钟 | ~32GB |

### 双卡并行

| 数据量 | 批大小 | 预计时间 | 显存占用 |
|--------|--------|----------|----------|
| 30,000 条 | 64 | ~30 分钟 | ~32GB × 2 |

---

## 📁 文件说明

```
workspace/scripts/
├── recap_vllm_inference.py      # 主推理脚本
├── setup_vllm_env.sh            # 环境配置脚本
└── test_recap_model_official.py # 测试脚本（fallback）

notes/
└── vllm_setup_guide.md          # 本文档
```

---

## ⚠️ 注意事项

### 显存管理

- vLLM 会占用指定比例的显存（默认 90%）
- 确保使用 GPU 时没有其他大模型在运行
- 如果显存不足，可以减小 `--batch-size` 或 `--gpu-memory-utilization`

### 模型路径

确保模型文件存在：
```
ClientResistance-Model-Share/
├── binary_share_model/           # 二分类模型
└── only_resistance_share_model/  # 细分类模型
```

### 输出格式

标注结果 JSON 结构：
```json
{
  "sample_id": "0",
  "context": "咨询师：...\n来访者：...",
  "response": "来访者发言内容",
  "binary_label": "阻抗",
  "fine_label": "否认-不认同",
  "metadata": { ... }
}
```

---

## 🔍 故障排查

### vLLM 安装失败

```bash
# 检查 CUDA 版本
nvcc --version

# 尝试安装指定版本
pip install vllm==0.7.3 --extra-index-url https://download.pytorch.org/whl/cu121
```

### 显存不足 (OOM)

```bash
# 减小批大小
--batch-size 16

# 降低显存利用率
--gpu-memory-utilization 0.8
```

### 模型加载失败

```bash
# 检查模型路径
ls -la ../ClientResistance-Model-Share/binary_share_model/

# 使用绝对路径
--binary-model /data5/zxj/llm_simu_client/ClientResistance-Model-Share/binary_share_model
```

---

## 📝 后续计划

1. **环境配置** ← 当前阶段（等待同学协调 GPU）
2. **Dry Run 测试** ← 已完成 ✅
3. **ESConv 批量标注**
4. **MESC 批量标注**
5. **标注质量验证**（抽样人工 review）

---

**当前状态**: 代码已就绪，等待 GPU 资源协调完成后即可运行。
