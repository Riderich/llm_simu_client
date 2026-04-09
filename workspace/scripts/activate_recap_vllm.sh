#!/bin/bash
# 激活 recap_vllm conda 环境的快捷脚本
# Usage: source workspace/scripts/activate_recap_vllm.sh

echo "Activating recap_vllm conda environment..."
source /data5/zxj/miniconda3/bin/activate recap_vllm
echo "Environment activated!"
echo ""
echo "Python: $(python --version)"
echo "PyTorch: $(python -c 'import torch; print(torch.__version__)')"
echo "vLLM: $(python -c 'import vllm; print(vllm.__version__)')"
echo "CUDA: $(python -c 'import torch; print(torch.version.cuda if torch.cuda.is_available() else \"N/A\")')"
