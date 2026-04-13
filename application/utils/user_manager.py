# utils/user_manager.py
"""
Database-backed user management utilities.

This module provides a set of functions to interact with the User model
in the database, allowing for the creation, deletion, and modification of
user accounts.

INDEX
-----
1.  Imports
2.  User Management Functions
"""

# ===========================================================================
# 1. Imports
# ===========================================================================
from __future__ import annotations
import json
import logging
import re
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import TypedDict

from werkzeug.security import generate_password_hash

from db import SessionLocal, User
from application.utils.logger_utils import log_security_event

logger = logging.getLogger(__name__)


class UserDict(TypedDict, total=False):
    id: int
    username: str
    email: str | None
    role: str
    created_at: datetime | None


def _user_to_dict(user: User) -> UserDict:
    """Convert a User ORM object to a dictionary."""
    return {  # type: ignore[return-value]
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "created_at": user.created_at,
    }


# ===========================================================================
# 2. User Management Functions
# ===========================================================================

def load_users() -> list[UserDict]:
    """Return all users from the database as dictionaries."""
    with SessionLocal() as session:
        users = session.query(User).all()
        return [_user_to_dict(u) for u in users]


def add_user(username: str, role: str = "viewer", password: str = "changeme", email: str | None = None) -> bool:
    """Create a new user if one with the same username does not already exist. Returns True on success."""
    if not isinstance(password, str) or len(password) < 12:
        logger.warning(f"Password rejected for user '{username}': minimum length is 12.")
        return False
    with SessionLocal() as session:
        if session.query(User).filter_by(username=username).first():
            logger.warning(f"Attempted to add existing user '{username}'. No action taken.")
            return False
        if email and session.query(User).filter_by(email=email).first():
            logger.warning(f"Email '{email}' already in use. No action taken.")
            return False
            
        user = User(
            username=username,
            email=email.strip() if email else None,
            password_hash=generate_password_hash(password, method="pbkdf2:sha256:600000", salt_length=16),
            role=role,
        )
        session.add(user)
        session.commit()
        logger.info(f"Successfully added new user '{username}' with role '{role}'.")
        log_security_event(user_id=username, action="user_create", details=f"role={role} email={email or ''}")
        return True


def delete_user(username: str) -> None:
    """Delete a user from the database by their username."""
    with SessionLocal() as session:
        user = session.query(User).filter_by(username=username).first()
        if user:
            session.delete(user)
            session.commit()
            logger.info(f"Successfully deleted user '{username}'.")
            log_security_event(user_id=username, action="user_delete", details="deleted")
        else:
            logger.warning(f"Attempted to delete non-existent user '{username}'.")


def set_role(username: str, role: str) -> None:
    """Update a user's role in the database."""
    with SessionLocal() as session:
        user = session.query(User).filter_by(username=username).first()
        if user:
            user.role = role  # type: ignore[misc]
            session.commit()
            logger.info(f"Successfully changed role for user '{username}' to '{role}'.")
            log_security_event(user_id=username, action="user_role_change", details=f"role={role}")
        else:
            logger.warning(f"Attempted to set role for non-existent user '{username}'.")


def get_user_by_username(username: str) -> UserDict | None:
    """Retrieve a user by username as a dictionary."""
    with SessionLocal() as session:
        user = session.query(User).filter_by(username=username).first()
        return _user_to_dict(user) if user else None


def get_user_by_email(email: str) -> UserDict | None:
    """Retrieve a user by email as a dictionary."""
    if not email:
        return None
    with SessionLocal() as session:
        user = session.query(User).filter_by(email=email.strip().lower()).first()
        if not user:
            user = session.query(User).filter_by(email=email.strip()).first()
        return _user_to_dict(user) if user else None


def validate_password_complexity(password: str) -> tuple[bool, str]:
    """
    Validate password meets complexity requirements.
    Returns (is_valid, error_message).
    """
    if not password or len(password) < 12:
        return False, "Password must be at least 12 characters."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]\\;'`~]", password):
        return False, "Password must contain at least one special character (!@#$%^&* etc)."
    return True, ""


def update_password(username: str, current_password: str, new_password: str) -> tuple[bool, str]:
    """
    Update a user's password after verifying the current password.
    Returns (success, message).
    """
    from werkzeug.security import check_password_hash
    
    is_valid, error_msg = validate_password_complexity(new_password)
    if not is_valid:
        return False, error_msg
    
    with SessionLocal() as session:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            return False, "User not found."
        
        if not check_password_hash(str(user.password_hash), current_password):  # type: ignore[arg-type]
            return False, "Current password is incorrect."
        
        user.password_hash = generate_password_hash(new_password, method="pbkdf2:sha256:600000", salt_length=16)  # type: ignore[misc]
        session.commit()
        logger.info(f"Password updated for user '{username}'.")
        log_security_event(user_id=username, action="password_change", details="password updated")
        return True, "Password updated successfully."


