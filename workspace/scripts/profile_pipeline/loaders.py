"""
profile_pipeline/loaders.py
────────────────────────────
Dataset-specific loaders that produce TranscriptSample lists for profile
extraction.  Each loader reads a clean dialogue JSON and renders utterances
into a plain-text transcript consumed by the LLM.

Supported datasets
──────────────────
  mesc   – workspace/dataset/MESC_from_csv.json                (English, no vision noise)
  esconv – workspace/dataset/ESConv.json                         (English)
  annomi – workspace/dataset/AnnoMI-full.json                    (English)
  recap  – workspace/dataset/_raw/ClientResistance_decrypted.json (Chinese)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from .types import Language, TranscriptSample

REPO = Path(__file__).resolve().parents[3]


# ── Shared transcript renderer ─────────────────────────────────────────────

def _render(turns: list[tuple[str, str]]) -> str:
    """Render (speaker_label, text) pairs as a plain-text transcript."""
    return "\n".join(f"{spk}: {txt}" for spk, txt in turns if txt.strip())


# ── Per-dataset loaders ───────────────────────────────────────────────────

def load_mesc_from_csv(path: Path | None = None) -> list[TranscriptSample]:
    """Load MESC from the clean CSV-derived source (no visual contamination)."""
    src = path or REPO / "workspace/dataset/MESC_from_csv.json"
    data = json.loads(src.read_text(encoding="utf-8"))
    samples: list[TranscriptSample] = []
    for dlg in data:
        turns = [
            ("Client" if t["speaker"] == "user" else "Therapist", t.get("text", ""))
            for t in dlg.get("dialog", [])
        ]
        samples.append(TranscriptSample(
            sample_id=f"mesc_{dlg['dialogue_id']}",
            transcript_text=_render(turns),
            language="en",
            metadata={
                "problem_type": dlg.get("problem_type", ""),
                "situation":    dlg.get("situation", ""),
            },
        ))
    return samples


def load_esconv(path: Path | None = None) -> list[TranscriptSample]:
    """Load ESConv dialogues."""
    src = path or REPO / "workspace/dataset/ESConv.json"
    data = json.loads(src.read_text(encoding="utf-8"))
    samples: list[TranscriptSample] = []
    for i, dlg in enumerate(data):
        turns = [
            ("Client" if t.get("speaker") == "seeker" else "Therapist",
             t.get("content", ""))
            for t in dlg.get("dialog", [])
        ]
        meta = dlg.get("situation", {}) if isinstance(dlg.get("situation"), dict) else {}
        samples.append(TranscriptSample(
            sample_id=f"esconv_{i}",
            transcript_text=_render(turns),
            language="en",
            metadata={
                "problem_type": meta.get("emotion_type", dlg.get("emotion_type", "")),
                "situation":    meta.get("problem",      dlg.get("problem", "")),
            },
        ))
    return samples


def load_annomi(path: Path | None = None) -> list[TranscriptSample]:
    """Load AnnoMI transcripts."""
    src = path or REPO / "workspace/dataset/AnnoMI-full.json"
    raw = json.loads(src.read_text(encoding="utf-8"))
    transcripts = raw.get("transcripts", {})
    samples: list[TranscriptSample] = []
    for tid, payload in transcripts.items():
        turns = [
            ("Client" if t.get("interlocutor") == "client" else "Therapist",
             t.get("utterance_text", ""))
            for t in payload.get("dialogue", [])
        ]
        samples.append(TranscriptSample(
            sample_id=f"annomi_{tid}",
            transcript_text=_render(turns),
            language="en",
            metadata={
                "mi_quality": payload.get("mi_quality", ""),
                "topic":      payload.get("topic", ""),
            },
        ))
    return samples


def load_recap(path: Path | None = None) -> list[TranscriptSample]:
    """
    Load RECAP (ClientResistance) dialogues.

    RECAP items have the form:
      { "dialogue": [{"role": "counselor"|"client", "content": "..."}, ...],
        "target_utterance": "...", ... }

    Each item is a unique dialogue_id × target_utterance pair; we deduplicate
    on dialogue_id to get one transcript per dialogue.
    """
    src = path or REPO / "workspace/dataset/_raw/ClientResistance_decrypted.json"
    data = json.loads(src.read_text(encoding="utf-8"))
    seen: set[str] = set()
    samples: list[TranscriptSample] = []
    for item in data:
        did = str(item.get("dialogue_id", ""))
        if did in seen:
            continue
        seen.add(did)
        turns = [
            ("来访者" if t.get("role") == "client" else "咨询师",
             t.get("content", ""))
            for t in item.get("dialogue", [])
        ]
        samples.append(TranscriptSample(
            sample_id=f"recap_{did}",
            transcript_text=_render(turns),
            language="zh",
            metadata={},
        ))
    return samples


# ── Registry ──────────────────────────────────────────────────────────────

LOADERS: dict[str, Callable[..., list[TranscriptSample]]] = {
    "mesc":   load_mesc_from_csv,
    "esconv": load_esconv,
    "annomi": load_annomi,
    "recap":  load_recap,
}


def load_dataset(dataset: str, path: Path | None = None) -> list[TranscriptSample]:
    """Load a dataset by name.  Raises KeyError for unknown datasets."""
    if dataset not in LOADERS:
        raise KeyError(
            f"Unknown dataset '{dataset}'. Choices: {sorted(LOADERS)}"
        )
    return LOADERS[dataset](path)
