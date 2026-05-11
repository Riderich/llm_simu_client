#!/usr/bin/env bash
# 双卡 nohup 启动 ExtES 本地筛（--world-size 2），GPU 物理 1 / 2 各一进程。
# 用法：在仓库根执行  bash workspace/scripts/extes_local_screen_sharded_start.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

BK="${EXTES_BINARY_KEPT:-workspace/dataset/extes_preliminary_stacked/binary_kept.json}"
RFK="${EXTES_RESIST_FINE_KEPT:-workspace/dataset/extes_preliminary_stacked/resist_fine_kept.json}"
MP="${EXTES_MODEL_PATH:-Qwen/Qwen2.5-7B-Instruct}"
OUT="${EXTES_OUT_JSONL:-workspace/results/extes/local_scores.jsonl}"
SUM="${EXTES_SUMMARY_JSON:-workspace/results/extes/local_screen_report.json}"
GPU0="${EXTES_GPU0:-1}"
GPU1="${EXTES_GPU1:-2}"

RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
RUNDIR="$ROOT/workspace/results/extes/logs/run_${RUN_ID}"
mkdir -p "$RUNDIR"

META="$RUNDIR/meta.env"
{
  echo "ROOT=$ROOT"
  echo "RUN_ID=$RUN_ID"
  echo "BK=$ROOT/$BK"
  echo "OUT=$ROOT/$OUT"
  echo "LOG0=$RUNDIR/shard0.log"
  echo "LOG1=$RUNDIR/shard1.log"
  echo "PID0=$RUNDIR/shard0.pid"
  echo "PID1=$RUNDIR/shard1.pid"
} >"$META"
ln -sfn "$RUNDIR" "$ROOT/workspace/results/extes/logs/LATEST_SHARD_RUN"

echo "RUNDIR=$RUNDIR"
echo "LATEST_SHARD_RUN -> $RUNDIR"

start_one() {
  local rank="$1" gpu="$2" log="$3" pidf="$4"
  nohup env CUDA_VISIBLE_DEVICES="$gpu" PYTHONUNBUFFERED=1 \
    python -u -m data_scripts.extes_pipeline.local_model_screen \
    --binary-kept "$ROOT/$BK" \
    --resist-fine-kept "$ROOT/$RFK" \
    --model-path "$MP" \
    --gpu 0 \
    --out-jsonl "$ROOT/$OUT" \
    --summary-json "$ROOT/$SUM" \
    --world-size 2 \
    --rank "$rank" \
    >"$log" 2>&1 &
  echo $! >"$pidf"
  echo "shard rank=$rank CUDA_VISIBLE_DEVICES=$gpu pid=$(cat "$pidf") log=$log"
}

start_one 0 "$GPU0" "$RUNDIR/shard0.log" "$RUNDIR/shard0.pid"
start_one 1 "$GPU1" "$RUNDIR/shard1.log" "$RUNDIR/shard1.pid"

echo "Started. Monitor: bash workspace/scripts/extes_local_screen_sharded_monitor_loop.sh"
echo "Merge when both shards exit: see tail of monitor log or README ExtES section."
