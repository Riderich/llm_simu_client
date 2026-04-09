"""
classify_recap_coop_subtype.py

Use Qwen to sub-classify RECAP cooperative samples ("合作-未阻抗") into:
- E1: Exploratory / Vulnerability
- E2: Simple Agreement
- E3: Insight / Resolution

Input:
  workspace/dataset/ClientResistance_processed.json

Output:
  workspace/dataset/ClientResistance_processed_e_split.json
"""

import argparse
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Optional, cast

from dotenv import load_dotenv
from openai import OpenAI


SYSTEM_PROMPT = """你是心理咨询对话数据标注专家。
你的任务：仅对“合作-未阻抗”样本打 E1/E2/E3 子标签。

定义：
- E1（Exploratory/Vulnerability）: 来访者在探索感受、困惑、矛盾或脆弱体验；开放但未形成明确行动决断。
- E2（Simple Agreement）: 来访者只是简短附和、礼貌回应、浅层配合或事实性回答；没有明显深入探索，也没有明确认知转折/行动承诺。
- E3（Insight/Resolution）: 来访者出现清晰认知转折、领悟，或提出明确行动决策/承诺。

判别优先级：
1) 若有明确“我决定/我会/接下来要”或明显认知转折，优先 E3。
2) 否则若仅是短促附和/浅层回答，优先 E2。
3) 其余偏开放探索和情绪加工，归 E1。

输出必须是严格 JSON，不要输出任何额外文本。
JSON schema:
{"subtype":"E1|E2|E3","confidence":0.0-1.0,"rationale":"不超过30字"}
"""


def _workspace_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_env(workspace_dir: str) -> None:
    env_path = os.path.join(workspace_dir, ".env")
    load_dotenv(env_path)


def _build_client(model: str) -> OpenAI:
    if model.lower().startswith("qwen"):
        api_key = os.getenv("QWEN_API_KEY") or os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("QWEN_BASE_URL") or "https://dashscope.aliyuncs.com/compatible-mode/v1"
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")

    if not api_key:
        raise ValueError("Missing API key. Please set QWEN_API_KEY or OPENAI_API_KEY in .env")

    return OpenAI(api_key=api_key, base_url=base_url)


def _format_dialogue(dialogue: list[dict[str, str]], max_turns: int = 10) -> str:
    clipped = dialogue[-max_turns:] if len(dialogue) > max_turns else dialogue
    lines = []
    for t in clipped:
        role = "咨询师" if t.get("role") == "user" else "来访者"
        lines.append(f"{role}: {t.get('content', '').strip()}")
    return "\n".join(lines)


def _normalize_cbs_type(v: Any) -> str:
    if not v:
        return ""
    s = str(v).strip().upper().replace("-", "").replace("_", "")
    mapping = {
        "CBS2": "CBS2", "AGREEMENT": "CBS2", "AGREEING": "CBS2", "认同": "CBS2",
        "CBS3": "CBS3", "APPROPRIATEREQUESTS": "CBS3", "REQUESTS": "CBS3", "恰当请求": "CBS3",
        "CBS4": "CBS4", "RECOUNTING": "CBS4", "NARRATIVES": "CBS4", "叙述": "CBS4",
        "CBS5": "CBS5", "COGNITIVEBEHAVIORALEXPLORATION": "CBS5", "认知行为探索": "CBS5",
        "CBS6": "CBS6", "AFFECTIVEEXPLORATION": "CBS6", "情感探索": "CBS6",
        "CBS7": "CBS7", "INSIGHT": "CBS7", "领悟": "CBS7",
        "CBS8": "CBS8", "THERAPEUTICCHANGES": "CBS8", "治疗性改变": "CBS8",
    }
    return mapping.get(s, "")


def _extract_json(text: str) -> Optional[dict[str, Any]]:
    text = (text or "").strip()
    if not text:
        return None

    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass

    m = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not m:
        return None

    try:
        obj = json.loads(m.group(0))
        if isinstance(obj, dict):
            return obj
    except Exception:
        return None
    return None


