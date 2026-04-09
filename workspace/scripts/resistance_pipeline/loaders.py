from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .types import Sample


def _tail_context(lines: list[str], max_turns: int) -> str:
    if max_turns <= 0:
        return "\n".join(lines)
    return "\n".join(lines[-max_turns:])


def load_annomi_full(path: str, max_turns: int = 6, max_samples: int | None = None) -> list[Sample]:
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    transcripts = data.get("transcripts", {})

    samples: list[Sample] = []
    for transcript_id, payload in transcripts.items():
        dialogue = payload.get("dialogue", [])
        running_context: list[str] = []
        client_turn_index = 0

        for turn in dialogue:
            role = turn.get("interlocutor", "")
            text = (turn.get("utterance_text") or "").strip()
            if not text:
                continue

            if role == "client":
                if running_context:
                    sample_id = f"annomi_{transcript_id}_{client_turn_index}"
                    samples.append(
                        Sample(
                            sample_id=sample_id,
                            context=_tail_context(running_context, max_turns),
                            response=text,
                            metadata={
                                "dataset": "annomi_full",
                                "transcript_id": transcript_id,
                                "utterance_id": turn.get("utterance_id"),
                                "timestamp": turn.get("timestamp"),
                                "client_talk_type": turn.get("client_talk_type"),
                            },
                        )
                    )
                    if max_samples and len(samples) >= max_samples:
                        return samples
                client_turn_index += 1

            speaker = "咨询师" if role == "therapist" else "来访者"
            running_context.append(f"{speaker}：{text}")

    return samples


def load_extes(path: str, max_turns: int = 6, max_samples: int | None = None) -> list[Sample]:
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))

    samples: list[Sample] = []
    for dialog_idx, item in enumerate(data):
        turns = item.get("content", [])
        running_context: list[str] = []
        user_turn_index = 0

        for turn in turns:
            user_text = (turn.get("User") or "").strip()
            ai_text = (turn.get("AI") or "").strip()

            if user_text:
                if running_context:
                    sample_id = f"extes_{dialog_idx}_{user_turn_index}"
                    samples.append(
                        Sample(
                            sample_id=sample_id,
                            context=_tail_context(running_context, max_turns),
                            response=user_text,
                            metadata={
                                "dataset": "extes",
                                "dialog_index": dialog_idx,
                                "scene": item.get("scene"),
                                "description": item.get("description"),
                            },
                        )
                    )
                    if max_samples and len(samples) >= max_samples:
                        return samples
                running_context.append(f"来访者：{user_text}")
                user_turn_index += 1

            if ai_text:
                running_context.append(f"咨询师：{ai_text}")

    return samples


def filter_unprocessed(samples: Iterable[Sample], seen_ids: set[str]) -> list[Sample]:
    return [s for s in samples if s.sample_id not in seen_ids]

