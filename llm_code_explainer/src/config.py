"""Application configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    mode: str = "mock"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    @classmethod
    def from_env(cls, mode_override: str | None = None) -> "AppConfig":
        mode = (mode_override or os.getenv("LLM_MODE", "mock")).strip().lower()
        if mode not in {"mock", "openai"}:
            mode = "mock"
        return cls(
            mode=mode,
            openai_api_key=os.getenv("OPENAI_API_KEY", "").strip(),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini",
        )

