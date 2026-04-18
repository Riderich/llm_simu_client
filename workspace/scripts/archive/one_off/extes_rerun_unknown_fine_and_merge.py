"""
将 extes_resistance_fine.json 中 fine_category=Unknown 的条目，用
scripts/psychfire_resistance_fine_prompt.py 中的统一提示词全量重跑细标，
并写回同一 JSON。运行前会复制一份备份到 results/。
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import torch
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

_SCRIPTS = Path(__file__).resolve().parents[2]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from psychfire_resistance_fine_prompt import build_resistance_fine_user_prompt

WORKSPACE = Path("/data5/zxj/llm_simu_client/workspace")
FINE_PATH = WORKSPACE / "results" / "extes_resistance_fine.json"
BINARY_PATH = WORKSPACE / "results" / "extes_binary.json"
MODEL_PATH = "/data5/zxj/llm_simu_client/ClientResistance-Model-Share/only_resistance_share_model"
SAVE_EVERY = 80


LABELS_MAP = {
    "争辩-挑战": "A1",
    "争辩-贬低": "A2",
    "否认-责怪": "B1",
    "否认-不认同": "B2",
    "否认-找借口": "B3",
    "否认-最小化": "B4",
    "否认-悲观": "B5",
    "否认-犹豫": "B6",
    "否认-不愿改变": "B7",
    "回避-最小的回应": "C1",
    "回避-界限设定": "C2",
    "忽视-不关注": "D1",
    "忽视-岔开话题": "D2",
}
ALL_CODES = ("A1", "A2", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "C1", "C2", "D1", "D2")


def format_context(context, max_turns: int = 3) -> str:
    if isinstance(context, str):
        return context
    if not context:
        return ""
    lines = []
    for turn in context[-max_turns:]:
        speaker = turn.get("speaker", turn.get("role", ""))
        content = (turn.get("content") or turn.get("text") or "").strip()
        if speaker and content:
            speaker_cn = (
                "咨询师" if speaker in ("therapist", "supporter", "user") else "来访者"
            )
            lines.append(f"{speaker_cn}: {content}")
    return "\n".join(lines)


def decode_label(tokenizer, model, device, prompt: str) -> tuple[str, str]:
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1536)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=15,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    raw = tokenizer.decode(out[0][inputs["input_ids"].shape[1] :], skip_special_tokens=True).strip()
    line0 = raw.split("\n")[0].strip()
    if "#" in line0:
        line0 = line0.split("#")[0].strip()
    fine_label = line0[:24].strip()
    cat = LABELS_MAP.get(fine_label, "Unknown")
    if cat == "Unknown":
        for code in ALL_CODES:
            if code in fine_label:
                cat = code
                break
    return fine_label, cat


def main() -> None:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = FINE_PATH.with_name(f"extes_resistance_fine.pre_unknown_rerun_{ts}.json")
    shutil.copy2(FINE_PATH, backup)
    print(f"backup -> {backup}")

    fine = json.loads(FINE_PATH.read_text(encoding="utf-8"))
    binary = json.loads(BINARY_PATH.read_text(encoding="utf-8"))
    by_id = {r["sample_id"]: r for r in binary}

    unk_indices = [i for i, r in enumerate(fine) if r.get("fine_category") == "Unknown"]
    print(f"total rows {len(fine)}, unknown to rerun: {len(unk_indices)}")

    tok = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH, torch_dtype=torch.bfloat16, trust_remote_code=True
    ).to("cuda:0")
    device = next(model.parameters()).device

    still_unknown = 0
    for k, idx in enumerate(tqdm(unk_indices, desc="Rerun Unknown")):
        row = fine[idx]
        sid = row["sample_id"]
        src = by_id[sid]
        ctx = format_context(src.get("context", ""))
        tgt = src.get("response", row.get("response", ""))
        prompt = build_resistance_fine_user_prompt(ctx, tgt)
        lab, cat = decode_label(tok, model, device, prompt)
        fine[idx]["fine_label"] = lab
        fine[idx]["fine_category"] = cat
        if cat == "Unknown":
            still_unknown += 1
        if (k + 1) % SAVE_EVERY == 0:
            FINE_PATH.write_text(json.dumps(fine, ensure_ascii=False, indent=2), encoding="utf-8")

    FINE_PATH.write_text(json.dumps(fine, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"done. still Unknown after rerun: {still_unknown}")
    print(f"wrote {FINE_PATH}")


if __name__ == "__main__":
    main()
