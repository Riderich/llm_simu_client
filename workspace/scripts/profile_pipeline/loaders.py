from __future__ import annotations

import json
from pathlib import Path

from .types import Language, TranscriptSample


# ── Rendering helpers ─────────────────────────────────────────────────────────

def _render_annomi_dialogue(dialogue: list[dict]) -> str:
    lines: list[str] = []
    for turn in dialogue:
        role = turn.get("interlocutor", "")
        text = (turn.get("utterance_text") or "").strip()
        if not text:
            continue
        speaker = "Therapist" if role == "therapist" else "Client"
        lines.append(f"{speaker}: {text}")
    return "\n".join(lines)


def _render_recap_dialogue(dialogue: list[dict]) -> str:
    lines: list[str] = []
    for turn in dialogue:
        role = turn.get("role", "")
        text = (turn.get("content") or "").strip()
        if not text:
            continue
        speaker = "咨询师" if role == "counselor" else "来访者"
        lines.append(f"{speaker}：{text}")
    return "\n".join(lines)


def _render_label_summary(labels: list[dict]) -> str:
    """
    Build a concise annotation block from utterance-level labels.

    Each label dict has keys: turn_idx, binary_label, label, response.
    Returns empty string if no labels are available.
    """
    if not labels:
        return ""
    lines = ["", "--- BEHAVIORAL ANNOTATIONS ---",
             "The following client utterances were labeled in this conversation:"]
    for lbl in sorted(labels, key=lambda x: x["turn_idx"]):
        tag = "[RESISTANCE]" if lbl["binary_label"] == "阻抗" else "[COOPERATION]"
        category = lbl.get("label", "")
        snippet = (lbl.get("response") or "").strip().replace("\n", " ")[:80]
        lines.append(f"  {tag} {category} — \"{snippet}\"")
    return "\n".join(lines)


# ── Label file helpers ────────────────────────────────────────────────────────

def _load_label_records(paths: list[str]) -> list[dict]:
    records: list[dict] = []
    for p in paths:
        if p and Path(p).exists():
            records.extend(json.loads(Path(p).read_text(encoding="utf-8")))
    return records


def _build_esconv_label_index(records: list[dict]) -> dict[int, list[dict]]:
    """
    ESConv sample_id format: "{conv_idx}_{turn_idx}" (turn_idx = dialog array index).
    Returns {conv_idx: [label_dict, ...]} sorted by turn_idx.
    """
    index: dict[int, list[dict]] = {}
    for item in records:
        sid = item.get("sample_id", "")
        parts = sid.split("_")
        if len(parts) != 2:
            continue
        try:
            conv_idx, turn_idx = int(parts[0]), int(parts[1])
        except ValueError:
            continue
        label = item.get("cbs_type") or item.get("fine_label", "")
        index.setdefault(conv_idx, []).append({
            "turn_idx": turn_idx,
            "binary_label": item.get("binary_label", ""),
            "label": label,
            "response": item.get("response", ""),
        })
    for v in index.values():
        v.sort(key=lambda x: x["turn_idx"])
    return index


def _build_annomi_label_index(records: list[dict]) -> dict[str, list[dict]]:
    """
    AnnoMI sample_id format: "annomi_{transcript_id}_{utterance_idx}".
    Returns {transcript_id: [label_dict, ...]} sorted by utterance_idx.
    """
    index: dict[str, list[dict]] = {}
    for item in records:
        sid = item.get("sample_id", "")
        if not sid.startswith("annomi_"):
            continue
        parts = sid[len("annomi_"):].rsplit("_", 1)
        if len(parts) != 2:
            continue
        transcript_id, utt_idx_str = parts[0], parts[1]
        try:
            utt_idx = int(utt_idx_str)
        except ValueError:
            continue
        label = item.get("cbs_type") or item.get("fine_category") or item.get("fine_label", "")
        index.setdefault(transcript_id, []).append({
            "turn_idx": utt_idx,
            "binary_label": item.get("binary_label", ""),
            "label": label,
            "response": item.get("response", ""),
        })
    for v in index.values():
        v.sort(key=lambda x: x["turn_idx"])
    return index


