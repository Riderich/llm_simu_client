"""
Build labeled/esconv_utterances.json (flat rows with context + response) from
views/esconv.json for run_cbs_labeling.py --dataset esconv.

sample_id format matches build_character_view._build_esconv_id_map.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "data_scripts"))
from build_character_view import _build_esconv_id_map  # noqa: E402

DATASET = REPO / "workspace/dataset/ESConv.json"
VIEWS = REPO / "workspace/results/views/esconv.json"
OUT = REPO / "workspace/results/labeled/esconv_utterances.json"


def main() -> None:
    raw = json.loads(DATASET.read_text(encoding="utf-8"))
    views = json.loads(VIEWS.read_text(encoding="utf-8"))
    id_map = _build_esconv_id_map(raw)

    # Index view labels by (dlg_idx inferred from character_id)
    lab: dict[tuple[int, int], str] = {}
    for dlg in views:
        cid = dlg.get("character_id", "")
        dlg_idx = int(cid.split("_", 1)[1])
        for t in dlg.get("dialogue", []):
            if t.get("speaker") != "client":
                continue
            pos = t.get("turn_pos")
            bl = t.get("binary_label")
            if bl in ("阻抗", "合作"):
                lab[(dlg_idx, int(pos))] = bl

    rows: list[dict] = []
    for dlg_idx, item in enumerate(raw):
        turns = item.get("dialog", [])
        for pos, turn in enumerate(turns):
            if turn.get("speaker") != "seeker":
                continue
            key = (dlg_idx, pos)
            if key not in lab:
                continue
            sid = id_map.get(key)
            if not sid:
                continue
            ctx_turns = []
            for p2, t2 in enumerate(turns):
                if p2 >= pos:
                    break
                sp = t2.get("speaker", "")
                role = "seeker" if sp == "seeker" else "supporter"
                ctx_turns.append({
                    "speaker": role,
                    "content": (t2.get("content") or "").strip(),
                })
            rows.append({
                "sample_id": sid,
                "binary_label": lab[key],
                "context": ctx_turns,
                "response": (turn.get("content") or "").strip(),
            })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(rows)} rows → {OUT}")


if __name__ == "__main__":
    main()
