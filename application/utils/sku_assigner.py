# utils/sku_assigner.py
"""
Thread-safe utility for generating and tracking sequential SKUs.

This module reads from and writes to a central SKU tracker JSON file,
ensuring that each artwork receives a unique, sequential SKU.

INDEX
-----
1.  Imports
2.  Configuration & Constants
3.  SKU Management Functions
"""

# ===========================================================================
# 1. Imports
# ===========================================================================
from __future__ import annotations
import json
import logging
from pathlib import Path
import threading
import time
import re

import application.config as config

# ===========================================================================
# 2. Configuration & Constants
# ===========================================================================
SKU_PREFIX = config.SKU_CONFIG["PREFIX"]
SKU_DIGITS = config.SKU_CONFIG["DIGITS"]
SKU_LOCK_TIMEOUT_SECONDS = float(getattr(config, "SKU_LOCK_TIMEOUT_SECONDS", 2.0))

_LOCK = threading.Lock()  # for thread/process safety
logger = logging.getLogger(__name__)


# ===========================================================================
# 3. SKU Management Functions
# ===========================================================================


def compute_next_sku(last_sku: int, *, prefix: str = SKU_PREFIX, digits: int = SKU_DIGITS) -> tuple[str, int]:
    """Pure helper: return (next_sku_str, next_last_value) without I/O.

    Used by unit tests to avoid touching the filesystem.
    """
    next_sku_num = int(last_sku) + 1
    return f"{prefix}{next_sku_num:0{digits}d}", next_sku_num


def _parse_sku_number(sku: str) -> int:
    """Extract the numeric component from a SKU and validate prefix/format."""
    if not isinstance(sku, str):
        raise ValueError("sku must be a string")
    if not sku.startswith(SKU_PREFIX):
        raise ValueError(f"sku must start with prefix {SKU_PREFIX}")
    # accept separators like RJC-0001 or RJC0001
    tail = sku[len(SKU_PREFIX):]
    tail = tail.lstrip("-")
    if not tail or not re.fullmatch(r"\d+", tail):
        raise ValueError("sku numeric portion missing")
    return int(tail)


def _with_lock(timeout: float = SKU_LOCK_TIMEOUT_SECONDS):
    if not _LOCK.acquire(timeout=timeout):  # pragma: no cover - defensive, covered indirectly
        raise TimeoutError(f"Could not acquire SKU lock within {timeout} seconds")
    return True


def get_next_sku(tracker_path: Path) -> str:
    """Safely increments and returns the next sequential SKU (file-backed)."""
    _with_lock()
    try:
        try:
            if tracker_path.exists():
                with open(tracker_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    last_sku = int(data.get("last_sku", 0))
            else:
                last_sku = 0
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Could not read SKU tracker at {tracker_path}. Starting from 0. Error: {e}")
            last_sku = 0

        next_sku_str, next_sku_num = compute_next_sku(last_sku)

        try:
            tracker_path.write_text(json.dumps({"last_sku": next_sku_num}, indent=2), encoding="utf-8")
            logger.info(f"Assigned new SKU: {next_sku_str}. Tracker file updated.")
        except IOError as e:
            logger.error(f"Could not write to SKU tracker at {tracker_path}: {e}")

        return next_sku_str
    finally:
        try:
            _LOCK.release()
        except Exception:
            pass


def commit_sku(tracker_path: Path, sku: str) -> str:
    """Persist the provided SKU as the latest value without advancing further.

    Enforces monotonic, sequential progression. Raises if the incoming SKU does
    not match the expected next value to avoid silently skipping or consuming
    numbers on failure paths.
    """
    _with_lock()
    try:
        current_last = 0
        try:
            if tracker_path.exists():
                with tracker_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    current_last = int(data.get("last_sku", 0))
        except Exception as e:
            logger.warning(f"Could not read SKU tracker at {tracker_path}; assuming 0. Error: {e}")

        target_num = _parse_sku_number(sku)
        expected = current_last + 1
        if target_num != expected:
            raise ValueError(f"SKU commit refused: expected {SKU_PREFIX}{expected:0{SKU_DIGITS}d} but got {sku}")

        tracker_path.parent.mkdir(parents=True, exist_ok=True)
        tracker_path.write_text(json.dumps({"last_sku": target_num}, indent=2), encoding="utf-8")
        logger.info(f"Committed SKU: {SKU_PREFIX}{target_num:0{SKU_DIGITS}d}")
        return f"{SKU_PREFIX}{target_num:0{SKU_DIGITS}d}"
    finally:
        try:
            _LOCK.release()
        except Exception:
            pass


def peek_next_sku(tracker_path: Path) -> str:
    """Returns what the next SKU would be without incrementing the tracker."""
    _with_lock()
    try:
        try:
            if tracker_path.exists():
                with open(tracker_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    last_sku = int(data.get("last_sku", 0))
            else:
                last_sku = 0
        except (IOError, json.JSONDecodeError) as e:
            logger.warning(f"Could not read SKU tracker at {tracker_path} for peeking. Assuming 0. Error: {e}")
            last_sku = 0
        next_sku_str, _ = compute_next_sku(last_sku)
        return next_sku_str
    finally:
        try:
            _LOCK.release()
        except Exception:
            pass