def _build_mesc_label_index(
    dataset: list[dict],
    records: list[dict],
) -> dict[int, list[dict]]:
    """
    MESC sample_id format: "mesc_{global_idx}" where global_idx is the
    sequential index of user turns across ALL conversations.
    Returns {conv_idx: [label_dict, ...]} sorted by local turn order.
    """
    # Map global user-turn index → (conv_idx, local_turn_pos)
    global_to_conv: dict[int, tuple[int, int]] = {}
    global_idx = 0
    for conv_idx, conv in enumerate(dataset):
        local_pos = 0
        for turn in conv.get("dialog", []):
            if turn.get("speaker") == "user":
                global_to_conv[global_idx] = (conv_idx, local_pos)
                global_idx += 1
                local_pos += 1

    index: dict[int, list[dict]] = {}
    for item in records:
        sid = item.get("sample_id", "")
        if not sid.startswith("mesc_"):
            continue
        try:
            g_idx = int(sid[len("mesc_"):])
        except ValueError:
            continue
        mapping = global_to_conv.get(g_idx)
        if mapping is None:
            continue
        conv_idx, local_pos = mapping
        label = item.get("cbs_type") or item.get("fine_label", "")
        index.setdefault(conv_idx, []).append({
            "turn_idx": local_pos,
            "binary_label": item.get("binary_label", ""),
            "label": label,
            "response": item.get("response", ""),
        })
    for v in index.values():
        v.sort(key=lambda x: x["turn_idx"])
    return index


# ── Dataset loaders ───────────────────────────────────────────────────────────

def load_annomi(
    path: str,
    max_samples: int | None = None,
    label_coop_path: str | None = None,
    label_res_path: str | None = None,
    **_kwargs,
) -> list[TranscriptSample]:
    """
    One TranscriptSample per AnnoMI transcript (133 total).
    Language: English.

    If label_coop_path / label_res_path are provided (or the default result
    files exist), a behavioral annotation block is appended to each transcript
    so the profile extractor has fine-grained CBS2-8 / A1-D2 context.
    """
    coop_path = label_coop_path or "workspace/results/annomi_coop.json"
    res_path  = label_res_path  or "workspace/results/annomi_resistance.json"
    label_records = _load_label_records([coop_path, res_path])
    label_index = _build_annomi_label_index(label_records)

    data = json.loads(Path(path).read_text(encoding="utf-8"))
    transcripts = data.get("transcripts", {})

    samples: list[TranscriptSample] = []
    for transcript_id, payload in transcripts.items():
        dialogue = payload.get("dialogue", [])
        text = _render_annomi_dialogue(dialogue)
        if not text.strip():
            continue

        annotations = _render_label_summary(label_index.get(transcript_id, []))
        if annotations:
            text = text + "\n" + annotations

        samples.append(TranscriptSample(
            sample_id=f"annomi_{transcript_id}",
            transcript_text=text,
            language="en",
            metadata={
                "dataset": "annomi",
                "transcript_id": transcript_id,
                "mi_quality": payload.get("metadata", {}).get("mi_quality"),
                "topic": payload.get("metadata", {}).get("topic"),
            },
        ))
        if max_samples and len(samples) >= max_samples:
            break

    return samples