def classify_one(
    client: OpenAI,
    model: str,
    dialogue: list[dict[str, str]],
    target: str,
    temperature: float = 0.1,
    max_retries: int = 3,
) -> dict[str, Any]:
    user_prompt = f"""请判断来访者发言属于 CBS 2-8 中的哪一类。

完整对话（最后几句）：
{_format_dialogue(dialogue)}

目标句（来访者发言）：
{target}

请仅输出 JSON。"""

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    text = ""
    last_err = None
    for attempt in range(max_retries):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=cast(Any, messages),
                temperature=temperature,
                max_tokens=200,
            )
            text = resp.choices[0].message.content or ""
            last_err = None
            break
        except Exception as e:
            last_err = e
            time.sleep(min(2 ** attempt, 8))

    if last_err is not None:
        raise ValueError(f"API error after retries: {str(last_err)[:120]}")

    parsed = _extract_json(text)

    if not parsed:
        messages.append({"role": "assistant", "content": text})
        messages.append({"role": "user", "content": "输出不合规。请只输出一个 JSON 对象，不要任何解释。"})
        resp = client.chat.completions.create(
            model=model,
            messages=cast(Any, messages),
            temperature=0,
            max_tokens=120,
        )
        text = resp.choices[0].message.content or ""
        parsed = _extract_json(text)

    if not parsed:
        raise ValueError(f"Failed to parse JSON response: {text[:200]}")

    cbs_type = _normalize_cbs_type(parsed.get("cbs_type"))
    if cbs_type not in {f"CBS{i}" for i in range(2, 9)}:
        raise ValueError(f"Invalid cbs_type: {parsed.get('cbs_type')}")

    confidence = parsed.get("confidence", 0.5)
    try:
        confidence = float(confidence)
    except Exception:
        confidence = 0.5
    confidence = max(0.0, min(1.0, confidence))

    rationale = str(parsed.get("rationale", "")).strip()
    if len(rationale) > 30:
        rationale = rationale[:30]

    return {
        "cbs_type": cbs_type,
        "confidence": confidence,
        "rationale": rationale,
        "raw_response": text,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify cooperative samples into CBS 2-8 using Qwen")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default="qwen-max")
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--limit", type=int, default=0, help="Only process first N cooperative samples (0 = all)")
    parser.add_argument("--resume", action="store_true", help="Skip samples already containing cooperative_subtype")
    parser.add_argument("--save-every", type=int, default=50)
    parser.add_argument("--sleep", type=float, default=0.0, help="Sleep seconds between requests")
    parser.add_argument("--retry-failed", action="store_true", help="When --resume, also reprocess records with confidence<=0 or ERROR rationale")
    parser.add_argument("--max-retries", type=int, default=3, help="Max API retries per sample")
    parser.add_argument("--workers", type=int, default=1, help="Parallel worker threads")
    args = parser.parse_args()

    workspace_dir = _workspace_root()
    _load_env(workspace_dir)
    client = _build_client(args.model)

    in_path = os.path.join(workspace_dir, args.input)
    out_path = os.path.join(workspace_dir, args.output)

    with open(in_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    coop_indices = []
    for i, r in enumerate(data):
        if r.get("binary_label") == "合作":
            coop_indices.append(i)

    if args.limit > 0:
        coop_indices = coop_indices[: args.limit]

    print(f"Total records: {len(data)}")
    print(f"Cooperative candidates: {len(coop_indices)}")
    print(f"Model: {args.model}")

    done = 0
    failed = 0
    cbs_count = {f"CBS{i}": 0 for i in range(2, 9)}

    def should_skip(idx: int) -> bool:
        r = data[idx]
        if not args.resume:
            return False
        if r.get("cbs_type") in {f"CBS{i}" for i in range(2, 9)}:
            if not args.retry_failed:
                return True
            conf = float(r.get("cbs_confidence", 0.0) or 0.0)
            if conf > 0 and not str(r.get("cbs_rationale", "")).startswith("ERROR:"):
                return True
        return False

    pending_indices: list[int] = []
    for idx in coop_indices:
        if should_skip(idx):
            cbs_type = data[idx].get("cbs_type")
            if cbs_type in cbs_count:
                cbs_count[cbs_type] += 1
            done += 1
        else:
            pending_indices.append(idx)

    print(f"Already done/skipped: {done}")
    print(f"Pending to process: {len(pending_indices)}")

    def apply_success(rec: dict[str, Any], result: dict[str, Any]) -> None:
        rec["cbs_type"] = result["cbs_type"]
        rec["cbs_confidence"] = result["confidence"]
        rec["cbs_rationale"] = result["rationale"]
        rec["cbs_model"] = args.model

    def apply_failure(rec: dict[str, Any], err: Exception) -> None:
        rec["cbs_type"] = "CBS2"  # Default fallback
        rec["cbs_confidence"] = 0.0
        rec["cbs_rationale"] = f"ERROR:{str(err)[:20]}"
        rec["cbs_model"] = args.model

    def save_checkpoint() -> None:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[{done}/{len(coop_indices)}] checkpoint saved -> {out_path}")

    def get_dialogue_and_target(rec):
        # Handle ESConv format
        metadata = rec.get("metadata", {})
        dialog = metadata.get("dialog", [])
        target = rec.get("response", "")
        return dialog, target

    if args.workers <= 1:
        for pos, idx in enumerate(pending_indices, start=1):
            rec = data[idx]
            try:
                dialogue, target = get_dialogue_and_target(rec)
                result = classify_one(
                    client=client,
                    model=args.model,
                    dialogue=dialogue,
                    target=target,
                    temperature=args.temperature,
                    max_retries=args.max_retries,
                )
                apply_success(rec, result)
                cbs_count[result["cbs_type"]] += 1
            except Exception as e:
                apply_failure(rec, e)
                failed += 1
            done += 1

            if args.sleep > 0:
                time.sleep(args.sleep)

            if done % args.save_every == 0:
                save_checkpoint()

            if pos % 20 == 0 or pos == len(pending_indices):
                cbs_str = " ".join([f"{k}={v}" for k, v in cbs_count.items()])
                print(f"Progress {done}/{len(coop_indices)} | {cbs_str} failed={failed}")
    else:
        print(f"Running with {args.workers} worker threads")

        def run_one(idx: int) -> tuple[int, Optional[dict[str, Any]], Optional[str]]:
            local_client = _build_client(args.model)
            rec = data[idx]
            try:
                dialogue, target = get_dialogue_and_target(rec)
                result = classify_one(
                    client=local_client,
                    model=args.model,
                    dialogue=dialogue,
                    target=target,
                    temperature=args.temperature,
                    max_retries=args.max_retries,
                )
                return idx, result, None
            except Exception as e:
                return idx, None, str(e)

        completed_pending = 0
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            future_map = {ex.submit(run_one, idx): idx for idx in pending_indices}
            for fut in as_completed(future_map):
                idx, result, err = fut.result()
                rec = data[idx]
                if result is not None:
                    apply_success(rec, result)
                    cbs_count[result["cbs_type"]] += 1
                else:
                    apply_failure(rec, Exception(err or "unknown"))
                    failed += 1

                done += 1
                completed_pending += 1

                if done % args.save_every == 0:
                    save_checkpoint()

                if completed_pending % 20 == 0 or completed_pending == len(pending_indices):
                    print(
                        f"Progress {done}/{len(coop_indices)} | "
                        f"E1={subtype_count['E1']} E2={subtype_count['E2']} E3={subtype_count['E3']} failed={failed}"
                    )

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Done.")
    print(f"Output: {out_path}")
    print(f"Processed: {done}, Failed: {failed}")
    print(f"CBS distribution: {cbs_count}")


if __name__ == "__main__":
    main()
