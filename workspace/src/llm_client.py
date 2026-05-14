from __future__ import annotations

import os
import time
from typing import Any, Final

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
_DEEPSEEK_KEY_ENV: Final = "DEEPSEEK_API_KEY"
_DEEPSEEK_BASE_ENV: Final = "DEEPSEEK_BASE_URL"
_DEEPSEEK_THINKING_ENV: Final = "DEEPSEEK_THINKING"
_DEEPSEEK_REASONING_EFFORT_ENV: Final = "DEEPSEEK_REASONING_EFFORT"

_RETRY_DELAYS: Final[tuple[float, ...]] = (2.0, 5.0, 15.0)  # exponential backoff

_UNSET: Final[Any] = object()


def _normalize_deepseek_thinking(raw: str | None) -> str:
    t = (raw or "disabled").strip().lower()
    return t if t in ("disabled", "enabled") else "disabled"


def build_deepseek_completion_extras(
    model: str,
    *,
    thinking: str | None = None,
    reasoning_effort: str | None = None,
) -> dict[str, Any]:
    """
    Extra kwargs for ``chat.completions.create`` on DeepSeek (vendor + OpenAI-style).

    - ``extra_body``: ``{"thinking": {"type": "enabled"|"disabled"}}`` (DeepSeek)
    - ``reasoning_effort``: e.g. ``"high"``, only sent when non-empty

    Non-``deepseek*`` models return an empty dict.
    """
    if not model.lower().startswith("deepseek"):
        return {}
    think = _normalize_deepseek_thinking(
        thinking if thinking is not None else os.getenv(_DEEPSEEK_THINKING_ENV, "disabled")
    )
    reff_raw = (
        reasoning_effort
        if reasoning_effort is not None
        else os.getenv(_DEEPSEEK_REASONING_EFFORT_ENV, "")
    )
    reff = (reff_raw or "").strip() or None
    out: dict[str, Any] = {"extra_body": {"thinking": {"type": think}}}
    if reff:
        out["reasoning_effort"] = reff
    return out


def _normalize_deepseek_base(url: str) -> str:
    u = (url or "").strip().rstrip("/")
    if not u:
        return "https://api.deepseek.com/v1"
    if u.endswith("/v1"):
        return u
    return f"{u}/v1"


def _resolve_client(model: str, api_key: str | None, base_url: str | None) -> OpenAI:
    """Route model name to the right API endpoint and key."""
    ml = model.lower()
    if ml.startswith("qwen"):
        resolved_key = api_key or os.getenv(_QWEN_KEY_ENV) or os.getenv(_DEFAULT_KEY_ENV)
        resolved_base = base_url or _QWEN_BASE
    elif ml.startswith("deepseek"):
        resolved_key = api_key or os.getenv(_DEEPSEEK_KEY_ENV) or os.getenv(_DEFAULT_KEY_ENV)
        resolved_base = base_url or _normalize_deepseek_base(os.getenv(_DEEPSEEK_BASE_ENV, ""))
    else:
        resolved_key = api_key or os.getenv(_DEFAULT_KEY_ENV)
        resolved_base = base_url or _DEFAULT_BASE

    if not resolved_key:
        raise EnvironmentError(
            "No API key found. For deepseek* models set DEEPSEEK_API_KEY; "
            "otherwise OPENAI_API_KEY or QWEN_API_KEY in your .env file."
        )
    return OpenAI(api_key=resolved_key, base_url=resolved_base)


class LLMClient:
    """
    Thin, retry-capable wrapper around the OpenAI-compatible chat API.

    For ``deepseek*`` models, ``chat()`` merges extras from
    :func:`build_deepseek_completion_extras` — same shape as official usage, e.g.::

        client.chat.completions.create(
            model=\"deepseek-v4-pro\",
            messages=messages,
            reasoning_effort=\"high\",
            extra_body={\"thinking\": {\"type\": \"enabled\"}},
        )

    Configure via constructor args or env: ``DEEPSEEK_THINKING`` (``enabled`` /
    ``disabled``, default ``disabled``) and ``DEEPSEEK_REASONING_EFFORT`` (e.g.
    ``high``; empty = omit).

    Retry policy: up to len(_RETRY_DELAYS) retries on transient errors
    (RateLimitError, APIError with status >= 500) with exponential back-off.
    Other errors (e.g. invalid request) are raised immediately.
    """

    def __init__(
        self,
        model: str = "deepseek-v4-flash",
        api_key: str | None = None,
        base_url: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 1500,
        *,
        deepseek_thinking: str | None = None,
        deepseek_reasoning_effort: str | None = None,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._ds_thinking = _normalize_deepseek_thinking(
            deepseek_thinking
            if deepseek_thinking is not None
            else os.getenv(_DEEPSEEK_THINKING_ENV, "disabled")
        )
        _re = (
            deepseek_reasoning_effort
            if deepseek_reasoning_effort is not None
            else os.getenv(_DEEPSEEK_REASONING_EFFORT_ENV, "")
        )
        self._ds_reasoning_effort = (_re or "").strip() or None
        self._client = _resolve_client(model, api_key, base_url)

    def chat(
        self,
        system: str,
        user: str,
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        deepseek_thinking: Any = _UNSET,
        deepseek_reasoning_effort: Any = _UNSET,
    ) -> str:
        """
        Call the model with a system + user message pair.
        Returns the assistant's response text.

        ``temperature`` and ``max_tokens`` override instance defaults when given.
        For ``deepseek*`` only: pass ``deepseek_thinking`` / ``deepseek_reasoning_effort``
        only when you want to override the values set on this client (constructor /
        env). Omit those keyword arguments to keep client defaults.
        Raises on non-retryable errors or after all retries are exhausted.
        """
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
        _temp   = temperature if temperature is not None else self.temperature
        _tokens = max_tokens  if max_tokens  is not None else self.max_tokens

        last_exc: Exception | None = None
        create_kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": _temp,
            "max_tokens": _tokens,
        }
        if deepseek_thinking is _UNSET:
            think = self._ds_thinking
        else:
            think = _normalize_deepseek_thinking(str(deepseek_thinking))
        if deepseek_reasoning_effort is _UNSET:
            reff = self._ds_reasoning_effort
        else:
            reff = (str(deepseek_reasoning_effort).strip() if deepseek_reasoning_effort else "") or None
        create_kwargs.update(
            build_deepseek_completion_extras(
                self.model,
                thinking=think,
                reasoning_effort=reff,
            )
        )

        for attempt, delay in enumerate((*_RETRY_DELAYS, None), start=1):
            try:
                response = self._client.chat.completions.create(**create_kwargs)
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
