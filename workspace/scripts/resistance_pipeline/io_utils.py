from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str) -> Any:
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def write_json(path: str, payload: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_existing_results(path: str) -> list[dict]:
    data = load_json(path)
    if not data:
        return []
    if not isinstance(data, list):
        return []
    return data


def existing_id_set(records: list[dict]) -> set[str]:
    return {r.get("sample_id") for r in records if r.get("sample_id")}

