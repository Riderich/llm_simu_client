from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


Language = Literal["en", "zh"]


@dataclass(slots=True)
class TranscriptSample:
    """One complete therapy transcript, ready for profile extraction."""

    sample_id: str
    transcript_text: str       # Full conversation rendered as plain text
    language: Language
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Profile:
    """
    Background Profile extracted from a therapy transcript.

    Field names are always English; values are in the source language.
    Fields are None when the transcript provides no reliable evidence.
    """

    sample_id: str

    # Who is this person and what is their life situation?
    background: str | None = None

    # How does the CLIENT frame the problem (their words, not a clinical label)?
    self_view_of_problem: str | None = None

    # Concrete reasons — grounded in things they said — that maintain resistance.
    resistance_drivers: list[str] = field(default_factory=list)

    # The MI ambivalence tension: what pulls toward change vs. what pulls away.
    ambivalence: dict[str, str] = field(default_factory=lambda: {
        "for_change": "",
        "against_change": "",
    })

    # Relationships, values, identities the client would not want to lose.
    values_and_stakes: list[str] = field(default_factory=list)

    # Specific verifiable details from the transcript (numbers, events, habits).
    key_facts: list[str] = field(default_factory=list)

    # ── provenance ────────────────────────────────────────────────────────────
    extraction_model: str = ""
    raw_response: str = ""
    parse_error: str = ""       # Non-empty if JSON parsing failed

    def to_dict(self) -> dict[str, Any]:
        return {
            "sample_id": self.sample_id,
            "background": self.background,
            "self_view_of_problem": self.self_view_of_problem,
            "resistance_drivers": self.resistance_drivers,
            "ambivalence": self.ambivalence,
            "values_and_stakes": self.values_and_stakes,
            "key_facts": self.key_facts,
            "extraction_model": self.extraction_model,
            "raw_response": self.raw_response,
            "parse_error": self.parse_error,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Profile:
        return cls(
            sample_id=d["sample_id"],
            background=d.get("background"),
            self_view_of_problem=d.get("self_view_of_problem"),
            resistance_drivers=d.get("resistance_drivers") or [],
            ambivalence=d.get("ambivalence") or {"for_change": "", "against_change": ""},
            values_and_stakes=d.get("values_and_stakes") or [],
            key_facts=d.get("key_facts") or [],
            extraction_model=d.get("extraction_model", ""),
            raw_response=d.get("raw_response", ""),
            parse_error=d.get("parse_error", ""),
        )
