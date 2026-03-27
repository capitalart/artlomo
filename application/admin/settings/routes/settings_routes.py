from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Any

from flask import Blueprint, current_app, jsonify, redirect, render_template, request, url_for, flash

from application.utils.csrf import require_csrf_or_400
from application.admin.hub.services.style_service import StyleService
from application.export.service import cleanup_old_exports

logger = logging.getLogger(__name__)

settings_bp = Blueprint(
    "admin_settings",
    __name__,
    template_folder=str(Path(__file__).resolve().parents[1] / "ui" / "templates"),
)


def _style_service() -> StyleService:
    cfg = current_app.config
    return StyleService(
        themes_dir=Path(cfg["THEMES_DIR"]),
        generated_css_path=Path(cfg["THEME_GENERATED_CSS"]),
    )


def _valid_preset_slug(value: str) -> bool:
    if not value:
        return False
    return re.match(r"^[a-zA-Z0-9_-]+$", value) is not None


def _env_file_path() -> Path:
    repo_root = Path(current_app.root_path).resolve().parent
    return repo_root / ".env"


def _parse_stack(raw: Any) -> list[str]:
    if raw is None:
        return []
    if isinstance(raw, (list, tuple)):
        return [str(x).strip() for x in raw if str(x).strip()]
    text = str(raw).strip()
    if not text:
        return []
    parts: list[str] = []
    for chunk in text.replace("\n", ",").split(","):
        val = str(chunk).strip()
        if val:
            parts.append(val)
    return parts


def _stack_to_env_value(stack: list[str]) -> str:
    return ",".join([s.strip() for s in stack if str(s).strip()])


def _update_dotenv_file(path: Path, updates: dict[str, str]) -> None:
    if not path.exists():
        raise FileNotFoundError(f".env not found at {path}")

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    remaining = dict(updates)
    out: list[str] = []

    hit_counts: dict[str, int] = {k: 0 for k in remaining}

    for line in lines:
        replaced_any = False
        # Preserve commented lines; only replace active assignments.
        if re.match(r"^\s*#", line):
            out.append(line)
            continue

        for key, new_val in updates.items():
            # Support both `KEY=...` and `export KEY=...` while preserving any inline comments.
            m = re.match(
                rf"^(\s*)(export\s+)?({re.escape(key)}\s*=\s*)([^\n#]*)(\s*(#.*)?)(\r?\n)?$",
                line,
            )
            if not m:
                continue

            leading_ws, export_prefix, key_prefix, _old_val, suffix, _comment, newline = m.groups()
            nl = newline if newline is not None else "\n"
            export_txt = export_prefix or ""
            out.append(f"{leading_ws}{export_txt}{key_prefix}{new_val}{suffix}{nl}")
            hit_counts[key] = hit_counts.get(key, 0) + 1
            remaining.pop(key, None)
            replaced_any = True
            break

        if not replaced_any:
            out.append(line)

    if remaining:
        if out and not out[-1].endswith("\n"):
            out[-1] = out[-1] + "\n"
        for key, val in remaining.items():
            out.append(f"{key}={val}\n")

    path.write_text("".join(out), encoding="utf-8")


def _openai_models_list() -> tuple[list[str], str | None]:
    try:
        from openai import OpenAI

        api_key = (current_app.config.get("OPENAI_API_KEY") or "").strip()
        project_id = (current_app.config.get("OPENAI_PROJECT_ID") or "").strip()
        if not api_key:
            return [], "OPENAI_API_KEY not configured"

        client = OpenAI(api_key=api_key, project=project_id or None)
        resp = client.models.list()
        data = getattr(resp, "data", None)
        if not data:
            return [], None
        ids = []
        for item in data:
            mid = getattr(item, "id", None)
            if mid:
                ids.append(str(mid))
        return sorted(set(ids)), None
    except Exception as exc:  # pylint: disable=broad-except
        return [], str(exc)


def _gemini_models_list() -> tuple[list[str], str | None]:
    try:
        api_key = (current_app.config.get("GEMINI_API_KEY") or "").strip()
        if not api_key:
            return [], "GEMINI_API_KEY not configured"

        try:
            from google import genai
        except Exception as exc:  # pylint: disable=broad-except
            return [], f"Gemini SDK not available: {exc}"

        client = genai.Client(api_key=api_key)
        models_obj = getattr(client, "models", None)
        if models_obj is None:
            return [], "Gemini client has no models interface"

        list_fn = getattr(models_obj, "list", None)
        if not callable(list_fn):
            return [], "Gemini SDK does not support models.list()"

        resp = list_fn()
        data = getattr(resp, "data", None) or resp
        ids: list[str] = []
        # Ensure data is iterable; default to empty list if not
        items = data if isinstance(data, (list, tuple)) else []
        for item in items:
            mid = getattr(item, "name", None) or getattr(item, "id", None)
            if mid:
                ids.append(str(mid))
        return sorted(set(ids)), None
    except Exception as exc:  # pylint: disable=broad-except
        return [], str(exc)


