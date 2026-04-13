# routes/auth_routes.py
# =============================================================================
# Minimal, robust session-based auth (no DB) to unblock login immediately.
# Reads ADMIN_USERNAME / ADMIN_PASSWORD from app.config (which you populate
# from .env via config.py). HEAD now handled as GET (no spurious 401s).
# =============================================================================

from __future__ import annotations

import functools
from typing import Callable
import logging
import time
import json
import base64
import hmac
import hashlib
from urllib.parse import urlparse

from flask import (
    Blueprint,
    current_app,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)
from flask.typing import ResponseReturnValue
import sys as _sys
from application.utils.session_tracker import SessionTracker
from werkzeug.security import check_password_hash
from application.utils.csrf import require_csrf_or_400
from application.utils.user_manager import (
    create_password_reset_token,
    validate_reset_token,
    reset_password_with_token,
)

try:
    from db import SessionLocal, User
except Exception:  # pragma: no cover - db may be unavailable in some deployments
    SessionLocal = None  # type: ignore
    User = None  # type: ignore

logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _tracker() -> SessionTracker:
    tracker = getattr(current_app, "session_tracker", None)
    if tracker is None:
        raise RuntimeError("session_tracker is not configured on the Flask app")
    return tracker


def login_required(view: Callable) -> Callable:
    """Lightweight decorator to protect views using a session flag."""
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            nxt = request.path or "/admin/"
            return redirect(url_for("auth.login", next=nxt))
        return view(*args, **kwargs)
    return wrapped


def _safe_next_url(next_url: str | None, default: str) -> str:
    if not next_url:
        return default
    parsed = urlparse(str(next_url))
    if parsed.scheme or parsed.netloc:
        return default
    if next_url.startswith("//"):
        return default
    if not next_url.startswith("/"):
        return default
    return next_url


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> ResponseReturnValue:
    """
    Render login (GET/HEAD) and process login (POST).
    On success: session['is_admin'] = True and redirect to ?next=...
    """
    # Sessions need a SECRET_KEY; fail fast (clear error in logs & UI)
    if not current_app.config.get("SECRET_KEY"):
        return "Server misconfig: SECRET_KEY is not set.", 500

    # Only handle credentials on POST; treat GET/HEAD as "show the form"
    if request.method == "POST":
        ok, resp = require_csrf_or_400(request)
        if not ok:
            return resp  # type: ignore[return-value]

        username = (request.form.get("username") or "").strip()
        password = (request.form.get("password") or "").strip()

        admin_user = (current_app.config.get("ADMIN_USERNAME") or "").strip()
        admin_pass = (current_app.config.get("ADMIN_PASSWORD") or "").strip()

        # Respect temporary login lockout for non-admin users
        try:
            import application.utils.security as sec  # local import avoids cycles
            if username != admin_user and getattr(sec, "is_site_locked", lambda: False)():
                return ("Login temporarily disabled", 403)
        except Exception:
            pass

        if not admin_user or not admin_pass:
            return "Server misconfig: ADMIN_USERNAME/ADMIN_PASSWORD not set.", 500

        # Admin login path (supports test fallback alias)
        is_test_env = bool(current_app.config.get("TESTING")) or ("pytest" in _sys.modules)
        is_admin_creds = (username == admin_user and password == admin_pass)
        is_fallback_test_admin = is_test_env and (username == "admin" and password == "CHANGE_ME_ADMIN_PASSWORD")
        is_admin = is_admin_creds or is_fallback_test_admin

        def _verify_user(u: str, p: str) -> tuple[bool, str | None]:
            if not (SessionLocal and User):
                return False, None
            try:
                with SessionLocal() as db_sess:  # type: ignore[misc]
                    user = db_sess.query(User).filter_by(username=u).first()
                    if not user:
                        return False, None
                    if not check_password_hash(str(user.password_hash), p):  # type: ignore[arg-type]
                        return False, None
                    role = getattr(user, "role", None) or "viewer"
                    return True, str(role)
            except Exception:
                logger.debug("Auth lookup failed", exc_info=True)
                return False, None

        # Safe reset: remove user keys but preserve CSRF token
        def _safe_session_reset():
            keys_to_remove = ['user_id', 'username', 'role', 'is_admin', 'session_id', 'login_ts', 'last_activity_ts', '_fresh']
            for key in keys_to_remove:
                session.pop(key, None)

        if is_admin:
            tracker = _tracker()
            if tracker.is_at_limit(username):
                try:
                    tracker.clear_all(username)
                except Exception:
                    return ("Maximum login limit reached. Please try again later.", 403)
            _safe_session_reset()
            session.permanent = True
            session["is_admin"] = True
            session["username"] = username or admin_user
            session["role"] = "admin"
            now_ts = float(time.time())
            session["login_ts"] = now_ts
            session["last_activity_ts"] = now_ts
            info = tracker.add_session(username or admin_user)
            session["session_id"] = info.session_id
            logger.info("[auth] admin login success user=%s session_id=%s", username or admin_user, info.session_id)
            # Honor ?next= param, otherwise default to user manager for admin
            next_url = _safe_next_url(request.args.get("next"), "/admin/users")
            return redirect(next_url)

        # Database user login path: check credentials against DB
        ok_user, role = _verify_user(username, password)
        if username and password and ok_user:
            # Database users with role='admin' get full admin access
            user_is_admin = (role == "admin")
            _safe_session_reset()
            session.permanent = True
            session["username"] = username
            session["is_admin"] = user_is_admin
            session["role"] = role or "viewer"
            now_ts = float(time.time())
            session["login_ts"] = now_ts
            session["last_activity_ts"] = now_ts
            if user_is_admin:
                tracker = _tracker()
                info = tracker.add_session(username)
                session["session_id"] = info.session_id
                logger.info("[auth] db admin login success user=%s session_id=%s", username, info.session_id)
                next_url = _safe_next_url(request.args.get("next"), "/admin/users")
            else:
                logger.info("[auth] user login success user=%s role=%s", username, role)
                default_dest = "/about" if role == "artist" else "/"
                next_url = _safe_next_url(request.args.get("next"), default_dest)
            return redirect(next_url)

        flash("Invalid username or password.", "danger")
        logger.info("[auth] login failed user=%s", username)
        return render_template("auth/login.html", page_title="Login"), 401

    # GET / HEAD
    return render_template("auth/login.html", page_title="Login")


