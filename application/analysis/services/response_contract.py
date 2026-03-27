from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AnalysisContractResult:
    ok: bool
    reason: str | None = None


_REQUIRED_LISTING_FIELDS = ("title", "description", "tags", "materials")
_FAILURE_MARKERS = ("ANALYSIS_FAILED", "STATUS: FAILED", "STATUS=FAILED")


def _has_failure_marker(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    text = value.strip().upper()
    return any(marker in text for marker in _FAILURE_MARKERS)


def validate_analysis_response(payload: Any) -> AnalysisContractResult:
    """Validate AI analysis service output for deterministic pipeline handling.

    Expected shape:
    {
      "listing": {...},
      "metadata": {...}
    }

    This validator is intentionally strict on contract shape and required fields,
    while permissive about creative content to avoid false negatives.
    """

    if not isinstance(payload, dict):
        return AnalysisContractResult(ok=False, reason="Analysis response is not an object")

    listing = payload.get("listing")
    if not isinstance(listing, dict):
        return AnalysisContractResult(ok=False, reason="Missing listing object in analysis response")

    for field in _REQUIRED_LISTING_FIELDS:
        if field not in listing:
            return AnalysisContractResult(ok=False, reason=f"Missing required listing field: {field}")

    title = listing.get("title")
    if not isinstance(title, str) or not title.strip():
        return AnalysisContractResult(ok=False, reason="Listing title is empty")
    if _has_failure_marker(title):
        return AnalysisContractResult(ok=False, reason="AI returned explicit failure marker in title")

    description = listing.get("description")
    if not isinstance(description, str) or not description.strip():
        return AnalysisContractResult(ok=False, reason="Listing description is empty")
    if _has_failure_marker(description):
        return AnalysisContractResult(ok=False, reason="AI returned explicit failure marker in description")

    tags = listing.get("tags")
    if not isinstance(tags, list) or not tags:
        return AnalysisContractResult(ok=False, reason="Listing tags are missing or invalid")

    materials = listing.get("materials")
    if not isinstance(materials, list) or not materials:
        return AnalysisContractResult(ok=False, reason="Listing materials are missing or invalid")

    metadata = payload.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        return AnalysisContractResult(ok=False, reason="Metadata must be an object when present")

    return AnalysisContractResult(ok=True)
