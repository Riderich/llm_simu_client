#!/bin/bash
# vLLM 环境配置脚本
# 在指定的 conda 环境 (/data5/zxj/llama_3_1/) 中安装 vLLM

set -e

CONDA_ENV="/data5/zxj/llama_3_1"
PYTHON="$CONDA_ENV/bin/python"
PIP="$CONDA_ENV/bin/pip"

echo "=========================================="
echo "配置 vLLM 环境"
echo "Conda 环境: $CONDA_ENV"
echo "Python: $($PYTHON --version)"
echo "=========================================="

# 1. 升级 pip
echo "[1/4] 升级 pip..."
$PIP install --upgrade pip -q

# 2. 安装编译依赖（如果需要从源码编译）
echo "[2/4] 安装编译依赖..."
$PIP install setuptools-rust -q 2>/dev/null || echo "setuptools-rust 安装失败，尝试继续..."

# 3. 安装 vLLM
# 根据 CUDA 版本选择合适的版本
echo "[3/4] 安装 vLLM..."
CUDA_VERSION=$(nvcc --version | grep "release" | sed -n 's/.*release \([0-9]\+\.[0-9]\+\).*/\1/p')
echo "检测到 CUDA 版本: $CUDA_VERSION"

if [[ "$CUDA_VERSION" == "12.1" ]] || [[ "$CUDA_VERSION" == "12.2" ]] || [[ "$CUDA_VERSION" == "12.3" ]] || [[ "$CUDA_VERSION" == "12.4" ]]; then
    echo "安装 vLLM (CUDA 12.x)..."
    $PIP install vllm --extra-index-url https://download.pytorch.org/whl/cu121
elif [[ "$CUDA_VERSION" == "11.8" ]]; then
    echo "安装 vLLM (CUDA 11.8)..."
    $PIP install vllm --extra-index-url https://download.pytorch.org/whl/cu118
else
    echo "尝试安装通用版本的 vLLM..."
    $PIP install vllm
fi

# 4. 验证安装
echo "[4/4] 验证安装..."
$PYTHON -c "import vllm; print(f'vLLM version: {vllm.__version__}')"

echo ""
echo "=========================================="
echo "✅ vLLM 环境配置完成！"
echo "=========================================="
echo ""
echo "使用方法:"
echo "  1. 激活环境: source /data5/zxj/llama_3_1/bin/activate"
echo "  2. Dry run 测试:"
echo "     python scripts/recap_vllm_inference.py --dry-run"
echo "  3. 实际推理:"
echo "     python scripts/recap_vllm_inference.py --input dataset/ESConv.json --output results/esconv_labeled.json"
echo ""
echo "高级选项:"
echo "  - 多卡并行: --tp-size 2"
echo "  - 只二分类: --no-fine-grained"
echo "  - 指定批大小: --batch-size 64"
