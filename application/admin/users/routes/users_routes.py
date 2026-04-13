from __future__ import annotations

import logging
from pathlib import Path

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from application.utils.csrf import require_csrf_or_400
from application.utils.user_manager import add_user, delete_user, load_users, validate_password_complexity
from application.utils.logger_utils import log_security_event

logger = logging.getLogger(__name__)

users_bp = Blueprint(
    "admin_users",
    __name__,
    template_folder=str(Path(__file__).resolve().parents[1] / "ui" / "templates"),
)


def _require_admin():
    """Check if current user is admin."""
    return session.get("role") == "admin" or session.get("is_admin")


@users_bp.route("/users", methods=["GET"])
def users_page():
    if not _require_admin():
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for("upload.upload_page"))

    users = []
    try:
        users = load_users()
    except Exception as e:
        logger.error(f"Failed to load users: {e}")
        flash("Failed to load users.", "danger")

    return render_template("users.html", users=users)


@users_bp.route("/users/create", methods=["POST"])  # type: ignore[misc]
def create_user():
    if not _require_admin():
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for("upload.upload_page"))

    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    username = (request.form.get("username") or "").strip()
    email = (request.form.get("email") or "").strip()
    password = request.form.get("password") or ""
    confirm_password = request.form.get("confirm_password") or ""
    role = (request.form.get("role") or "artist").strip()

    if not username:
        flash("Username is required.", "danger")
        return redirect(url_for("admin_users.users_page"))

    if len(username) < 3:
        flash("Username must be at least 3 characters.", "danger")
        return redirect(url_for("admin_users.users_page"))

    is_valid, error_msg = validate_password_complexity(password)
    if not is_valid:
        flash(error_msg, "danger")
        return redirect(url_for("admin_users.users_page"))

    if password != confirm_password:
        flash("Passwords do not match.", "danger")
        return redirect(url_for("admin_users.users_page"))

    if role not in ("artist", "viewer", "admin"):
        role = "artist"
    
    if role == "admin" and not _require_admin():
        flash("Only admins can create admin users.", "danger")
        return redirect(url_for("admin_users.users_page"))

    success = add_user(username=username, role=role, password=password, email=email or None)
    if success:
        flash(f"User '{username}' created successfully with role '{role}'.", "success")
        log_security_event(
            user_id=session.get("username"),
            action="admin_create_user",
            details=f"created user={username} role={role}",
        )
    else:
        flash(f"Failed to create user '{username}'. Username or email may already exist.", "danger")

    return redirect(url_for("admin_users.users_page"))


@users_bp.route("/users/delete/<username>", methods=["POST"])  # type: ignore[misc]
def delete_user_route(username: str):
    if not _require_admin():
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for("upload.upload_page"))

    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    username_clean = (username or "").strip()
    if not username_clean:
        flash("Invalid username.", "danger")
        return redirect(url_for("admin_users.users_page"))

    current_user = session.get("username")
    if username_clean == current_user:
        flash("Cannot delete your own account.", "danger")
        return redirect(url_for("admin_users.users_page"))

    try:
        delete_user(username_clean)
        flash(f"User '{username_clean}' deleted.", "success")
        log_security_event(
            user_id=current_user,
            action="admin_delete_user",
            details=f"deleted user={username_clean}",
        )
    except Exception as e:
        logger.error(f"Failed to delete user {username_clean}: {e}")
        flash(f"Failed to delete user '{username_clean}'.", "danger")

    return redirect(url_for("admin_users.users_page"))
