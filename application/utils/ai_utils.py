"""AI Response Sanitization Layer.

Provides utilities for cleaning and safely parsing AI model responses,
ensuring cross-model compatibility between OpenAI and Gemini.
"""
from __future__ import annotations

import json
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


def clean_json_response(text: str) -> str:
    """Strip markdown code blocks and other formatting from AI response text.

    Handles common patterns:
    - ```json ... ```
    - ``` ... ```
    - Leading/trailing whitespace
    - BOM characters

    Args:
        text: Raw response text from AI model.

    Returns:
        Cleaned text with markdown fencing removed.
    """
    if not text:
        return ""

    cleaned = str(text).strip()

    cleaned = cleaned.lstrip("\ufeff")

    pattern = r"^```(?:json)?\s*\n?(.*?)\n?```$"
    match = re.match(pattern, cleaned, re.DOTALL | re.IGNORECASE)
    if match:
        cleaned = match.group(1).strip()

    cleaned = re.sub(r"^```(?:json)?\s*\n?", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\n?```\s*$", "", cleaned)

    return cleaned.strip()


def safe_parse_json(text: str) -> dict[str, Any] | None:
    """Safely parse JSON from AI response text.

    Applies clean_json_response first, then attempts json.loads().
    Returns None on failure instead of raising, to prevent crashes.

    Args:
        text: Raw response text from AI model.

    Returns:
        Parsed dict if successful, None if parsing fails.
    """
    if not text:
        logger.warning("safe_parse_json received empty text")
        return None

    cleaned = clean_json_response(text)
    if not cleaned:
        logger.warning("safe_parse_json: cleaned text is empty")
        return None

    try:
        result = json.loads(cleaned)
        if isinstance(result, dict):
            return result
        logger.warning("safe_parse_json: parsed result is not a dict (type=%s)", type(result).__name__)
        return None
    except json.JSONDecodeError as exc:
        logger.error(
            "safe_parse_json: JSON decode error at line %d col %d: %s",
            exc.lineno,
            exc.colno,
            exc.msg,
        )
        logger.debug("safe_parse_json: failed text (first 500 chars): %s", cleaned[:500])
        return None
    except Exception as exc:
        logger.error("safe_parse_json: unexpected error: %s", exc)
        return None


def _is_emoji_led_paragraph(text: str) -> bool:
    """Check if a paragraph starts with an emoji or symbol (non-alphanumeric)."""
    stripped = str(text or "").lstrip()
    if not stripped:
        return False
    first = stripped[0]
    # If first char is alnum or a standard bullet/dash, it's not our emoji-led style
    if first.isalnum() or first in {"-", "*", "•"}:
        return False
    return True


def validate_pioneer_blocks(blocks: list[str]) -> list[str]:
    """Validate Pioneer story blocks and pad if necessary.

    Ensures the list has exactly 13 blocks by padding with empty strings
    if the AI returned fewer than expected. Prevents crashes in UI.
    Also checks for emoji-led paragraphs and logs warnings for issues.

    Args:
        blocks: List of story blocks (paragraphs).

    Returns:
        List of exactly 13 story blocks.
    """
    if len(blocks) != 13:
        logger.warning("Gemini returned fewer blocks than expected (got %d). Padding to 13.", len(blocks))

    # Pad with empty strings until length is 13
    padded_blocks = list(blocks)
    while len(padded_blocks) < 13:
        padded_blocks.append("")

    # Defensive: truncate if more than 13
    final_blocks = padded_blocks[:13]

    # Verify emoji-led rule (Warning only, no exception)
    for i, block in enumerate(final_blocks, start=1):
        if block and not _is_emoji_led_paragraph(block):
            logger.warning("Gemini validation issue: block %d is not emoji-led.", i)

    return final_blocks
