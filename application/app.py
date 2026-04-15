import application._legacy_guard
import json
import os
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv
from flask import Flask, request, url_for, flash, session, current_app, render_template, redirect
from werkzeug.exceptions import RequestEntityTooLarge
from .config import AppConfig
from .upload.routes.upload_routes import upload_bp
from .admin.hub.routes.hub_routes import hub_bp
from .admin.analysis.routes import analysis_management_bp
from .artwork.routes.artwork_routes import artwork_bp
from .analysis.manual.routes.manual_routes import manual_bp
from .analysis.api.routes import analysis_api_bp
from .analysis.api.job_routes import job_api_bp
from .analysis.routes import analysis_bp
from .export.api.routes import export_api_bp
from .mockups.admin.routes import mockups_admin_bp, manual_artworks_bp, forge_bp, utility_bp
from .mockups.routes import mockups_bp
from .admin.settings.routes.settings_routes import settings_bp
from .admin.profile.routes.profile_routes import profile_bp
from .admin.users.routes.users_routes import users_bp
from .site.routes.site_routes import site_bp
from application.routes.auth_routes import auth_bp
from application.video.routes import video_bp, video_workspace_bp
from application.common import common_bp
from application.utils.session_tracker import SessionTracker
from application.utils.csrf import get_csrf_token
from application.logging_config import configure_logging

def init_session_tracker(flask_app: Flask) -> SessionTracker:
    """Attach a session tracker to the Flask app if not already present."""
    existing = getattr(flask_app, "session_tracker", None)
    if existing:
        return existing
    max_sessions = int(flask_app.config.get("MAX_ADMIN_SESSIONS", 5) or 5)
    namespace = (os.getenv("SESSION_TRACKER_NAMESPACE") or os.getenv("SESSION_NAMESPACE") or "default").strip() or "default"
    base_root = Path(flask_app.root_path).parent
    default_registry = base_root / "var" / "session_registry.json"
    registry_path = Path(os.getenv("SESSION_REGISTRY_FILE", flask_app.config.get("SESSION_REGISTRY_FILE", default_registry)))
    tracker = SessionTracker(max_sessions=max_sessions, namespace=namespace, registry_path=registry_path)
    setattr(flask_app, "session_tracker", tracker)
    return tracker