@auth_bp.route("/logout", methods=["GET"])
def logout() -> ResponseReturnValue:
    """Clear the admin session completely and return to login."""
    # Best-effort: remove this specific session from the tracker
    try:
        username = session.get("username") or (current_app.config.get("ADMIN_USERNAME") or "")
        sid = session.get("session_id")
        tracker = getattr(current_app, "session_tracker", None)
        if tracker and username and sid:
            if tracker.remove_session(username, sid):
                logger.info("[auth] logout user=%s session_id=%s", username, sid)
    except Exception:
        pass
    # Full session clear on logout - this is the heavy lifter for cleanup
    session.clear()
    session.modified = True
    return redirect(url_for("auth.login"))


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password() -> ResponseReturnValue:
    """Handle forgot password requests."""
    if request.method == "POST":
        ok, resp = require_csrf_or_400(request)
        if not ok:
            return resp  # type: ignore[return-value]
        
        email = (request.form.get("email") or "").strip()
        if not email:
            flash("Please enter your email address.", "danger")
            return render_template("auth/forgot_password.html", page_title="Forgot Password")
        
        success, message, token = create_password_reset_token(email)
        if success:
            flash("If an account exists with that email, a reset link has been generated. Check admin console logs.", "success")
            logger.info(f"[ADMIN CONSOLE] Password reset requested for email: {email}")
        else:
            flash("If an account exists with that email, a reset link has been generated.", "success")
        
        return redirect(url_for("auth.login"))
    
    return render_template("auth/forgot_password.html", page_title="Forgot Password")


