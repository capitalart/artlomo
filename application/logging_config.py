from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys

import application.config as config


_MAX_BYTES = 10 * 1024 * 1024


def _rotating_file_handler(*, filename: str, level: int) -> RotatingFileHandler:
    Path(config.LOGS_DIR).mkdir(parents=True, exist_ok=True)
    log_path = Path(config.LOGS_DIR) / filename
    try:
        handler = RotatingFileHandler(
            log_path,
            maxBytes=_MAX_BYTES,
            backupCount=int(getattr(config, "LOG_BACKUP_COUNT", 5) or 5),
            encoding="utf-8",
        )
    except (PermissionError, OSError):
        stream_handler = logging.StreamHandler(stream=sys.stderr)
        stream_handler.setLevel(level)
        stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        return stream_handler  # type: ignore[return-value]

    handler.setLevel(level)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    return handler


def configure_logging() -> None:
    root = logging.getLogger()
    if getattr(root, "_artlomo_logging_configured", False):
        return

    level_name = str(getattr(config, "LOG_LEVEL", "INFO") or "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    root.setLevel(level)

    root.addHandler(_rotating_file_handler(filename="app.log", level=level))
    root.addHandler(_rotating_file_handler(filename="error.log", level=logging.ERROR))

    ai_logger = logging.getLogger("ai_processing")
    ai_logger.setLevel(logging.DEBUG)
    if not ai_logger.handlers:
        ai_logger.addHandler(_rotating_file_handler(filename="ai_processing.log", level=logging.DEBUG))
    ai_logger.propagate = False

    logging.getLogger("werkzeug").propagate = True

    integrate_with_gunicorn()

    setattr(root, "_artlomo_logging_configured", True)


def integrate_with_gunicorn() -> None:
    gunicorn_error = logging.getLogger("gunicorn.error")
    if not gunicorn_error.handlers:
        return

    for name in ("flask.app", "werkzeug"):
        target = logging.getLogger(name)
        target.handlers = gunicorn_error.handlers
        target.setLevel(gunicorn_error.level)
        target.propagate = False


def get_ai_logger() -> logging.Logger:
    configure_logging()
    return logging.getLogger("ai_processing")
