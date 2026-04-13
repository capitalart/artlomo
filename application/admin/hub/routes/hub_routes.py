from pathlib import Path

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for, jsonify

from ..services.style_service import DEFAULTS, StyleService
from application.utils.csrf import require_csrf_or_400

hub_bp = Blueprint(
    "hub",
    __name__,
    template_folder=str(Path(__file__).resolve().parents[1] / "aui" / "templates"),
    static_folder=str(Path(__file__).resolve().parents[1] / "aui" / "static"),
    static_url_path="/admin/hub/static",
)


def _service() -> StyleService:
    cfg = current_app.config
    return StyleService(
        themes_dir=Path(cfg["THEMES_DIR"]),
        generated_css_path=Path(cfg["THEME_GENERATED_CSS"]),
    )


@hub_bp.route("/", methods=["GET"])
def home():
    return render_template("hub_home.html")


@hub_bp.route("/style", methods=["GET"])
def style_legacy_redirect():
    return redirect(url_for("hub.style_editor"))


@hub_bp.route("/style-editor", methods=["GET", "POST"])  # type: ignore[misc]
def style_editor():
    service = _service()
    if request.method == "POST":
        ok, resp = require_csrf_or_400(request)
        if not ok:
            return resp
        action = (request.form.get("action") or "save").strip() or "save"
        if action == "restore":
            service.restore_defaults()
            flash("Theme restored to defaults.", "success")
        else:
            payload = service.parse_form(request.form)
            service.save_theme(payload)
            flash("Theme saved and applied.", "success")
        return redirect(url_for("hub.style_editor"))

    return render_template(
        "style_editor.html",
        defaults=DEFAULTS,
        current=service.current_preset(),
        presets=service.list_presets(),
    )


@hub_bp.post("/style/save")  # type: ignore[misc]
def style_save():
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    service = _service()
    body = request.get_json(silent=True) if request.is_json else None
    if not isinstance(body, dict):
        body = {}

    raw_name = str(body.get("name") or "").strip()
    raw_values = body.get("values")
    values = raw_values if isinstance(raw_values, dict) else {}

    raw_light = body.get("light")
    raw_dark = body.get("dark")
    light = raw_light if isinstance(raw_light, dict) else None
    dark = raw_dark if isinstance(raw_dark, dict) else None
    raw_custom_css = body.get("custom_css")
    if raw_custom_css is None:
        raw_custom_css = body.get("customCss")
    custom_css = str(raw_custom_css) if isinstance(raw_custom_css, str) else ""
    mode = str(body.get("mode") or "save").strip().lower() or "save"
    if mode not in {"save", "copy"}:
        mode = "save"

    try:
        if light is not None or dark is not None:
            path = service.save_root_preset_twin(
                raw_name,
                light=light or {},
                dark=dark or {},
                custom_css=custom_css,
                mode=mode,
            )
        else:
            path = service.save_root_preset(raw_name, values, mode=mode)
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400

    return jsonify(
        {
            "ok": True,
            "folder": "root",
            "name": path.stem,
            "preset": service.current_preset(),
            "presets": service.list_presets(),
        }
    )


@hub_bp.post("/style/delete")  # type: ignore[misc]
def style_delete():
    ok, resp = require_csrf_or_400(request)
    if not ok:
        return resp

    body = request.get_json(silent=True) if request.is_json else None
    if not isinstance(body, dict):
        body = {}

    folder = str(body.get("folder") or "").strip().lower()
    name = str(body.get("name") or "").strip()

    service = _service()
    try:
        current = service.delete_preset(folder, name)
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    except FileNotFoundError:
        return jsonify({"ok": False, "error": "Preset not found"}), 404

    return jsonify(
        {
            "ok": True,
            "current": current,
            "presets": service.list_presets(),
        }
    )


@hub_bp.get("/style/data")
def style_editor_data():
    service = _service()
    return jsonify(
        {
            "ok": True,
            "defaults": DEFAULTS,
            "current": service.current_preset(),
            "presets": service.list_presets(),
        }
    )
