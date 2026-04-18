from __future__ import annotations

import os
import time
from typing import Final

from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, APIError, RateLimitError

# Search for .env starting from this file's location up to the repo root,
# so the client works regardless of the process's working directory.
def _find_and_load_dotenv() -> None:
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / ".env"
        if candidate.exists():
            load_dotenv(candidate)
            return
    load_dotenv()  # fallback: let python-dotenv search CWD as before

_find_and_load_dotenv()

# Model → (env_key, base_url) routing — mirrors workspace/src/context_inference.py
_QWEN_KEY_ENV: Final = "QWEN_API_KEY"
_QWEN_BASE: Final = "https://dashscope.aliyuncs.com/compatible-mode/v1"
_DEFAULT_KEY_ENV: Final = "OPENAI_API_KEY"
_DEFAULT_BASE: Final = os.getenv("OPENAI_BASE_URL", "https://api.apiplus.org/v1")

_RETRY_DELAYS: Final[tuple[float, ...]] = (2.0, 5.0, 15.0)  # exponential backoff


def _resolve_client(model: str, api_key: str | None, base_url: str | None) -> OpenAI:
    """Route model name to the right API endpoint and key."""
    if model.lower().startswith("qwen"):
        resolved_key = api_key or os.getenv(_QWEN_KEY_ENV) or os.getenv(_DEFAULT_KEY_ENV)
        resolved_base = base_url or _QWEN_BASE
    else:
        resolved_key = api_key or os.getenv(_DEFAULT_KEY_ENV)
        resolved_base = base_url or _DEFAULT_BASE

    if not resolved_key:
        raise EnvironmentError(
            "No API key found. Set OPENAI_API_KEY or QWEN_API_KEY in your .env file."
        )
    return OpenAI(api_key=resolved_key, base_url=resolved_base)


class LLMClient:
    """
    Thin, retry-capable wrapper around the OpenAI-compatible chat API.

    Retry policy: up to len(_RETRY_DELAYS) retries on transient errors
    (RateLimitError, APIError with status >= 500) with exponential back-off.
    Other errors (e.g. invalid request) are raised immediately.
    """

    def __init__(
        self,
        model: str = "deepseek-v3.2",
        api_key: str | None = None,
        base_url: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 1500,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._client = _resolve_client(model, api_key, base_url)

    def chat(
        self,
        system: str,
        user: str,
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """
        Call the model with a system + user message pair.
        Returns the assistant's response text.

        ``temperature`` and ``max_tokens`` override instance defaults when given.
        Raises on non-retryable errors or after all retries are exhausted.
        """
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
        _temp   = temperature if temperature is not None else self.temperature
        _tokens = max_tokens  if max_tokens  is not None else self.max_tokens

        last_exc: Exception | None = None
        for attempt, delay in enumerate((*_RETRY_DELAYS, None), start=1):
            try:
                response = self._client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=_temp,
                    max_tokens=_tokens,
                )
                return response.choices[0].message.content or ""

            except RateLimitError as exc:
                last_exc = exc
                if delay is None:
                    break
                print(f"  [RateLimit] attempt {attempt}, retrying in {delay}s…")
                time.sleep(delay)

            except APIError as exc:
                if exc.status_code is not None and exc.status_code < 500:
                    raise  # client error — not retryable
                last_exc = exc
                if delay is None:
                    break
                print(f"  [APIError {exc.status_code}] attempt {attempt}, retrying in {delay}s…")
                time.sleep(delay)

        raise RuntimeError(
            f"LLM call failed after {len(_RETRY_DELAYS) + 1} attempts."
        ) from last_exc
