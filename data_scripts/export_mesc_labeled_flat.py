"""
Export flat impedance / cooperation tables from views/mesc.json for
data_scripts/build_character_view.py (sample_id–aligned rows).

Usage (repo root):
  python data_scripts/export_mesc_labeled_flat.py
"""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VIEWS = REPO / "workspace/results/views/mesc.json"
OUT_R = REPO / "workspace/results/labeled/mesc_resist.json"
OUT_C = REPO / "workspace/results/labeled/mesc_coop.json"


def main() -> None:
    data = json.loads(VIEWS.read_text(encoding="utf-8"))
    resist: list[dict] = []
    coop: list[dict] = []
    for dlg in data:
        cid = dlg.get("character_id", "")
        dlg_id = int(cid.split("_", 1)[1])
        client_idx = 0
        for t in dlg.get("dialogue", []):
            if t.get("speaker") != "client":
                continue
            sid = f"mesc_{dlg_id}_{client_idx}"
            text = (t.get("text") or "").strip()
            bl = t.get("binary_label")
            if bl == "阻抗":
                resist.append({
                    "sample_id": sid,
                    "binary_label": "阻抗",
                    "fine_label": t.get("fine_label"),
                    "fine_category": t.get("fine_category"),
                    "response": text,
                })
            elif bl == "合作":
                fl = t.get("fine_label") or ""
                coop.append({
                    "sample_id": sid,
                    "binary_label": "合作",
                    "cbs_type": fl if fl.startswith("CBS") else fl,
                    "response": text,
                })
            client_idx += 1

    OUT_R.write_text(json.dumps(resist, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_C.write_text(json.dumps(coop, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(resist)} → {OUT_R}")
    print(f"Wrote {len(coop)} → {OUT_C}")


if __name__ == "__main__":
    main()
