"""Minimal DeepSeek chat client (OpenAI-compatible). Reads DEEPSEEK_* from .env."""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def _normalize_base_url(url: str) -> str:
    url = (url or "").strip().rstrip("/")
    if not url:
        return "https://api.deepseek.com/v1"
    if url.endswith("/v1"):
        return url
    return f"{url}/v1"


class DeepSeekClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.base_url = _normalize_base_url(base_url or os.getenv("DEEPSEEK_BASE_URL", ""))
        self.model = model or os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY 未设置（请检查 .env）")
        self._client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ) -> str:
        resp = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return (resp.choices[0].message.content or "").strip()
