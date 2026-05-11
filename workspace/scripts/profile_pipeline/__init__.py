"""Structured client Profile extraction pipeline.

Supports AnnoMI (English) and RECAP (Chinese) datasets.
Field names are always English; field values are in the source language.
"""

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[2] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from llm_client import LLMClient  # noqa: E402,F401  (re-export shared LLM client)
