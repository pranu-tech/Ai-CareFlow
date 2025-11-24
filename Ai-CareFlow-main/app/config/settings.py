"""Configuration helpers for AI CareFlow.

This module centralizes configuration values such as model names,
feature flags, and environment-driven settings. Using a dedicated
module keeps configuration logic separate from application code and
simplifies testing.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class ModelSettings:
    """Model-related configuration values."""

    model_name: str = "gpt-4o-mini"
    temperature: float = 0.3


@dataclass
class AppSettings:
    """Top-level application settings for AI CareFlow."""

    environment: str = "development"
    openai_api_key: str | None = None
    model: ModelSettings = field(default_factory=ModelSettings)


def load_settings() -> AppSettings:
    """Load application settings from environment variables.

    This minimal implementation only reads the OpenAI API key and
    leaves other values at their defaults.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    return AppSettings(openai_api_key=api_key)
