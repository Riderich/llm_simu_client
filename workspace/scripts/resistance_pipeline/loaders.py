"""
resistance_pipeline/loaders.py
────────────────────────────────
Dataset-specific loaders for the binary resistance classification pipeline.
Produces Sample lists suitable for TransformersBinaryClassifier.

Supported formats
─────────────────
  annomi_full – labeled/annomi_binary.json     (all client utterances)
  mesc        – labeled/mesc_binary.json       (balanced client utterances)
  extes       – extes/binary.json              (all client utterances)

Each loader formats the conversation context as a single string and isolates
the target client utterance as the response field.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .types import Sample


def _format_context(context: Any, max_turns: int = 4) -> str:
    """Render a context field (list of dicts or plain string) to a string."""
    if isinstance(context, str):
        return context.strip()
    if not isinstance(context, list):
        return ""
    lines: list[str] = []
    for turn in context[-max_turns:]:
        role = turn.get("speaker", turn.get("role", ""))
        text = turn.get("content", turn.get("text", "")).strip()
        if not text:
            continue
        if role in ("therapist", "supporter", "counselor", "sys"):
            label = "咨询师"
        elif role in ("client", "seeker", "user"):
            label = "来访者"
        else:
            label = role
        lines.append(f"{label}: {text}")
    return "\n".join(lines)


def filter_unprocessed(samples: list[Sample], seen: set[str]) -> list[Sample]:
    """Remove already-processed samples (for resume support)."""
    return [s for s in samples if s.sample_id not in seen]


def _load_generic(
    path: Path,
    *,
    response_field: str = "response",
    context_field: str = "context",
    max_turns: int = 4,
    max_samples: int | None = None,
) -> list[Sample]:
    data: list[dict] = json.loads(path.read_text(encoding="utf-8"))
    if max_samples is not None:
        data = data[:max_samples]
    samples: list[Sample] = []
    for item in data:
        sid = item.get("sample_id", "")
        ctx = _format_context(item.get(context_field, ""), max_turns=max_turns)
        resp = (item.get(response_field) or "").strip()
        if not resp:
            continue
        samples.append(Sample(
            sample_id=sid,
            context=ctx,
            response=resp,
            metadata={k: v for k, v in item.items()
                      if k not in (context_field, response_field, "sample_id")},
        ))
    return samples


# ── Public loaders ────────────────────────────────────────────────────────

REPO = Path(__file__).resolve().parents[3]


def load_annomi_full(
    path: str | None = None,
    *,
    max_turns: int = 4,
    max_samples: int | None = None,
) -> list[Sample]:
    src = Path(path) if path else REPO / "workspace/results/labeled/annomi_binary.json"
    return _load_generic(src, max_turns=max_turns, max_samples=max_samples)


def load_mesc(
    path: str | None = None,
    *,
    max_turns: int = 4,
    max_samples: int | None = None,
) -> list[Sample]:
    src = Path(path) if path else REPO / "workspace/results/labeled/mesc_binary.json"
    return _load_generic(src, max_turns=max_turns, max_samples=max_samples)


def load_extes(
    path: str | None = None,
    *,
    max_turns: int = 4,
    max_samples: int | None = None,
) -> list[Sample]:
    src = Path(path) if path else REPO / "workspace/results/extes/binary.json"
    return _load_generic(src, max_turns=max_turns, max_samples=max_samples)
