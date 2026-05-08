#!/usr/bin/env python3
"""
DeepSeek LLM pipeline: suitability judge -> clinical ZH translation -> post-check.
Reads translation queue from training_splits; writes JSONL + progress.json for monitoring.

Resume: re-run with same --out-dir; completed sample_id lines are skipped.

Example (foreground smoke):
  python data_scripts/run_zh_translation_pipeline.py --max-items 3

Multi-thread (e.g. 4 workers; watch API rate limits):
  python data_scripts/run_zh_translation_pipeline.py --workers 4 --sleep 0.2

Background:
  nohup python -u data_scripts/run_zh_translation_pipeline.py --workers 4 > workspace/results/translation_pipeline/nohup.log 2>&1 &
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "workspace" / "src"))

from deepseek_client import DeepSeekClient  # noqa: E402

DEFAULT_QUEUE = REPO / "workspace/results/training_splits/translation_culture_judge_queue.json"
DEFAULT_OUT = REPO / "workspace/results/translation_pipeline"

SYSTEM_JSON = "你只输出合法 JSON，不要 Markdown，不要多余解释。"

PROMPT_JUDGE = """你是心理咨询语料审核员。给定一段英文咨询对话片段（来访者与咨询师），判断是否适合翻译成**简体中文**用于训练「来访者模拟」模型。

适合翻译：语义在中文里可自然呈现，且翻译后**仍能保持**原来的阻抗/合作、情绪强度与话轮功能。
不适合翻译：强文化绑定（本地政治/宗教专属梗、强依赖英语双关、特定国家制度细节且难以中性转写）、或翻译会系统性扭曲行为标签。

行为标签（勿改，仅供你判断）：
- binary_label: {binary_label}
- label_code: {label_code}

对话与目标轮（JSON）：
{payload}

请输出 JSON，字段如下：
{{
  "suitability": "translate" | "translate_with_note" | "exclude",
  "risk_tags": [字符串，可为空],
  "rationale": "中文简短理由",
  "confidence": "low" | "medium" | "high"
}}
说明：若基本可译但需译者注意文化差异，用 translate_with_note；若应丢弃该样本，用 exclude。"""

PROMPT_TRANSLATE = """你是专业译者，将心理咨询场景下的**来访者视角**英文转为自然简体中文口语。

硬性要求：
1) 保持来访者立场与情绪；**不要**润色成「积极配合治疗」的来访者腔。
2) 保留话轮功能：挑战、防御、否认、回避、短答等需保留力度。
3) 保留 <internal> 内结构：仍使用 <internal>\\n[Perception]...\\n[Decision]...\\n</internal> 之后再跟外显话（与英文结构一致）。
4) 不要添加未出现在原文的临床诊断或价值判断。

行为标签（参考，禁止改写标签本身）：
- binary_label: {binary_label}
- label_code: {label_code}

英文 JSON：
{payload}

只输出一个 JSON 对象，字段：
{{
  "context_zh": [ {{"speaker":"therapist|client","text":"..."}} ],
  "therapist_turn_zh": "...",
  "client_response_zh": "...",
  "internal_zh": "<internal>\\n...\\n</internal>\\n（若英文 internal 无标签则只译正文并保持段落名称）"
}}

注意：internal_zh 应包含 <internal> 与 </internal> 包裹的完整内心独白；若原 internal 以 [Perception]/[Decision] 分段，请保留该分段标题。"""

PROMPT_POSTCHECK = """你是质检员。给定英文原稿与中文译文、以及行为标签，判断中文是否**扭曲**了阻抗/合作或文化上不应直译处未处理。

标签（须与之一致地评估，不得要求修改标签）：
- binary_label: {binary_label}
- label_code: {label_code}

英文原稿 JSON：
{en}

中文译文 JSON：
{zh}

