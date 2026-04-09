from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .types import Profile


def load_existing_profiles(path: str) -> list[dict[str, Any]]:
    """Load previously saved profiles from a JSON file. Returns [] if absent."""
    p = Path(path)
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def existing_id_set(records: list[dict[str, Any]]) -> set[str]:
    return {r["sample_id"] for r in records if r.get("sample_id")}


def save_profiles(path: str, records: list[dict[str, Any]]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def profile_to_record(profile: Profile) -> dict[str, Any]:
    return profile.to_dict()
