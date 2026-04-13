from __future__ import annotations

"""
Lightweight CSRF utilities used by admin routes.

Provides:
- get_csrf_token() -> str
- require_csrf_or_400(request) -> tuple[bool, Response|None]

Notes:
- Token is stored in session under '_csrf_token'.
- Accepted locations: header 'X-CSRF-Token', form field 'csrf_token', or JSON body 'csrf_token'.
"""

import secrets
from typing import Optional

from flask import Request, make_response, jsonify, session

_SESSION_KEY = "_csrf_token"


def get_csrf_token() -> str:
    token = session.get(_SESSION_KEY)
    if not token:
        token = secrets.token_urlsafe(32)
        session[_SESSION_KEY] = token
    return token


def _extract_token(req: Request) -> Optional[str]:
    # 1) Header (preferred for fetch/XHR)
    hdr = req.headers.get("X-CSRFToken")
    if hdr:
        return hdr.strip()
    hdr = req.headers.get("X-CSRF-Token")
    if hdr:
        return hdr.strip()
    # 2) Form field (classic POST)
    try:
        form_token = req.form.get("csrf_token") if req.form is not None else None
        if form_token:
            return form_token.strip()
    except Exception:
        pass
    # 3) JSON body (application/json)
    try:
        payload = req.get_json(silent=True) or {}
        json_token = payload.get("csrf_token")
        if isinstance(json_token, str) and json_token:
            return json_token.strip()
    except Exception:
        pass
    return None


def require_csrf_or_400(req: Request):
    """
    Return (ok, resp). When ok is False, resp is a 400 response to return immediately.
    """
    expected = session.get(_SESSION_KEY) or get_csrf_token()
    provided = _extract_token(req)
    if provided and secrets.compare_digest(str(provided), str(expected)):
        return True, None

    # Build a 400 response that works for HTML and JSON clients
    wants_json = False
    try:
        accept = (req.headers.get("Accept") or "").lower()
        wants_json = "application/json" in accept or (req.is_json is True)
    except Exception:
        wants_json = False

    if wants_json:
        return False, make_response(jsonify({"ok": False, "error": "missing or invalid csrf token"}), 400)
    return False, make_response(("Bad Request: missing or invalid csrf token", 400))
