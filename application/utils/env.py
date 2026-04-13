from __future__ import annotations

"""
# [S1] utils.env — Environment loader and validation

Load .env at process start, expose typed getters, and validate required keys.
Deterministic and side-effect free beyond environment loading.
"""

import os
from typing import Optional
from dotenv import load_dotenv


# Always load .env if present, allowing override of process env for deterministic runs.
load_dotenv(override=True)


class EnvError(RuntimeError):
    """Raised when required environment keys are missing or invalid."""


_DEF_BOOL_TRUE = {"1", "true", "yes", "on"}
_DEF_BOOL_FALSE = {"0", "false", "no", "off"}


def get_bool(name: str, default: bool | str = False) -> bool:
    """Return a boolean for name with tolerant parsing.

    Accepts 1/0, true/false, yes/no, on/off (case-insensitive).
    """
    val = os.getenv(name)
    if val is None:
        return bool(default) if isinstance(default, bool) else (str(default).lower() in _DEF_BOOL_TRUE)
    v = val.strip().lower()
    if v in _DEF_BOOL_TRUE:
        return True
    if v in _DEF_BOOL_FALSE:
        return False
    # Fallback: non-empty -> True
    return bool(v)


def get_int(name: str, default: int | str) -> int:
    """Return integer env with safe fallback."""
    try:
        return int(os.getenv(name, str(default)))
    except Exception:
        return int(default)


def require(key: str) -> str:
    """Return the env value or raise EnvError if missing/blank."""
    val = os.getenv(key, "").strip()
    if not val:
        raise EnvError(f"Missing required environment variable: {key}")
    return val


# Validate required keys eagerly when this module is imported by app code.
# Libraries can import getters without forcing validation.
OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY or not OPENAI_API_KEY.strip():
    # Allow tests without a real key; production code should ensure it's set.
    if os.getenv("PYTEST_CURRENT_TEST") is None:
        raise EnvError("OPENAI_API_KEY is required. Set it in .env or the environment.")

# Provide sane defaults for optional OpenAI config
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_MAX_OUTPUT_TOKENS = get_int("OPENAI_MAX_OUTPUT_TOKENS", 256)
OPENAI_TIMEOUT_SECONDS = get_int("OPENAI_TIMEOUT_SECONDS", 60)
OPENAI_RETRY_LIMIT = get_int("OPENAI_RETRY_LIMIT", 1)
VIDEO_ENABLED = get_bool("VIDEO_ENABLED", False)
