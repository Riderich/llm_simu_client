from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Sample:
    sample_id: str
    context: str
    response: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Prediction:
    sample_id: str
    binary_label: str
    raw_output: str