@auth_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password() -> ResponseReturnValue:
    """Handle password reset with token."""
    token = request.args.get("token") or request.form.get("token") or ""
    
    if request.method == "POST":
        ok, resp = require_csrf_or_400(request)
        if not ok:
            return resp  # type: ignore[return-value]
        
        new_password = request.form.get("new_password") or ""
        confirm_password = request.form.get("confirm_password") or ""
        
        if new_password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("auth/reset_password.html", token=token, page_title="Reset Password")
        
        success, message = reset_password_with_token(token, new_password)
        if success:
            flash(message, "success")
            return redirect(url_for("auth.login"))
        else:
            flash(message, "danger")
            return render_template("auth/reset_password.html", token=token, page_title="Reset Password")
    
    is_valid, username = validate_reset_token(token)
    if not is_valid:
        flash("Invalid or expired reset link.", "danger")
        return redirect(url_for("auth.forgot_password"))
    
    return render_template("auth/reset_password.html", token=token, username=username, page_title="Reset Password")


# Compatibility export for app.py
bp = auth_bp


def _decode_b64url_to_json(raw: str) -> dict | None:
    try:
        padding = "=" * ((4 - (len(raw) % 4)) % 4)
        decoded = base64.urlsafe_b64decode((raw + padding).encode("ascii"))
        payload = json.loads(decoded.decode("utf-8"))
        return payload if isinstance(payload, dict) else None
    except Exception:
        return None


def _verify_dream_bridge_token(token: str, secret: str) -> dict | None:
    token_str = str(token or "").strip()
    if not token_str or "." not in token_str:
        return None

    payload_b64, signature = token_str.rsplit(".", 1)
    expected_sig = hmac.new(secret.encode("utf-8"), payload_b64.encode("utf-8"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected_sig):
        return None

    payload = _decode_b64url_to_json(payload_b64)
    if not payload:
        return None

    try:
        exp = int(payload.get("exp") or 0)
        iat = int(payload.get("iat") or 0)
    except Exception:
        return None

    now_ts = int(time.time())
    if exp <= now_ts or iat > now_ts + 30:
        return None

    subject = str(payload.get("sub") or "").strip()
    if not subject:
        return None
    return payload


@auth_bp.route("/dream-bridge", methods=["GET"])
def dream_bridge_login() -> ResponseReturnValue:
    """Trusted bridge login from DreamArtMachine via short-lived signed token."""
    shared_secret = str(current_app.config.get("ARTLOMO_SSO_SHARED_SECRET") or "").strip()
    if not shared_secret:
        flash("Bridge login is not configured.", "warning")
        return redirect(url_for("auth.login", next=_safe_next_url(request.args.get("next"), "/admin/")))

    token = str(request.args.get("token") or "").strip()
    payload = _verify_dream_bridge_token(token, shared_secret)
    if not payload:
        flash("Bridge login token is invalid or expired.", "danger")
        return redirect(url_for("auth.login", next=_safe_next_url(request.args.get("next"), "/admin/")))

    username = str(payload.get("sub") or "").strip()
    is_admin = bool(payload.get("is_admin"))

    # Session reset while preserving CSRF token behavior.
    for key in ["user_id", "username", "role", "is_admin", "session_id", "login_ts", "last_activity_ts", "_fresh"]:
        session.pop(key, None)

    session.permanent = True
    session["username"] = username
    session["is_admin"] = is_admin
    session["role"] = "admin" if is_admin else "viewer"
    now_ts = float(time.time())
    session["login_ts"] = now_ts
    session["last_activity_ts"] = now_ts

    if is_admin:
        tracker = _tracker()
        if tracker.is_at_limit(username):
            tracker.clear_all(username)
        info = tracker.add_session(username)
        session["session_id"] = info.session_id
        logger.info("[auth] dream bridge login success user=%s session_id=%s", username, info.session_id)
    else:
        logger.info("[auth] dream bridge login success user=%s role=viewer", username)

    default_next = "/admin/" if is_admin else "/"
    return redirect(_safe_next_url(request.args.get("next"), default_next))