仅输出 JSON：
{{
  "verdict": "keep" | "revise" | "reject",
  "notes": "中文说明",
  "revised_context_zh": null 或同结构数组,
  "revised_therapist_turn_zh": null 或字符串,
  "revised_client_response_zh": null 或字符串,
  "revised_internal_zh": null 或字符串
}}
若仅需微调，用 revise 并给出 revised_*；若必须丢弃该训练样本，用 reject。"""


def _extract_json(text: str) -> dict:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # 取第一个 ```json ... ``` 块
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", text, re.IGNORECASE)
    if fence:
        try:
            return json.loads(fence.group(1).strip())
        except json.JSONDecodeError:
            pass
    # 从首个 { 开始做括号_balance截取第一个完整对象
    start = text.find("{")
    if start >= 0:
        depth = 0
        for i, ch in enumerate(text[start:], start):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start : i + 1])
                    except json.JSONDecodeError:
                        break
    m = re.search(r"\{[\s\S]*\}", text)
    if m:
        return json.loads(m.group(0))
    raise ValueError(f"无法解析 JSON: {text[:200]}...")


def _chat_parse_with_retries(
    *,
    label: str,
    sample_id: str,
    client: DeepSeekClient,
    messages: list[dict],
    temperature: float,
    max_tokens: int,
    max_attempts: int,
    retry_sleep_s: float,
) -> tuple[dict | None, str, list[str]]:
    """
    调用 chat 并解析 JSON；失败则间隔重试。
    返回 (parsed 或 None, 最后一次 raw 文本, 每次尝试的错误摘要列表)。
    """
    raw_last = ""
    errs: list[str] = []
    for attempt in range(1, max_attempts + 1):
        try:
            raw_last = client.chat(messages, temperature=temperature, max_tokens=max_tokens)
            return _extract_json(raw_last), raw_last, []
        except Exception as e:  # noqa: BLE001
            errs.append(f"{attempt}/{max_attempts}: {repr(e)}")
            if attempt < max_attempts:
                print(
                    f"[retry {label}] {sample_id} {attempt}/{max_attempts} {e!r}",
                    flush=True,
                )
                if retry_sleep_s > 0:
                    time.sleep(retry_sleep_s)
    return None, raw_last, errs


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_jsonl_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    ids: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            sid = obj.get("sample_id")
            if sid:
                ids.add(sid)
        except json.JSONDecodeError:
            continue
    return ids


def _append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
        f.flush()


def _write_progress(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _count_nonempty_lines(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open(encoding="utf-8") as fh:
        return sum(1 for line in fh if line.strip())


def _fmt_payload(item: dict) -> str:
    return json.dumps(
        {
            "context": item["text_bundle"].get("context", []),
            "therapist_turn": item["text_bundle"].get("therapist_turn", ""),
            "client_response": item["text_bundle"].get("client_response", ""),
            "internal": item["text_bundle"].get("internal", ""),
        },
        ensure_ascii=False,
        indent=2,
    )


def _read_judge_for_sample(stage1_path: Path, sample_id: str) -> dict:
    judge: dict = {}
    if not stage1_path.exists():
        return judge
    for line in stage1_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        o = json.loads(line)
        if o.get("sample_id") == sample_id:
            judge = o.get("judge") or {}
    return judge


def _read_stage2_row(stage2_path: Path, sample_id: str) -> tuple[dict, bool, dict]:
    """Returns (zh_obj, skipped2, row2_full)."""
    if not stage2_path.exists():
        return {}, True, {}
    for line in stage2_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        o = json.loads(line)
        if o.get("sample_id") == sample_id:
            return o.get("zh") or {}, o.get("skipped", False), o
    return {}, True, {}


_thread_local = threading.local()


def _thread_client(model_hint: str | None) -> DeepSeekClient:
    """OpenAI SDK / httpx：每线程独立 Client，避免并发共享连接。"""
    key = model_hint or ""
    cur = getattr(_thread_local, "client_key", None)
    if getattr(_thread_local, "client", None) is None or cur != key:
        _thread_local.client = DeepSeekClient()
        _thread_local.client_key = key
    return _thread_local.client


def _process_one_item(
    item: dict,
    *,
    client: DeepSeekClient,
    stage1_path: Path,
    stage2_path: Path,
    stage3_path: Path,
    progress_path: Path,
    started: str,
    done1: set[str],
    done2: set[str],
    done3: set[str],
    io_lock: threading.Lock,
    total_cap: int,
    progress_every: int,
    processed_holder: list[int],
    progress_lock: threading.Lock,
    sleep_s: float,
    max_call_attempts: int,
    retry_sleep_s: float,
) -> str:
    """处理单条样本（三阶段）。返回 sample_id。"""
    sample_id = item.get("sample_id", "")
    payload = _fmt_payload(item)
    bl = item.get("binary_label", "")
    lc = item.get("label_code", "")

    with io_lock:
        already_done = sample_id in done3
    if already_done:
        with progress_lock:
            processed_holder[0] += 1
            pc = processed_holder[0]
            if pc % progress_every == 0:
                _write_progress(
                    progress_path,
                    {
                        "started_at": started,
                        "updated_at": _now_iso(),
                        "model": client.model,
                        "base_url": client.base_url,
                        "processed_this_run": pc,
                        "total_to_process_this_run": total_cap,
                        "stage1_lines": _count_nonempty_lines(stage1_path),
                        "stage2_lines": _count_nonempty_lines(stage2_path),
                        "stage3_lines": _count_nonempty_lines(stage3_path),
                        "last_sample_id": sample_id,
                        "last_error": None,
                        "note": "skipped_already_in_done3",
                    },
                )
        if sleep_s > 0:
            time.sleep(sleep_s)
        print(f"[{processed_holder[0]}/{total_cap}] {sample_id} skip_done", flush=True)
        return sample_id

    judge: dict = {}

    # ---- Stage 1
    with io_lock:
        in_done1 = sample_id in done1
    if not in_done1:
        uj = PROMPT_JUDGE.format(binary_label=bl, label_code=lc, payload=payload)
        msgs_j = [{"role": "system", "content": SYSTEM_JSON}, {"role": "user", "content": uj}]
        judge_parsed, raw_last, try_errs = _chat_parse_with_retries(
            label="stage1",
            sample_id=sample_id,
            client=client,
            messages=msgs_j,
            temperature=0.1,
            max_tokens=1024,
            max_attempts=max_call_attempts,
            retry_sleep_s=retry_sleep_s,
        )
        if judge_parsed is None:
            row1 = {
                "sample_id": sample_id,
                "source": item.get("source"),
                "binary_label": bl,
                "label_code": lc,
                "judge": {},
                "parse_error": True,
                "attempts": max_call_attempts,
                "errors": try_errs,
                "raw_judge": raw_last or None,
                "ts": _now_iso(),
                "note": "Stage1 连续调用或 JSON 解析失败，已跳过；后续按 exclude 处理。",
            }
            judge = {}
            with io_lock:
                _append_jsonl(stage1_path, row1)
                done1.add(sample_id)
            with progress_lock:
                _write_progress(
                    progress_path,
                    {
                        "started_at": started,
                        "model": client.model,
                        "last_sample_id": sample_id,
                        "last_stage": "stage1",
                        "last_error": try_errs[-1] if try_errs else "unknown",
                        "processed_this_run": processed_holder[0],
                        "hint": "stage1 max retries exhausted; wrote parse_error row",
                    },
                )
        else:
            judge = judge_parsed
            row1 = {
                "sample_id": sample_id,
                "source": item.get("source"),
                "binary_label": bl,
                "label_code": lc,
                "judge": judge,
                "raw_judge": raw_last,
                "ts": _now_iso(),
            }
            with io_lock:
                _append_jsonl(stage1_path, row1)
                done1.add(sample_id)
    else:
        with io_lock:
            judge = _read_judge_for_sample(stage1_path, sample_id)

    suitability = (judge or {}).get("suitability", "exclude")

    # ---- Stage 2
    with io_lock:
        in_done2 = sample_id in done2
    if not in_done2:
        if suitability == "exclude":
            row2 = {
                "sample_id": sample_id,
                "skipped": True,
                "reason": "exclude_by_judge",
                "judge": judge,
                "ts": _now_iso(),
            }
            with io_lock:
                _append_jsonl(stage2_path, row2)
                done2.add(sample_id)
        else:
            ut = PROMPT_TRANSLATE.format(binary_label=bl, label_code=lc, payload=payload)
            msgs_t = [{"role": "system", "content": SYSTEM_JSON}, {"role": "user", "content": ut}]
            zh_parsed, raw_t, try_errs_t = _chat_parse_with_retries(
                label="stage2",
                sample_id=sample_id,
                client=client,
                messages=msgs_t,
                temperature=0.15,
                max_tokens=4096,
                max_attempts=max_call_attempts,
                retry_sleep_s=retry_sleep_s,
            )
            if zh_parsed is None:
                row2 = {
                    "sample_id": sample_id,
                    "skipped": True,
                    "reason": "translate_parse_or_api_failed",
                    "parse_error": True,
                    "attempts": max_call_attempts,
                    "errors": try_errs_t,
                    "judge": judge,
                    "raw_translate": raw_t or None,
                    "ts": _now_iso(),
                    "note": "Stage2 连续失败；未写入译文，Stage3 将跳过质检。",
                }
                with io_lock:
                    _append_jsonl(stage2_path, row2)
                    done2.add(sample_id)
                with progress_lock:
                    _write_progress(
                        progress_path,
                        {
                            "started_at": started,
                            "model": client.model,
                            "last_sample_id": sample_id,
                            "last_stage": "stage2",
                            "last_error": try_errs_t[-1] if try_errs_t else "unknown",
                            "processed_this_run": processed_holder[0],
                            "hint": "stage2 max retries exhausted; wrote skipped row",
                        },
                    )
            else:
                zh_obj = zh_parsed
                row2 = {
                    "sample_id": sample_id,
                    "skipped": False,
                    "binary_label": bl,
                    "label_code": lc,
                    "judge": judge,
                    "zh": zh_obj,
                    "raw_translate": raw_t,
                    "en_backup": json.loads(payload),
                    "ts": _now_iso(),
                }
                with io_lock:
                    _append_jsonl(stage2_path, row2)
                    done2.add(sample_id)

    with io_lock:
        zh_obj, skipped2, row2_full = _read_stage2_row(stage2_path, sample_id)

    # ---- Stage 3
    with io_lock:
        in_done3 = sample_id in done3
    if not in_done3:
        if skipped2:
            row3 = {
                "sample_id": sample_id,
                "skipped": True,
                "reason": "no_translation",
                "ts": _now_iso(),
            }
            with io_lock:
                _append_jsonl(stage3_path, row3)
                done3.add(sample_id)
        else:
            en_block = json.loads(payload)
            up = PROMPT_POSTCHECK.format(
                binary_label=bl,
                label_code=lc,
                en=json.dumps(en_block, ensure_ascii=False, indent=2),
                zh=json.dumps(zh_obj, ensure_ascii=False, indent=2),
            )
            msgs_p = [{"role": "system", "content": SYSTEM_JSON}, {"role": "user", "content": up}]
            check_parsed, raw_p, try_errs_p = _chat_parse_with_retries(
                label="stage3",
                sample_id=sample_id,
                client=client,
                messages=msgs_p,
                temperature=0.0,
                max_tokens=2048,
                max_attempts=max_call_attempts,
                retry_sleep_s=retry_sleep_s,
            )
            if check_parsed is None:
                err_row = {
                    "sample_id": sample_id,
                    "skipped": False,
                    "parse_error": True,
                    "attempts": max_call_attempts,
                    "errors": try_errs_p,
                    "verdict": None,
                    "check": {},
                    "raw_postcheck": raw_p or None,
                    "zh_final": zh_obj,
                    "stage2_snapshot": row2_full,
                    "ts": _now_iso(),
                    "note": "Stage3 连续失败；zh_final 回退为 stage2 译文，可后续人工或重跑单条。",
                }
                with io_lock:
                    _append_jsonl(stage3_path, err_row)
                    done3.add(sample_id)
                with progress_lock:
                    _write_progress(
                        progress_path,
                        {
                            "started_at": started,
                            "model": client.model,
                            "last_sample_id": sample_id,
                            "last_stage": "stage3",
                            "last_error": try_errs_p[-1] if try_errs_p else "unknown",
                            "processed_this_run": processed_holder[0],
                            "hint": "stage3 max retries exhausted; wrote parse_error row",
                        },
                    )
            else:
                check = check_parsed
                row3 = {
                    "sample_id": sample_id,
                    "skipped": False,
                    "parse_error": False,
                    "verdict": check.get("verdict"),
                    "check": check,
                    "raw_postcheck": raw_p,
                    "ts": _now_iso(),
                }
                if check.get("verdict") == "revise" and (
                    check.get("revised_client_response_zh") or check.get("revised_internal_zh")
                ):
                    merged = dict(zh_obj)
                    if check.get("revised_context_zh") is not None:
                        merged["context_zh"] = check["revised_context_zh"]
                    if check.get("revised_therapist_turn_zh"):
                        merged["therapist_turn_zh"] = check["revised_therapist_turn_zh"]
                    if check.get("revised_client_response_zh"):
                        merged["client_response_zh"] = check["revised_client_response_zh"]
                    if check.get("revised_internal_zh"):
                        merged["internal_zh"] = check["revised_internal_zh"]
                    row3["zh_final"] = merged
                else:
                    row3["zh_final"] = zh_obj
                row3["stage2_snapshot"] = row2_full
                with io_lock:
                    _append_jsonl(stage3_path, row3)
                    done3.add(sample_id)

    if sleep_s > 0:
        time.sleep(sleep_s)

    with progress_lock:
        processed_holder[0] += 1
        pc = processed_holder[0]
        if pc % progress_every == 0:
            _write_progress(
                progress_path,
                {
                    "started_at": started,
                    "updated_at": _now_iso(),
                    "model": client.model,
                    "base_url": client.base_url,
                    "processed_this_run": pc,
                    "total_to_process_this_run": total_cap,
                    "stage1_lines": _count_nonempty_lines(stage1_path),
                    "stage2_lines": _count_nonempty_lines(stage2_path),
                    "stage3_lines": _count_nonempty_lines(stage3_path),
                    "last_sample_id": sample_id,
                    "last_error": None,
                },
            )

    print(f"[{processed_holder[0]}/{total_cap}] {sample_id} done", flush=True)
    return sample_id


def run() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--max-items", type=int, default=0, help="0 表示全量")
    ap.add_argument("--sleep", type=float, default=0.0, help="每条样本完成后休眠秒数（限流，多线程时每线程独立）")
    ap.add_argument("--progress-every", type=int, default=10)
    ap.add_argument(
        "--workers",
        type=int,
        default=1,
        help="并发线程数（每线程独立 DeepSeek 客户端）；>1 时注意 API 限流，可适当加大 --sleep",
    )
    ap.add_argument(
        "--max-call-attempts",
        type=int,
        default=4,
        help="单阶段内每次 API+JSON 解析失败时的最大尝试次数（含首次）。默认 4=首次+最多 3 次重试；耗尽后写错误行并继续。",
    )
    ap.add_argument(
        "--retry-sleep",
        type=float,
        default=0.25,
        help="同一阶段内重试之间的休眠秒数（限流与抖动）。",
    )
    args = ap.parse_args()
    max_call_attempts = max(1, int(args.max_call_attempts))

    out_dir = args.out_dir
    stage1_path = out_dir / "stage1_suitability.jsonl"
    stage2_path = out_dir / "stage2_translation.jsonl"
    stage3_path = out_dir / "stage3_postcheck.jsonl"
    progress_path = out_dir / "progress.json"

    queue = json.loads(args.queue.read_text(encoding="utf-8"))
    done1 = _load_jsonl_ids(stage1_path)
    done2 = _load_jsonl_ids(stage2_path)
    done3 = _load_jsonl_ids(stage3_path)

    started = _now_iso()
    total_cap = len(queue) if args.max_items <= 0 else min(len(queue), args.max_items)
    processed_holder = [0]
    io_lock = threading.Lock()
    progress_lock = threading.Lock()

    probe = DeepSeekClient()
    _write_progress(
        progress_path,
        {
            "started_at": started,
            "model": probe.model,
            "base_url": probe.base_url,
            "workers": args.workers,
            "max_call_attempts": max_call_attempts,
            "retry_sleep_s": args.retry_sleep,
            "queue": str(args.queue),
            "total_queued": len(queue),
            "total_to_process_this_run": total_cap,
            "stage1_done_before": len(done1),
            "stage2_done_before": len(done2),
            "stage3_done_before": len(done3),
            "last_sample_id": None,
            "last_error": None,
        },
    )

    batch = queue[:total_cap]

    def _run_item(it: dict) -> None:
        cli = _thread_client(probe.model)
        _process_one_item(
            it,
            client=cli,
            stage1_path=stage1_path,
            stage2_path=stage2_path,
            stage3_path=stage3_path,
            progress_path=progress_path,
            started=started,
            done1=done1,
            done2=done2,
            done3=done3,
            io_lock=io_lock,
            total_cap=total_cap,
            progress_every=args.progress_every,
            processed_holder=processed_holder,
            progress_lock=progress_lock,
            sleep_s=args.sleep,
            max_call_attempts=max_call_attempts,
            retry_sleep_s=float(args.retry_sleep),
        )

    workers = max(1, int(args.workers))
    if workers == 1:
        for item in batch:
            _run_item(item)
    else:
        errors: list[BaseException] = []
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futures = [ex.submit(_run_item, item) for item in batch]
            for fut in as_completed(futures):
                try:
                    fut.result()
                except BaseException as e:  # noqa: BLE001
                    errors.append(e)
                    with progress_lock:
                        _write_progress(
                            progress_path,
                            {
                                "started_at": started,
                                "updated_at": _now_iso(),
                                "model": probe.model,
                                "workers": workers,
                                "fatal_worker_error": repr(e),
                            },
                        )
        if errors:
            raise errors[0]

    _write_progress(
        progress_path,
        {
            "started_at": started,
            "finished_at": _now_iso(),
            "model": probe.model,
            "base_url": probe.base_url,
            "workers": workers,
            "processed_this_run": processed_holder[0],
            "total_to_process_this_run": total_cap,
            "stage1_lines": _count_nonempty_lines(stage1_path),
            "stage2_lines": _count_nonempty_lines(stage2_path),
            "stage3_lines": _count_nonempty_lines(stage3_path),
            "status": "completed",
        },
    )
    print(f"Done. Outputs under {out_dir}", flush=True)


if __name__ == "__main__":
    run()
