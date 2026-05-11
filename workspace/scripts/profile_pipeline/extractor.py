from __future__ import annotations

import json
import re

from llm_client import LLMClient  # workspace/src/llm_client.py (path injected by profile_pipeline/__init__.py)
from .prompts import get_prompts
from .types import Profile, TranscriptSample

# Matches a JSON object possibly wrapped in ```json ... ``` fences
_JSON_FENCE_RE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)
_JSON_BARE_RE = re.compile(r"\{.*\}", re.DOTALL)
# LLMs often emit trailing commas before } or ] (invalid in strict JSON).
_TRAILING_COMMA_RE = re.compile(r",\s*([}\]])")


def _fix_trailing_commas(text: str) -> str:
    """Remove JSON trailing commas (e.g. {\"a\": 1,}) until stable."""
    prev = None
    while prev != text:
        prev = text
        text = _TRAILING_COMMA_RE.sub(r"\1", text)
    return text


def _extract_json_text(raw: str) -> str:
    """Pull the first JSON object out of an LLM response."""
    m = _JSON_FENCE_RE.search(raw)
    if m:
        return m.group(1)
    m = _JSON_BARE_RE.search(raw)
    if m:
        return m.group(0)
    return raw  # fallback: let json.loads report the error


def _normalize_fields(d: dict) -> dict:
    """
    Ensure every field has a non-null, non-empty value after parsing.

    List fields default to a placeholder list; scalar fields default to a
    placeholder string. Ambivalence sub-fields default to empty string.
    These fallbacks should be rare — they only fire when the model disobeys
    the prompt despite the "never null" instruction.
    """
    _INFERRED = "(inferred) Information not available in transcript."

    # Scalar fields
    for f in ("background", "self_view_of_problem"):
        if not d.get(f):
            d[f] = _INFERRED

    # List fields
    for f in ("resistance_drivers", "values_and_stakes", "key_facts"):
        v = d.get(f)
        if not isinstance(v, list) or len(v) == 0:
            d[f] = [_INFERRED]

    # Ambivalence sub-fields
    amb = d.get("ambivalence")
    if not isinstance(amb, dict):
        d["ambivalence"] = {
            "for_change": _INFERRED,
            "against_change": _INFERRED,
        }
    else:
        for sub in ("for_change", "against_change"):
            if not amb.get(sub):
                amb[sub] = _INFERRED

    return d


def _parse_profile(sample_id: str, raw: str, model: str) -> Profile:
    """
    Parse a raw LLM response into a Profile.
    On any parse failure, returns a Profile with parse_error set
    so the caller can decide whether to retry or skip.
    """
    try:
        json_text = _extract_json_text(raw)
        json_text = _fix_trailing_commas(json_text)
        parsed = json.loads(json_text)
        parsed = _normalize_fields(parsed)
        return Profile(
            sample_id=sample_id,
            background=parsed.get("background"),
            self_view_of_problem=parsed.get("self_view_of_problem"),
            resistance_drivers=parsed.get("resistance_drivers", []),
            ambivalence=parsed.get("ambivalence", {"for_change": "", "against_change": ""}),
            values_and_stakes=parsed.get("values_and_stakes", []),
            key_facts=parsed.get("key_facts", []),
            extraction_model=model,
            raw_response=raw,
        )
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        return Profile(
            sample_id=sample_id,
            extraction_model=model,
            raw_response=raw,
            parse_error=f"{type(exc).__name__}: {exc}",
        )


class ProfileExtractor:
    """
    Extracts a Background Profile from a TranscriptSample using an LLM.

    Responsibilities:
    - Select the correct prompt language from the sample.
    - Call the LLM via LLMClient.
    - Parse and validate the JSON response.
    - Return a Profile (with parse_error set on failure, never raises).
    """

    def __init__(self, client: LLMClient) -> None:
        self._client = client

    def extract(self, sample: TranscriptSample) -> Profile:
        system_prompt, user_template = get_prompts(sample.language)
        user_message = user_template.format(transcript=sample.transcript_text)

        try:
            raw = self._client.chat(system=system_prompt, user=user_message)
        except Exception as exc:
            return Profile(
                sample_id=sample.sample_id,
                extraction_model=self._client.model,
                parse_error=f"API call failed: {exc}",
            )

        return _parse_profile(
            sample_id=sample.sample_id,
            raw=raw,
            model=self._client.model,
        )
