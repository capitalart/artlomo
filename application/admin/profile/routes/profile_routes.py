from __future__ import annotations

import json
import logging
import shutil
import time
from pathlib import Path

from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

from application.utils.csrf import require_csrf_or_400
from application.utils.user_manager import delete_user, get_user_by_username, update_email, update_password
from application.utils.logger_utils import log_security_event

logger = logging.getLogger(__name__)


profile_bp = Blueprint(
    "admin_profile",
    __name__,
    template_folder=str(Path(__file__).resolve().parents[1] / "ui" / "templates"),
)


def _profile_path() -> Path:
    return Path(current_app.root_path) / "var" / "profile.json"


def _load_profile() -> dict:
    path = _profile_path()
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def _save_profile(payload: dict) -> None:
    path = _profile_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _profile_upload_dir() -> Path:
    static_root = Path(current_app.static_folder or current_app.root_path)
    return static_root / "uploads" / "profiles"


def _allowed_profile_image(filename: str) -> bool:
    ext = Path(filename).suffix.lower().lstrip(".")
    return ext in {"jpg", "jpeg", "png", "webp"}


@profile_bp.route("/profile", methods=["GET", "POST"])  # type: ignore[misc]
def profile_page():
    username = session.get("username") or ""
    user_info = None
    try:
        user_info = get_user_by_username(username) if username else None
    except Exception:
        pass

    if request.method == "POST":
        ok, resp = require_csrf_or_400(request)
        if not ok:
            return resp

        form_action = request.form.get("form_action", "save_profile")

        if form_action == "update_password":
            current_pwd = request.form.get("current_password", "")
            new_pwd = request.form.get("new_password", "")
            confirm_pwd = request.form.get("confirm_password", "")

            if new_pwd != confirm_pwd:
                flash("New passwords do not match.", "danger")
                return redirect(url_for("admin_profile.profile_page"))

            success, message = update_password(username, current_pwd, new_pwd)
            if success:
                flash(message, "success")
            else:
                flash(message, "danger")
            return redirect(url_for("admin_profile.profile_page"))

        if form_action == "update_email":
            new_email = request.form.get("email", "").strip()
            try:
                success, message = update_email(username, new_email)
                if success:
                    logger.info(f"Email updated for {username}: {new_email}")
                    flash("Email updated successfully!", "success")
                else:
                    flash(message, "danger")
            except Exception as e:
                logger.error(f"Failed to update email for {username}: {e}")
                flash("Failed to update email. Please try again.", "danger")
            return redirect(url_for("admin_profile.profile_page"))

        artist_name = str(request.form.get("artist_name") or "").strip()
        artist_story = str(request.form.get("artist_story") or "").strip()

        profile = _load_profile()

        upload = request.files.get("profile_image")
        if upload and getattr(upload, "filename", ""):
            original = str(upload.filename)
            if not _allowed_profile_image(original):
                flash("Unsupported image type. Allowed: jpg, png, webp.", "danger")
                return redirect(url_for("admin_profile.profile_page"))

            safe_name = secure_filename(original)
            if not safe_name:
                flash("Invalid filename.", "danger")
                return redirect(url_for("admin_profile.profile_page"))

            suffix = Path(safe_name).suffix.lower()
            if suffix == ".jpeg":
                suffix = ".jpg"
            if suffix.lstrip(".") not in {"jpg", "png", "webp"}:
                flash("Unsupported image type. Allowed: jpg, png, webp.", "danger")
                return redirect(url_for("admin_profile.profile_page"))

            timestamp = int(time.time())
            stored_name = f"profile_{timestamp}{suffix}"

            dest_dir = _profile_upload_dir()
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_path = dest_dir / stored_name
            upload.save(dest_path)
            profile["profile_image_path"] = f"/static/uploads/profiles/{stored_name}"

        profile["artist_name"] = artist_name
        profile["artist_story"] = artist_story
        _save_profile(profile)
        flash("Profile saved.", "success")
        return redirect(url_for("admin_profile.profile_page"))

    profile = _load_profile()
    return render_template(
        "profile.html",
        profile=profile,
        user_info=user_info,
        username=username,
    )


def _delete_user_artworks(username: str) -> tuple[int, int]:
    """
    Delete all artworks owned by the user.
    Returns (deleted_count, error_count).
    """
    cfg = current_app.config
    deleted = 0
    errors = 0

    dirs_to_scan = [
        Path(cfg.get("LAB_UNPROCESSED_DIR", "")),
        Path(cfg.get("LAB_PROCESSED_DIR", "")),
        Path(cfg.get("LAB_LOCKED_DIR", "")),
    ]

    for root_dir in dirs_to_scan:
        if not root_dir or not root_dir.exists():
            continue
        for slug_dir in root_dir.iterdir():
            if not slug_dir.is_dir():
                continue
            meta_path = slug_dir / "metadata.json"
            if not meta_path.exists():
                continue
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                if meta.get("owner_id") == username:
                    shutil.rmtree(slug_dir)
                    deleted += 1
                    logger.info(f"Deleted artwork {slug_dir.name} for user {username}")
            except Exception as e:
                logger.error(f"Failed to delete artwork {slug_dir.name}: {e}")
                errors += 1

    exports_dir = Path(cfg.get("EXPORTS_DIR", ""))
    if exports_dir and exports_dir.exists():
        for item in exports_dir.iterdir():
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                deleted += 1
            except Exception as e:
                logger.error(f"Failed to delete export {item.name}: {e}")
                errors += 1

    return deleted, errors


@profile_bp.route("/profile/delete", methods=["POST"])  # type: ignore[misc]
def delete_account():
    """Delete the current user's account and all associated data."""
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    username = session.get("username")
    if not username:
        flash("No user session found.", "danger")
        return redirect(url_for("auth.login"))

    if session.get("role") == "admin" or session.get("is_admin"):
        flash("Admin accounts cannot be deleted through this interface.", "danger")
        return redirect(url_for("admin_profile.profile_page"))

    try:
        deleted, errors = _delete_user_artworks(username)
        logger.info(f"Deleted {deleted} items for user {username} ({errors} errors)")

        delete_user(username)

        log_security_event(
            user_id=username,
            action="account_deleted",
            details=f"User deleted their account. {deleted} artworks removed.",
        )

        session.clear()
        flash("Your account has been permanently deleted.", "success")
        return redirect(url_for("auth.login"))

    except Exception as e:
        logger.error(f"Failed to delete account for {username}: {e}")
        flash("An error occurred while deleting your account. Please try again.", "danger")
        return redirect(url_for("admin_profile.profile_page"))