@settings_bp.route("/settings", methods=["GET", "POST"])  # type: ignore[misc]
def settings_page():
    cfg = current_app.config

    if request.method == "POST":
        ok, resp = require_csrf_or_400(request)
        if not ok:
            return resp

        openai_stack_raw = request.form.get("openai_model_stack") or ""
        gemini_stack_raw = request.form.get("gemini_model_stack") or ""

        openai_stack = _stack_to_env_value(_parse_stack(openai_stack_raw))
        gemini_stack = _stack_to_env_value(_parse_stack(gemini_stack_raw))

        env_path = _env_file_path()
        try:
            _update_dotenv_file(
                env_path,
                {
                    "OPENAI_MODEL_STACK": openai_stack,
                    "GEMINI_MODEL_STACK": gemini_stack,
                },
            )
            flash("Settings saved to .env. Restart the app to apply.", "success")
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Failed to update .env")
            flash(f"Failed to update .env: {exc}", "danger")

        return redirect(url_for("admin_settings.settings_page"))

    current_openai_stack = os.getenv("OPENAI_MODEL_STACK", "gpt-5.2,gpt-5.1,gpt-5,gpt-4o")
    current_gemini_stack = os.getenv("GEMINI_MODEL_STACK", "gemini-2.5-flash,gemini-2.5-pro")

    # Prefer Flask config when populated (app.config is derived from AppConfig),
    # but fall back to environment defaults so the form always shows something useful.
    openai_stack = cfg.get("OPENAI_MODEL_STACK") or current_openai_stack
    gemini_stack = cfg.get("GEMINI_MODEL_STACK") or current_gemini_stack

    return render_template(
        "settings.html",
        openai_model_stack=str(openai_stack),
        gemini_model_stack=str(gemini_stack),
        current_openai_stack=str(current_openai_stack),
        current_gemini_stack=str(current_gemini_stack),
        page_title="Settings",
    )


@settings_bp.get("/settings/check-latest")
def check_latest():
    openai_ids, openai_err = _openai_models_list()
    gemini_ids, gemini_err = _gemini_models_list()

    return jsonify(
        {
            "ok": True,
            "openai": {"models": openai_ids, "error": openai_err},
            "gemini": {"models": gemini_ids, "error": gemini_err},
        }
    )


@settings_bp.get("/style/load-preset/<folder>/<name>")
def load_style_preset(folder: str, name: str):
    folder = (folder or "").strip().lower()
    name = (name or "").strip()
    if folder not in {"root", "system", "user"}:
        return jsonify({"ok": False, "error": "Invalid folder"}), 400
    if not _valid_preset_slug(name):
        return jsonify({"ok": False, "error": "Invalid preset name"}), 400

    service = _style_service()
    try:
        preset = service.apply_preset(folder, name)
    except FileNotFoundError:
        return jsonify({"ok": False, "error": "Preset not found"}), 404

    return jsonify({"ok": True, "preset": preset, "presets": service.list_presets()})


@settings_bp.post("/style/save-preset")  # type: ignore[misc]
def save_style_preset():
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    service = _style_service()

    if request.is_json:
        body = request.get_json(silent=True) or {}
        raw_name = str(body.get("name") or "").strip()
        raw_values = body.get("values")
        values = raw_values if isinstance(raw_values, dict) else {}
    else:
        raw_name = str(request.form.get("name") or request.form.get("theme_name") or "").strip()
        values = {}
        for key in service.current_theme().keys():
            raw = request.form.get(key)
            if raw:
                values[key] = raw

    try:
        path = service.save_preset(raw_name, values)
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400

    return jsonify(
        {
            "ok": True,
            "folder": "user",
            "name": path.stem,
            "preset": service.current_preset(),
            "presets": service.list_presets(),
        }
    )


@settings_bp.post("/clear-export-cache")  # type: ignore[misc]
def clear_export_cache():
    """Clear old export files (older than 60 minutes by default, or all if force=true)."""
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    cfg = current_app.config
    exports_dir = Path(cfg.get("EXPORTS_DIR", ""))

    force_all = request.form.get("force") == "true" or request.args.get("force") == "true"
    max_age = 0 if force_all else 60

    deleted, errors = cleanup_old_exports(exports_dir, max_age_minutes=max_age)

    if errors > 0:
        flash(f"Cleared {deleted} export(s) with {errors} error(s).", "warning")
    elif deleted > 0:
        flash(f"Cleared {deleted} export(s) successfully.", "success")
    else:
        flash("No exports to clear.", "info")

    logger.info(f"Export cache cleared: {deleted} deleted, {errors} errors, force={force_all}")
    return redirect(url_for("admin_settings.settings_page"))