def update_email(username: str, new_email: str) -> tuple[bool, str]:
    """
    Update a user's email address.
    Returns (success, message).
    """
    new_email = (new_email or "").strip()
    
    with SessionLocal() as session:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            return False, "User not found."
        
        if new_email:
            existing = session.query(User).filter_by(email=new_email).first()
            if existing and existing.username != username:  # type: ignore[truthy-bool]
                return False, "Email address is already in use."
        
        old_email = user.email
        user.email = new_email if new_email else None  # type: ignore[misc]
        session.commit()
        logger.info(f"Email updated for user '{username}': {old_email} -> {new_email}")
        log_security_event(user_id=username, action="email_change", details=f"email updated to {new_email}")
        return True, "Email updated successfully."


# ===========================================================================
# 3. Password Reset Token Functions
# ===========================================================================

def _reset_tokens_path() -> Path:
    """Get the path to the reset tokens file."""
    base = Path(__file__).resolve().parents[2]
    data_dir = base / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "reset_tokens.json"


def _load_reset_tokens() -> dict:
    """Load reset tokens from file."""
    path = _reset_tokens_path()
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def _save_reset_tokens(tokens: dict) -> None:
    """Save reset tokens to file."""
    path = _reset_tokens_path()
    path.write_text(json.dumps(tokens, indent=2, default=str))


def create_password_reset_token(email: str) -> tuple[bool, str, str | None]:
    """
    Create a password reset token for the user with the given email.
    Returns (success, message, token_or_none).
    Token expires in 1 hour.
    """
    email = (email or "").strip().lower()
    if not email:
        return False, "Email address is required.", None
    
    user = get_user_by_email(email)
    if not user:
        return False, "No account found with that email address.", None
    
    token = secrets.token_urlsafe(32)
    expires_at = (datetime.utcnow() + timedelta(hours=1)).isoformat()
    
    tokens = _load_reset_tokens()
    tokens[token] = {
        "username": user.get("username", ""),  # type: ignore[typeddict-item]
        "email": email,
        "expires_at": expires_at,
        "created_at": datetime.utcnow().isoformat(),
    }
    _save_reset_tokens(tokens)
    
    username_str = user.get("username", "unknown")
    logger.info(f"[ADMIN CONSOLE] Password reset token created for user '{username_str}' (email: {email})")
    logger.info(f"[ADMIN CONSOLE] Reset link: /reset-password?token={token}")
    log_security_event(user_id=username_str, action="password_reset_requested", details=f"email={email}")
    
    return True, "Password reset link has been generated. Check admin console logs.", token


def validate_reset_token(token: str) -> tuple[bool, str | None]:
    """
    Validate a password reset token.
    Returns (is_valid, username_or_none).
    """
    if not token:
        return False, None
    
    tokens = _load_reset_tokens()
    token_data = tokens.get(token)
    
    if not token_data:
        return False, None
    
    expires_at = datetime.fromisoformat(token_data["expires_at"])
    if datetime.utcnow() > expires_at:
        del tokens[token]
        _save_reset_tokens(tokens)
        return False, None
    
    return True, token_data["username"]


def reset_password_with_token(token: str, new_password: str) -> tuple[bool, str]:
    """
    Reset a user's password using a valid reset token.
    Returns (success, message).
    """
    is_valid, username = validate_reset_token(token)
    if not is_valid or not username:
        return False, "Invalid or expired reset token."
    
    is_valid_pwd, error_msg = validate_password_complexity(new_password)
    if not is_valid_pwd:
        return False, error_msg
    
    with SessionLocal() as session:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            return False, "User not found."
        
        user.password_hash = generate_password_hash(new_password, method="pbkdf2:sha256:600000", salt_length=16)  # type: ignore[misc]
        session.commit()
    
    tokens = _load_reset_tokens()
    if token in tokens:
        del tokens[token]
        _save_reset_tokens(tokens)
    
    logger.info(f"Password reset completed for user '{username}'.")
    log_security_event(user_id=username, action="password_reset_completed", details="password reset via token")
    
    return True, "Password has been reset successfully. You can now log in."