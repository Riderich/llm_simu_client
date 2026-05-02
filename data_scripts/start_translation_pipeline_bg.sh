#!/usr/bin/env bash
# 后台启动中文翻译管线（DeepSeek，见 .env DEEPSEEK_*）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${ROOT}/workspace/results/translation_pipeline"
mkdir -p "$OUT"
cd "$ROOT"
nohup python3 -u data_scripts/run_zh_translation_pipeline.py --sleep 0.15 --progress-every 5 \
  > "${OUT}/nohup.log" 2>&1 &
echo $! > "${OUT}/pid.txt"
echo "Started PID $(cat "${OUT}/pid.txt")"
echo "Log: ${OUT}/nohup.log"
echo "Progress JSON: ${OUT}/progress.json"