def create_app(config_obj: AppConfig | None = None) -> Flask:
    configure_logging()
    # Load repo-level .env so ADMIN_* and secrets are available in app.config
    repo_root = Path(__file__).resolve().parents[1]
    dotenv_path = repo_root / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path=dotenv_path, override=False)

    cfg = config_obj or AppConfig()
    
    # Warn about missing API keys at startup
    import logging
    startup_logger = logging.getLogger("artlomo.startup")
    if not os.getenv("GEMINI_API_KEY"):
        startup_logger.warning("[STARTUP] GEMINI_API_KEY not found in environment - Gemini analysis will fail")
    if not os.getenv("OPENAI_API_KEY"):
        startup_logger.warning("[STARTUP] OPENAI_API_KEY not found in environment - OpenAI analysis will fail")
    
    base_dir = Path(__file__).resolve().parent
    ui_root = base_dir / "common" / "ui"
    static_root = ui_root / "static"
    templates_root = ui_root / "templates"
    app = Flask(
        __name__,
        static_folder=str(static_root),
        template_folder=str(templates_root),
    )
    app.config.from_object(cfg)

    @app.context_processor
    def _active_preset_css_context():
        try:
            themes_dir = app.config.get("THEMES_DIR")
            if not themes_dir:
                return {"active_preset_name": "default", "active_preset_version": 0}
            active_path = Path(str(themes_dir)) / "user" / "current_style.json"
            name = "default"
            if active_path.exists():
                try:
                    raw = json.loads(active_path.read_text(encoding="utf-8"))
                    if isinstance(raw, dict) and raw.get("name"):
                        name = str(raw.get("name") or "default").strip() or "default"
                except Exception:
                    name = "default"

            css_path = Path(app.static_folder or "") / "css" / "presets" / f"{name}.css"
            if active_path.exists() and not css_path.exists():
                try:
                    from application.admin.hub.services.style_service import StyleService

                    svc = StyleService(
                        themes_dir=Path(str(themes_dir)),
                        generated_css_path=Path(str(app.config.get("THEME_GENERATED_CSS"))),
                    )
                    raw = json.loads(active_path.read_text(encoding="utf-8"))
                    if isinstance(raw, dict):
                        svc._write_css(raw)
                except Exception:
                    pass
            if not css_path.exists() and name != "default":
                name = "default"
                css_path = Path(app.static_folder or "") / "css" / "presets" / "default.css"

            version = int(css_path.stat().st_mtime) if css_path.exists() else 0
            return {"active_preset_name": name, "active_preset_version": version}
        except Exception:
            return {"active_preset_name": "default", "active_preset_version": 0}

    environment = (os.getenv("ENVIRONMENT") or str(app.config.get("ENVIRONMENT") or "")).strip().lower() or "dev"
    session_cookie_secure = environment == "prod"
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=session_cookie_secure,
        PERMANENT_SESSION_LIFETIME=timedelta(hours=12),
    )

    try:
        from application import config as app_config

        Path(app_config.LOGS_DIR).mkdir(parents=True, exist_ok=True)
        for name in ("security.log", "access.log"):
            log_path = Path(app_config.LOGS_DIR) / name
            if not log_path.exists():
                log_path.touch()
    except Exception:
        pass

    # Ensure core secrets/creds are populated from environment/.env
    app.config["ADMIN_USERNAME"] = os.getenv("ADMIN_USERNAME", app.config.get("ADMIN_USERNAME", ""))
    app.config["ADMIN_PASSWORD"] = os.getenv("ADMIN_PASSWORD", app.config.get("ADMIN_PASSWORD", ""))
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY") or os.getenv("SECRET_KEY") or app.config.get("SECRET_KEY")
    app.config["MAX_ADMIN_SESSIONS"] = int(os.getenv("MAX_ADMIN_SESSIONS", app.config.get("MAX_ADMIN_SESSIONS", 5) or 5))
    app.config["ARTLOMO_SSO_SHARED_SECRET"] = os.getenv("ARTLOMO_SSO_SHARED_SECRET", "").strip()

    app.register_blueprint(upload_bp, url_prefix="/artworks")
    # Shared UI/static blueprint (exposes endpoint `common.static` used by templates)
    app.register_blueprint(common_bp)
    app.register_blueprint(hub_bp, url_prefix="/admin/hub")
    app.register_blueprint(analysis_management_bp, url_prefix="/admin")
    app.register_blueprint(settings_bp, url_prefix="/admin")
    app.register_blueprint(profile_bp, url_prefix="/admin")
    app.register_blueprint(users_bp, url_prefix="/admin")
    app.register_blueprint(mockups_admin_bp, url_prefix="/admin/mockups")
    app.register_blueprint(utility_bp, url_prefix="/admin/mockups")
    app.register_blueprint(forge_bp)
    app.register_blueprint(manual_artworks_bp, url_prefix="")
    app.register_blueprint(manual_bp, url_prefix="/manual")
    app.register_blueprint(analysis_bp, url_prefix="/analysis")
    app.register_blueprint(artwork_bp, url_prefix="/artwork")
    app.register_blueprint(mockups_bp, url_prefix="/artwork")
    app.register_blueprint(analysis_api_bp, url_prefix="/api")
    app.register_blueprint(job_api_bp, url_prefix="/api")
    app.register_blueprint(export_api_bp, url_prefix="/api")
    app.register_blueprint(video_bp, url_prefix="/api/video")
    app.register_blueprint(video_workspace_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(site_bp, url_prefix="")

    # Per-app session tracker (limits concurrent admin sessions and tracks logouts)
    init_session_tracker(app)

    # Initialize analysis presets in database
    try:
        from application.analysis.services import AnalysisPresetService
        AnalysisPresetService.initialize_defaults(force=False)
    except Exception as e:
        startup_logger.warning("[STARTUP] Failed to initialize analysis presets: %s", e)

    @app.before_request
    def enforce_login_wall():  # pragma: no cover - integration behavior
        path = request.path or ""

        # Always allow health + static assets + auth endpoints
        if path.startswith("/static/") or path.startswith("/health"):
            return None
        if path.startswith("/auth/") or path in {"/login", "/logout"}:
            return None

        protected_prefixes = (
            "/admin",
            "/api",
            "/artworks",
            "/artwork",
            "/manual",
            "/analysis",
        )
        if not path.startswith(protected_prefixes):
            return None

        now_ts = None
        try:
            import time

            now_ts = float(time.time())
        except Exception:
            now_ts = None

        if session.get("username") and now_ts is not None:
            last_seen = session.get("last_activity_ts")
            login_ts = session.get("login_ts")
            try:
                last_seen_val = float(last_seen) if last_seen is not None else None
            except Exception:
                last_seen_val = None
            try:
                login_ts_val = float(login_ts) if login_ts is not None else None
            except Exception:
                login_ts_val = None

            inactivity_seconds = 30 * 60
            absolute_seconds = 12 * 60 * 60
            if last_seen_val is not None and (now_ts - last_seen_val) > inactivity_seconds:
                session.clear()
                return redirect(url_for("auth.login", next=path))
            if login_ts_val is not None and (now_ts - login_ts_val) > absolute_seconds:
                session.clear()
                return redirect(url_for("auth.login", next=path))
            session["last_activity_ts"] = now_ts

        if path.startswith("/admin"):
            if session.get("is_admin"):
                return None
            return redirect(url_for("auth.login", next=path))

        if session.get("username"):
            return None

        return redirect(url_for("auth.login", next=path))

    @app.context_processor
    def inject_api_status():
        return {
            "openai_configured": bool(os.getenv("OPENAI_API_KEY") or app.config.get("OPENAI_API_KEY")),
            "google_configured": bool(
                os.getenv("GEMINI_API_KEY")
                or os.getenv("GOOGLE_API_KEY")
                or app.config.get("GEMINI_API_KEY")
                or app.config.get("GOOGLE_API_KEY")
            ),
        }

    @app.context_processor
    def inject_cross_app_links():
        raw_url = str(os.getenv("DREAMARTMACHINE_BASE_URL", "http://127.0.0.1:8070") or "").strip()
        if not raw_url:
            raw_url = "http://127.0.0.1:8070"
        return {
            "dreamartmachine_url": raw_url.rstrip("/") + "/studio",
        }

    @app.context_processor
    def inject_artist_profile():  # pragma: no cover - template convenience
        profile: dict = {}
        try:
            path = Path(app.root_path) / "var" / "profile.json"
            if path.exists():
                raw = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(raw, dict):
                    profile = raw
        except Exception:
            profile = {}

        name = str(profile.get("artist_name") or "").strip()
        initials = "RC"
        if name:
            parts = [p for p in name.replace("-", " ").split() if p]
            initials = "".join([p[0] for p in parts[:2]]).upper() or initials

        image_path = str(profile.get("profile_image_path") or "").strip()

        profile_image_mtime = None
        if image_path.startswith("/static/"):
            try:
                rel = image_path[len("/static/") :]
                fs_path = Path(app.static_folder or "") / rel
                if fs_path.exists():
                    profile_image_mtime = int(fs_path.stat().st_mtime)
            except Exception:
                profile_image_mtime = None

        if profile_image_mtime is not None:
            profile = {**profile, "profile_image_mtime": profile_image_mtime}
        return {
            "artist_profile": profile,
            "artist_profile_name": name,
            "artist_profile_initials": initials,
            "artist_profile_image_path": image_path,
        }

    @app.template_global()
    def safe_url(endpoint: str, **values) -> str:  # pragma: no cover - template helper
        try:
            return url_for(endpoint, **values)
        except Exception:
            return "#"

    @app.template_global()
    def csrf_token() -> str:  # pragma: no cover - template helper
        return get_csrf_token()

    @app.after_request
    def add_cache_busting_headers(response):
        """Prevent browser caching on auth and admin pages to avoid ghost session loops."""
        path = request.path or ""
        no_cache_paths = ("/auth/login", "/login", "/admin/users", "/auth/logout", "/logout")
        if path in no_cache_paths or path.startswith("/auth/"):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        return response

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.route("/")
    def home() -> str:
        return render_template("home.html", title="ArtLomo")

    @app.route("/login", methods=["GET", "POST"])  # type: ignore[misc]
    def login_alias():
        view = current_app.view_functions.get("auth.login")
        if view:
            return view()
        next_raw = request.args.get("next")
        parsed = urlparse(str(next_raw or ""))
        next_safe = "/admin/"
        if next_raw and not parsed.scheme and not parsed.netloc and str(next_raw).startswith("/") and not str(next_raw).startswith("//"):
            next_safe = str(next_raw)
        return redirect(url_for("auth.login", next=next_safe))

    @app.route("/logout")  # type: ignore[misc]
    def logout_alias():
        view = current_app.view_functions.get("auth.logout")
        if view:
            return view()
        next_raw = request.args.get("next")
        parsed = urlparse(str(next_raw or ""))
        next_safe = url_for("auth.login")
        if next_raw and not parsed.scheme and not parsed.netloc and str(next_raw).startswith("/") and not str(next_raw).startswith("//"):
            next_safe = str(next_raw)
        return redirect(url_for("auth.logout", next=next_safe))

    @app.route("/artwork")
    def gallery_alias():
        return redirect(url_for("upload.unprocessed"))

    @app.route("/admin/")
    @app.route("/admin")
    def admin_root():
        return redirect(url_for("hub.home"))

    @app.errorhandler(RequestEntityTooLarge)
    def handle_large_file(_: RequestEntityTooLarge):
        max_mb = int((app.config.get("MAX_CONTENT_LENGTH") or 0) / (1024 * 1024)) or 500
        flash(f"File too large. Maximum allowed size is {max_mb} MB.", "danger")
        base_url = str(app.config.get("BASE_URL") or "").rstrip("/")
        mockup_ref = f"{base_url}/admin/mockups" if base_url else ""
        if request.path.startswith("/admin/mockups") or (mockup_ref and (request.referrer or "").startswith(mockup_ref)) or (request.referrer or "").startswith("/admin/mockups"):
            return redirect(url_for("mockups_admin.upload_bases")), 413
        return redirect(url_for("upload.upload_page")), 413

    @app.errorhandler(400)
    def handle_bad_request(e):
        """Handle CSRF and other 400 errors with friendly messages."""
        error_str = str(e).lower()
        if "csrf" in error_str or "token" in error_str:
            flash("Session expired for security. Please try again.", "warning")
            return redirect(url_for("auth.login"))
        return e

    return app


# Expose app at module import for Gunicorn (dev runner) without altering logic
app = create_app()


def _debug_mode() -> bool:
    return os.environ.get("DEBUG", "0").lower() in {"1", "true", "yes"}


if __name__ == "__main__":
    app = create_app()
    raw_port = os.environ.get("PORT", "8013")
    try:
        port_val = int(str(raw_port).split()[0])
    except Exception:
        port_val = 8013
    app.run(host="0.0.0.0", port=port_val, debug=_debug_mode())
