"""Namespaced, durable session tracker.

Sessions are stored per-namespace in a small JSON registry on disk so that
Gunicorn workers share state while tests can isolate themselves by setting
``SESSION_TRACKER_NAMESPACE``. State is only mutated while holding an fcntl
lock to avoid cross-process races.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional
import fcntl
import json
import logging
import os
import time
import uuid

import application.config as config
from application.utils.json_util import safe_json_dump

logger = logging.getLogger(__name__)


@dataclass
class SessionInfo:
    session_id: str
    username: str
    created_at: float


class SessionTracker:
    def __init__(
        self,
        *,
        max_sessions: int | None = None,
        namespace: str | None = None,
        registry_path: Path | None = None,
    ) -> None:
        self._max_sessions = max_sessions
        self._namespace = (namespace or os.getenv("SESSION_TRACKER_NAMESPACE") or "default").strip() or "default"
        base = Path(getattr(config, "STATE_DIR", Path("var/state")))
        candidate = registry_path or os.getenv("SESSION_REGISTRY_FILE") or getattr(config, "SESSION_REGISTRY_FILE", base / "session_registry.json")
        self._registry_path = Path(candidate)
        if not self._registry_path.is_absolute():
            self._registry_path = base / self._registry_path
        self._registry_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._registry_path.exists():
            self._registry_path.write_text("{}", encoding="utf-8")

    @property
    def namespace(self) -> str:
        return self._namespace

    @property
    def max_sessions(self) -> int | None:
        return self._max_sessions

    def _locked_file(self):
        self._registry_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._registry_path.exists():
            # Ensure the registry file exists before attempting to lock it (notably for tests)
            self._registry_path.write_text("{}", encoding="utf-8")
        fh = self._registry_path.open("r+")
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        return fh

    def _load_registry(self) -> tuple[Dict[str, Dict[str, List[SessionInfo]]], object]:
        fh = self._locked_file()
        try:
            try:
                data = json.load(fh)
            except json.JSONDecodeError:
                data = {}
            return data, fh
        except Exception:
            fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
            fh.close()
            raise

    def _write_registry(self, fh, data: Dict[str, Dict[str, List[SessionInfo]]]) -> None:
        fh.seek(0)
        safe_json_dump(data, fh, ensure_ascii=True)
        fh.truncate()
        fh.flush()
        os.fsync(fh.fileno())

    def _load_namespace(self) -> tuple[Dict[str, List[SessionInfo]], tuple[Dict[str, Dict[str, List[SessionInfo]]], object]]:
        data, fh = self._load_registry()
        raw = data.get(self._namespace, {})
        sessions: Dict[str, List[SessionInfo]] = {}
        for user, items in raw.items():
            try:
                sessions[user] = [SessionInfo(**itm) for itm in items]  # type: ignore[arg-type]
            except Exception:
                sessions[user] = []
        return sessions, (data, fh)

    def _persist_namespace(self, sessions: Dict[str, List[SessionInfo]], bundle) -> None:
        data, fh = bundle
        data[self._namespace] = {
            user: [asdict(s) for s in user_sessions]
            for user, user_sessions in sessions.items()
        }
        self._write_registry(fh, data)
        fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
        fh.close()

    def active_sessions(self, username: str) -> List[dict]:
        sessions, bundle = self._load_namespace()
        try:
            return [asdict(s) for s in sessions.get(username, [])]
        finally:
            fcntl.flock(bundle[1].fileno(), fcntl.LOCK_UN)  # type: ignore[union-attr]
            bundle[1].close()  # type: ignore[union-attr]

    def is_at_limit(self, username: str) -> bool:
        if self._max_sessions is None:
            return False
        sessions, bundle = self._load_namespace()
        try:
            return len(sessions.get(username, [])) >= self._max_sessions
        finally:
            fcntl.flock(bundle[1].fileno(), fcntl.LOCK_UN)  # type: ignore[union-attr]
            bundle[1].close()  # type: ignore[union-attr]

    def add_session(self, username: str, session_id: str | None = None) -> SessionInfo:
        sid = session_id or f"sess-{uuid.uuid4().hex}"
        info = SessionInfo(session_id=sid, username=username, created_at=time.time())
        sessions, bundle = self._load_namespace()
        try:
            sessions.setdefault(username, []).append(info)
            self._persist_namespace(sessions, bundle)
            logger.info("[session] namespace=%s user=%s session_id=%s created", self._namespace, username, sid)
        except Exception:
            fcntl.flock(bundle[1].fileno(), fcntl.LOCK_UN)  # type: ignore[union-attr]
            bundle[1].close()  # type: ignore[union-attr]
            raise
        return info

    def remove_session(self, username: str, session_id: str) -> bool:
        sessions, bundle = self._load_namespace()
        try:
            items = sessions.get(username, [])
            before = len(items)
            items = [s for s in items if s.session_id != session_id]
            if items:
                sessions[username] = items
            else:
                sessions.pop(username, None)
            self._persist_namespace(sessions, bundle)
            removed = len(items) < before
            if removed:
                logger.info("[session] namespace=%s user=%s session_id=%s removed", self._namespace, username, session_id)
            return removed
        except Exception:
            fcntl.flock(bundle[1].fileno(), fcntl.LOCK_UN)  # type: ignore[union-attr]
            bundle[1].close()  # type: ignore[union-attr]
            raise

    def clear_all(self, username: str | None = None) -> None:
        sessions, bundle = self._load_namespace()
        try:
            if username:
                sessions.pop(username, None)
            else:
                sessions.clear()
            self._persist_namespace(sessions, bundle)
            logger.info("[session] namespace=%s cleared user=%s", self._namespace, username or "<all>")
        except Exception:
            fcntl.flock(bundle[1].fileno(), fcntl.LOCK_UN)  # type: ignore[union-attr]
            bundle[1].close()  # type: ignore[union-attr]
            raise

    def rebind(self, namespace: Optional[str] = None) -> None:
        """Point this tracker at a new namespace (used by tests)."""
        new_ns = (namespace or os.getenv("SESSION_TRACKER_NAMESPACE") or "default").strip() or "default"
        self._namespace = new_ns
