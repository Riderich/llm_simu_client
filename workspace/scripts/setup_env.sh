#!/bin/bash
# =============================================================================
# Inner Monologue Training Environment Setup Script
# 适用环境: Linux + Miniconda
# 使用方法: bash setup_env.sh
# =============================================================================

set -e  # 遇到错误立即退出

ENV_NAME="llm_train"
LLAMAFACTORY_DIR="$HOME/LLaMA-Factory"

echo "=============================================="
echo " Inner Monologue 训练环境一键配置脚本"
echo "=============================================="

# ── Step 1: 检查 GPU ───────────────────────────────────────────────────────
echo ""
echo "[1/6] 检查 GPU..."
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
echo ""

# ── Step 2: 安装/更新 Miniconda ────────────────────────────────────────────
echo "[2/6] 检查 Miniconda..."
if ! command -v conda &> /dev/null; then
    echo "  → 未检测到 conda，开始安装 Miniconda..."
    wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
    bash /tmp/miniconda.sh -b -p "$HOME/miniconda3"
    echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc
    export PATH="$HOME/miniconda3/bin:$PATH"
    conda init bash
    echo "  ✓ Miniconda 安装完成"
else
    echo "  ✓ conda 已存在: $(conda --version)"
fi

# ── Step 3: 创建 conda 环境 ────────────────────────────────────────────────
echo ""
echo "[3/6] 创建 conda 环境 '$ENV_NAME'..."
if conda env list | grep -q "^$ENV_NAME "; then
    echo "  ✓ 环境 '$ENV_NAME' 已存在，跳过创建"
else
    conda create -n "$ENV_NAME" python=3.10 -y
    echo "  ✓ 环境 '$ENV_NAME' 创建完成"
fi

# 激活环境
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"
echo "  ✓ 已激活环境: $CONDA_DEFAULT_ENV"

# ── Step 4: 克隆 LLaMA-Factory ────────────────────────────────────────────
echo ""
echo "[4/6] 安装 LLaMA-Factory..."
if [ -d "$LLAMAFACTORY_DIR" ]; then
    echo "  → LLaMA-Factory 已存在，执行 git pull 更新..."
    cd "$LLAMAFACTORY_DIR" && git pull
else
    git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git "$LLAMAFACTORY_DIR"
fi
cd "$LLAMAFACTORY_DIR"
pip install -e ".[torch,metrics]" -q
echo "  ✓ LLaMA-Factory 安装完成"

# ── Step 5: 安装额外依赖 ──────────────────────────────────────────────────
echo ""
echo "[5/6] 安装 QLoRA 和多卡训练依赖..."
pip install bitsandbytes -q          # 4bit 量化（QLoRA）
pip install deepspeed -q             # 多卡 ZeRO 训练
pip install wandb -q                 # 训练监控（可选）
echo "  ✓ 依赖安装完成"

# ── Step 6: 验证环境 ───────────────────────────────────────────────────────
echo ""
echo "[6/6] 验证环境..."
python -c "
import torch
print(f'  PyTorch 版本: {torch.__version__}')
print(f'  CUDA 可用: {torch.cuda.is_available()}')
print(f'  GPU 数量: {torch.cuda.device_count()}')
for i in range(torch.cuda.device_count()):
    name = torch.cuda.get_device_name(i)
    mem = torch.cuda.get_device_properties(i).total_memory / 1024**3
    print(f'    GPU {i}: {name} ({mem:.1f} GB)')
"

python -c "import bitsandbytes; print('  ✓ bitsandbytes (QLoRA) 可用')"
python -c "import deepspeed; print(f'  ✓ DeepSpeed 可用: {deepspeed.__version__}')"

echo ""
echo "=============================================="
echo " 环境配置完成！"
echo ""
echo " 下一步："
echo "   conda activate $ENV_NAME"
echo "   cd $LLAMAFACTORY_DIR"
echo "   # 上传数据："
echo "   # scp inner_monologue_dataset.json user@server:$LLAMAFACTORY_DIR/data/"
echo "   # 运行数据转换："
echo "   # python scripts/prepare_sft_data.py"
echo "   # 开始训练："
echo "   # llamafactory-cli train train_config/qwen25_7b_sft.yaml"
echo "=============================================="
