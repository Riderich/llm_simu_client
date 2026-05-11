#!/usr/bin/env bash
# 每 10 分钟记录一次：GPU 1/2、分片进程是否存活、各 part JSONL 行数、日志尾部。
# 在仓库根：nohup bash workspace/scripts/extes_local_screen_sharded_monitor_loop.sh &
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

LATEST="$ROOT/workspace/results/extes/logs/LATEST_SHARD_RUN"
INTERVAL_SEC="${EXTES_MONITOR_INTERVAL_SEC:-600}"

if [[ ! -L "$LATEST" && ! -d "$LATEST" ]]; then
  echo "No LATEST_SHARD_RUN symlink; run extes_local_screen_sharded_start.sh first." >&2
  exit 1
fi
RUNDIR="$(readlink -f "$LATEST")"
LOGMON="$RUNDIR/monitor.log"
OUT_JSONL=""
if [[ -f "$RUNDIR/meta.env" ]]; then
  # shellcheck source=/dev/null
  source "$RUNDIR/meta.env"
  OUT_JSONL="${OUT:-}"
fi

log() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$LOGMON"; }

log "monitor loop RUNDIR=$RUNDIR interval=${INTERVAL_SEC}s"

while true; do
  log "---- tick ----"
  nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total --format=csv 2>/dev/null | head -10 >>"$LOGMON" || true

  if [[ -n "$OUT_JSONL" ]]; then
    base="$(basename "$OUT_JSONL")"
    dir="$(dirname "$OUT_JSONL")"
    shopt -s nullglob
    parts=( "$dir"/"${base%.jsonl}".part*.jsonl )
    shopt -u nullglob
    if ((${#parts[@]})); then
      for f in "${parts[@]}"; do
        n="$(wc -l <"$f" 2>/dev/null || echo 0)"
        log "  $f lines=$n"
      done
    else
      log "  (no part*.jsonl yet under $dir)"
    fi
  fi

  for tag in 0 1; do
    pf="$RUNDIR/shard${tag}.pid"
    lf="$RUNDIR/shard${tag}.log"
    if [[ -f "$pf" ]]; then
      pid="$(tr -d ' \n' <"$pf")"
      if kill -0 "$pid" 2>/dev/null; then
        log "  shard${tag} pid=$pid running"
      else
        log "  shard${tag} pid=$pid NOT running (exited)"
      fi
    else
      log "  shard${tag} no pid file"
    fi
    if [[ -f "$lf" ]]; then
      log "  --- tail shard${tag}.log ---"
      tail -n 8 "$lf" | sed 's/^/    /' >>"$LOGMON"
    fi
  done

  sleep "$INTERVAL_SEC"
done
