from __future__ import annotations

from typing import Sequence

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from .prompts import BINARY_INSTRUCTION
from .types import Prediction, Sample


class TransformersBinaryClassifier:
    def __init__(self, model_path: str, gpu: str = "0", max_input_tokens: int = 2048) -> None:
        self.max_input_tokens = max_input_tokens
        self.device = f"cuda:{gpu}" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
            trust_remote_code=True,
        )

    @staticmethod
    def _extract_binary_label(raw_text: str) -> str:
        first = (raw_text or "").strip().split("\n")[0]
        if "阻抗" in first:
            return "阻抗"
        if "合作" in first:
            return "合作"
        return first[:20] or "UNKNOWN"

    def predict(self, samples: Sequence[Sample]) -> list[Prediction]:
        predictions: list[Prediction] = []
        for sample in samples:
            prompt = BINARY_INSTRUCTION.format(context=sample.context, response=sample.response)
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=self.max_input_tokens,
            )
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=10,
                    do_sample=False,
                    pad_token_id=self.tokenizer.eos_token_id,
                )
            raw = self.tokenizer.decode(
                outputs[0][inputs["input_ids"].shape[1] :],
                skip_special_tokens=True,
            ).strip()
            predictions.append(
                Prediction(
                    sample_id=sample.sample_id,
                    binary_label=self._extract_binary_label(raw),
                    raw_output=raw,
                )
            )
        return predictions

