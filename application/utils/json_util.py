from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any


def safe_serialize(obj: Any) -> Any:
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    if isinstance(obj, bytes):
        return obj.decode("utf-8", errors="ignore")

    if isinstance(obj, Path):
        return str(obj)

    if hasattr(obj, "numerator") and hasattr(obj, "denominator"):
        try:
            return float(obj)
        except Exception:
            pass

    if isinstance(obj, dict):
        return {str(k): safe_serialize(v) for k, v in obj.items()}

    if isinstance(obj, (list, tuple, set)):
        return [safe_serialize(v) for v in obj]

    try:
        return str(obj)
    except Exception:
        return repr(obj)


def json_default(obj: Any) -> Any:
    return safe_serialize(obj)


def safe_json_dump(payload: Any, fp, **kwargs) -> None:
    json.dump(payload, fp, default=json_default, **kwargs)