def load_recap(
    path: str,
    max_samples: int | None = None,
    **_kwargs,
) -> list[TranscriptSample]:
    """
    One TranscriptSample per unique RECAP conversation.

    RECAP samples share conversations (same dialogue prefix, different target
    utterances). We deduplicate by the full dialogue content so each unique
    conversation produces exactly one profile. The sample_id is derived from
    the first occurrence index.
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))

    seen_dialogues: dict[str, str] = {}   # dialogue_hash → sample_id
    samples: list[TranscriptSample] = []

    for idx, item in enumerate(data):
        dialogue = item.get("dialogue", [])
        text = _render_recap_dialogue(dialogue)
        if not text.strip():
            continue

        # Deduplicate: same rendered text = same conversation.
        dialogue_hash = str(hash(text))
        if dialogue_hash in seen_dialogues:
            continue

        sample_id = f"recap_{idx}"
        seen_dialogues[dialogue_hash] = sample_id

        samples.append(TranscriptSample(
            sample_id=sample_id,
            transcript_text=text,
            language="zh",
            metadata={
                "dataset": "recap",
                "source_index": idx,
                "binary_label": item.get("binary_label"),
                "mapped_category": item.get("mapped_category"),
            },
        ))
        if max_samples and len(samples) >= max_samples:
            break

    return samples


def load_esconv(
    path: str,
    max_samples: int | None = None,
    label_coop_path: str | None = None,
    label_res_path: str | None = None,
    **_kwargs,
) -> list[TranscriptSample]:
    """
    One TranscriptSample per ESConv conversation (1300 total).
    Language: English.

    If label_coop_path / label_res_path are provided, a behavioral annotation
    block is appended to each transcript for richer profile extraction context.
    Default paths point to the standard result files when not specified.
    """
    coop_path = label_coop_path or "workspace/results/esconv_coop.json"
    res_path  = label_res_path  or "workspace/results/esconv_resistance.json"
    label_records = _load_label_records([coop_path, res_path])
    label_index = _build_esconv_label_index(label_records)

    data = json.loads(Path(path).read_text(encoding="utf-8"))
    samples: list[TranscriptSample] = []

    for conv_idx, item in enumerate(data):
        situation = (item.get("situation") or "").strip()
        dialog = item.get("dialog", [])

        lines: list[str] = []
        if situation:
            lines.append(f"[Client's stated situation]: {situation}")
            lines.append("")
        for turn in dialog:
            speaker = turn.get("speaker", "")
            content = (turn.get("content") or "").strip()
            if not content:
                continue
            role = "Therapist" if speaker == "supporter" else "Client"
            lines.append(f"{role}: {content}")

        transcript = "\n".join(lines)
        annotations = _render_label_summary(label_index.get(conv_idx, []))
        if annotations:
            transcript = transcript + "\n" + annotations

        if not transcript.strip():
            continue

        samples.append(TranscriptSample(
            sample_id=f"esconv_{conv_idx}",
            transcript_text=transcript,
            language="en",
            metadata={
                "dataset": "esconv",
                "conv_index": conv_idx,
                "problem_type": item.get("problem_type"),
                "emotion_type": item.get("emotion_type"),
                "situation": situation,
            },
        ))
        if max_samples and len(samples) >= max_samples:
            break

    return samples


def load_mesc(
    path: str,
    max_samples: int | None = None,
    label_coop_path: str | None = None,
    label_res_path: str | None = None,
    **_kwargs,
) -> list[TranscriptSample]:
    """
    One TranscriptSample per MESC conversation (1019 total).
    Language: English.

    If label_coop_path / label_res_path are provided, a behavioral annotation
    block is appended to each transcript.
    Default paths point to the standard result files when not specified.
    """
    coop_path = label_coop_path or "workspace/results/mesc_coop.json"
    res_path  = label_res_path  or "workspace/results/mesc_resistance.json"

    data = json.loads(Path(path).read_text(encoding="utf-8"))

    label_records = _load_label_records([coop_path, res_path])
    label_index = _build_mesc_label_index(data, label_records)

    samples: list[TranscriptSample] = []

    for conv_idx, item in enumerate(data):
        situation = (item.get("situation") or "").strip()
        dialog = item.get("dialog", [])

        lines: list[str] = []
        if situation:
            lines.append(f"[Client's stated situation]: {situation}")
            lines.append("")
        for turn in dialog:
            speaker = turn.get("speaker", "")
            text = (turn.get("text") or "").strip()
            if not text:
                continue
            role = "Therapist" if speaker == "sys" else "Client"
            lines.append(f"{role}: {text}")

        transcript = "\n".join(lines)
        annotations = _render_label_summary(label_index.get(conv_idx, []))
        if annotations:
            transcript = transcript + "\n" + annotations

        if not transcript.strip():
            continue

        samples.append(TranscriptSample(
            sample_id=f"mesc_{conv_idx}",
            transcript_text=transcript,
            language="en",
            metadata={
                "dataset": "mesc",
                "conv_index": conv_idx,
                "dialogue_id": item.get("dialogue_id"),
                "problem_type": item.get("problem_type"),
                "situation": situation,
            },
        ))
        if max_samples and len(samples) >= max_samples:
            break

    return samples


# ── Registry ──────────────────────────────────────────────────────────────────

_LOADERS = {
    "annomi": load_annomi,
    "recap": load_recap,
    "esconv": load_esconv,
    "mesc": load_mesc,
}


def load_samples(
    data_format: str,
    path: str,
    max_samples: int | None = None,
    **kwargs,
) -> list[TranscriptSample]:
    loader = _LOADERS.get(data_format)
    if loader is None:
        raise ValueError(
            f"Unknown data_format '{data_format}'. "
            f"Available: {list(_LOADERS)}"
        )
    return loader(path, max_samples=max_samples, **kwargs)
