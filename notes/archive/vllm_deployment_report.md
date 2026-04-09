# vLLM 部署成功报告

> 日期：2026-03-21  
> GPU：NVIDIA RTX A6000 (GPU 3)  
> 环境：recap_vllm (conda)  
> vLLM 版本：0.6.1

---

## ✅ 部署状态

### 环境配置
| 组件 | 版本 | 状态 |
|------|------|------|
| Python | 3.10 | ✅ |
| PyTorch | 2.4.0+cu121 | ✅ |
| vLLM | 0.6.1 | ✅ |
| Transformers | 4.45.0 | ✅ |

### 模型加载
| 模型 | 显存占用 | 加载时间 | 状态 |
|------|----------|----------|------|
| binary_share_model | ~15 GB | 5s | ✅ |
| only_resistance_share_model | ~15 GB | - | ⚠️ (单卡无法同时加载) |

---

## 🚀 性能测试

### RECAP 数据 (10条)

```
推理时间: ~2秒
准确率: 10/10 = 100%
速度: ~5 it/s
```

### ESConv 数据 (100条)

```
推理时间: ~20秒
分布: 合作 97, 阻抗 3
速度: ~5 it/s
批处理: 32条/批
```

### 与 Transformers 对比

| 方案 | 速度 | 显存效率 | 批处理 |
|------|------|----------|--------|
| Transformers | ~0.3 it/s | 一般 | 手动实现 |
| **vLLM** | **~5 it/s** | **优秀** | **内置优化** |
| **提升** | **~17x** | - | - |

---

## 📁 使用方式

### 激活环境
```bash
conda activate recap_vllm
# 或
/data5/zxj/miniconda3/envs/recap_vllm/bin/python
```

### 批量标注 ESConv
```bash
cd /data5/zxj/llm_simu_client/workspace

CUDA_VISIBLE_DEVICES=3 /data5/zxj/miniconda3/envs/recap_vllm/bin/python \
    scripts/recap_vllm_inference.py \
    --input dataset/ESConv.json \
    --output results/esconv_labeled.json \
    --data-format esconv \
    --no-fine-grained
```

### 批量标注 MESC
```bash
CUDA_VISIBLE_DEVICES=3 /data5/zxj/miniconda3/envs/recap_vllm/bin/python \
    scripts/recap_vllm_inference.py \
    --input dataset/MESC_merged.json \
    --output results/mesc_labeled.json \
    --data-format esconv \
    --no-fine-grained
```

### 预估时间
| 数据集 | 数据量 | 预计时间 |
|--------|--------|----------|
| ESConv | ~16,000 条 | ~50 分钟 |
| MESC | ~14,000 条 | ~45 分钟 |

---

## ⚠️ 限制说明

### 单卡限制
- 无法同时加载两个模型（二分类 + 细分类）
- 如需细分类标注，需：
  1. 先用二分类筛选出阻抗样本
  2. 再单独用细分类模型标注

### 细分类方案
```bash
# 步骤1: 二分类筛选
python scripts/recap_vllm_inference.py \
    --input data.json \
    --output results/binary.json \
    --no-fine-grained

# 步骤2: 提取阻抗样本，用细分类模型标注
# (需要另一个脚本实现)
```

---

## 📝 脚本路径

```
workspace/scripts/recap_vllm_inference.py
```

**关键参数：**
- `--input`: 输入数据文件
- `--output`: 输出结果文件
- `--data-format`: `recap` 或 `esconv`
- `--batch-size`: 批大小 (默认 32)
- `--no-fine-grained`: 只进行二分类
- `--gpu`: GPU ID (默认 3)

---

## ✅ 验证命令

```bash
# Dry run 测试
CUDA_VISIBLE_DEVICES=3 /data5/zxj/miniconda3/envs/recap_vllm/bin/python \
    scripts/recap_vllm_inference.py --dry-run

# 小批量测试
CUDA_VISIBLE_DEVICES=3 /data5/zxj/miniconda3/envs/recap_vllm/bin/python \
    scripts/recap_vllm_inference.py \
    --input dataset/ESConv.json \
    --output results/test.json \
    --max-samples 100 \
    --no-fine-grained
```

---

## 🎉 结论

**vLLM 部署成功！**

- ✅ Conda 环境配置完成
- ✅ vLLM 0.6.1 安装成功
- ✅ 二分类模型运行正常
- ✅ 推理速度提升 17 倍
- ✅ 可立即用于 ESConv/MESC 批量标注

**下一步**: 运行全量 ESConv/MESC 标注
