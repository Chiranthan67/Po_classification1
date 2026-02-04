import os
from dataclasses import dataclass


def _get_env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return value


@dataclass(frozen=True)
class Settings:
    api_key: str | None
    model: str
    temperature: float
    max_tokens: int
    timeout_s: float


def load_settings() -> Settings:
    """
    Load configuration from environment variables with safe defaults.
    Streamlit secrets can still be used as a fallback in classifier.py.
    """
    return Settings(
        api_key=_get_env("GROQ_API_KEY"),
        model=_get_env("GROQ_MODEL", "llama-3.1-8b-instant"),
        temperature=float(_get_env("GROQ_TEMPERATURE", "0.0")),
        max_tokens=int(_get_env("GROQ_MAX_TOKENS", "512")),
        timeout_s=float(_get_env("GROQ_TIMEOUT_S", "20")),
    )
