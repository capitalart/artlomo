from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Set

from dotenv import load_dotenv


# =============================================================================
# Environment & helpers
# =============================================================================
PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
APPLICATION_ROOT: Path = Path(__file__).resolve().parent
DOTENV_PATH: Path = PROJECT_ROOT / ".env"
if DOTENV_PATH.exists():
    load_dotenv(dotenv_path=DOTENV_PATH, override=False)
else:
    load_dotenv(override=False)


def _env_bool(name: str, default: str = "false") -> bool:
    return (os.getenv(name, default) or "").strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: str) -> int:
    try:
        return int(os.getenv(name, default) or default)
    except Exception:
        return int(default)


def _env_float(name: str, default: str) -> float:
    try:
        return float(os.getenv(name, default) or default)
    except Exception:
        return float(default)


# =============================================================================
# Core paths (no auto-creation outside application/var)
# =============================================================================
BASE_DIR: Path = Path(os.getenv("ARTLOMO_BASE_DIR", PROJECT_ROOT)).resolve()
VAR_DIR: Path = Path(os.getenv("ARTLOMO_VAR_DIR", BASE_DIR / "var")).resolve()

SCRIPTS_DIR: Path = Path(os.getenv("SCRIPTS_DIR", BASE_DIR / "scripts"))
SETTINGS_DIR: Path = Path(os.getenv("SETTINGS_DIR", BASE_DIR / "settings"))
_logs_dir_raw = os.getenv("LOGS_DIR")
_logs_candidate: Path = (
    (BASE_DIR / _logs_dir_raw)
    if (_logs_dir_raw and not Path(_logs_dir_raw).is_absolute())
    else Path(_logs_dir_raw or (BASE_DIR / "logs"))
)
LOGS_DIR: Path = _logs_candidate
STATE_DIR: Path = Path(os.getenv("STATE_DIR", VAR_DIR / "state"))
DB_DIR: Path = Path(os.getenv("DB_DIR", VAR_DIR / "db"))
DATA_DIR: Path = Path(os.getenv("DATA_DIR", BASE_DIR / "data"))
STATIC_DIR: Path = Path(os.getenv("STATIC_DIR", BASE_DIR / "static"))
TEMPLATES_DIR: Path = Path(os.getenv("TEMPLATES_DIR", BASE_DIR / "templates"))

# Art processing roots (used by utils and services)
ART_PROCESSING_DIR: Path = Path(os.getenv("ART_PROCESSING_DIR", BASE_DIR / "art-processing"))
UNANALYSED_ROOT: Path = ART_PROCESSING_DIR / "unanalysed-artwork"
PROCESSED_ROOT: Path = ART_PROCESSING_DIR / "processed-artwork"
FINALISED_ROOT: Path = ART_PROCESSING_DIR / "finalised-artwork"
ARTWORK_VAULT_ROOT: Path = ART_PROCESSING_DIR / "artwork-vault"
ORIGINALS_DIR: Path = Path(os.getenv("ORIGINALS_DIR", ART_PROCESSING_DIR / "originals"))
ORIGINALS_STAGING_ROOT: Path = Path(os.getenv("ORIGINALS_STAGING_ROOT", ART_PROCESSING_DIR / "originals-staging"))

# Inputs/outputs
MOCKUPS_INPUT_DIR: Path = Path(os.getenv("MOCKUPS_INPUT_DIR", BASE_DIR / "inputs" / "mockups"))
MOCKUPS_CATEGORISED_INPUTS_DIR: Path = Path(os.getenv("MOCKUPS_CATEGORISED_INPUTS_DIR", MOCKUPS_INPUT_DIR / "categorised"))
SIGNATURES_DIR: Path = Path(os.getenv("SIGNATURES_DIR", BASE_DIR / "inputs" / "signatures"))
GENERIC_TEXTS_DIR: Path = Path(os.getenv("GENERIC_TEXTS_DIR", BASE_DIR / "generic_texts"))
COORDS_DIR: Path = Path(os.getenv("COORDS_DIR", BASE_DIR / "inputs" / "Coordinates"))

OUTPUTS_DIR: Path = Path(os.getenv("OUTPUTS_DIR", BASE_DIR / "outputs"))
COMPOSITES_DIR: Path = OUTPUTS_DIR / "composites"
SELECTIONS_DIR: Path = OUTPUTS_DIR / "selections"
EXPORTS_DIR: Path = Path(os.getenv("EXPORTS_DIR", OUTPUTS_DIR / "exports"))
IMPORTS_DIR: Path = Path(os.getenv("IMPORTS_DIR", OUTPUTS_DIR / "imports"))
SIGNED_DIR: Path = OUTPUTS_DIR / "signed"

# Registry & state files
DB_PATH: Path = DATA_DIR / "artlomo.sqlite3"
SKU_TRACKER: Path = SETTINGS_DIR / "sku_tracker.json"
SESSION_REGISTRY_FILE: Path = Path(os.getenv("SESSION_REGISTRY_FILE", STATE_DIR / "session_registry.json"))


def _safe_mkdir(path: Path) -> None:
    allowed_roots = {APPLICATION_ROOT.resolve(), VAR_DIR.resolve()}
    try:
        resolved = path.resolve()
        if any(str(resolved).startswith(str(root)) for root in allowed_roots):
            path.mkdir(parents=True, exist_ok=True)
    except Exception:
        return


for _p in {STATE_DIR, SESSION_REGISTRY_FILE.parent}:
    _safe_mkdir(_p)


# =============================================================================
# Network/branding
# =============================================================================
BRAND_DOMAIN = os.getenv("BRAND_DOMAIN", "artlomo.com")
HOST = os.getenv("HOST", "127.0.0.1")
PORT = _env_int("PORT", os.getenv("SERVER_PORT", "8013"))
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev").strip().lower()
BASE_URL = os.getenv("BASE_URL") or (f"https://{BRAND_DOMAIN}" if ENVIRONMENT == "prod" else f"http://{HOST}:{PORT}")


def _relative_to_base(path: Path) -> str:
    try:
        return path.resolve().relative_to(BASE_DIR).as_posix()
    except Exception:
        return path.name


PROCESSED_URL_PATH = f"/static/{_relative_to_base(PROCESSED_ROOT)}".replace("//", "/")
PROCESSED_PUBLIC_BASE = f"{BASE_URL.rstrip('/')}{PROCESSED_URL_PATH}"


def public_processed_url(rel_path: str) -> str:
    return f"{PROCESSED_PUBLIC_BASE.rstrip('/')}/{str(rel_path).lstrip('/')}"


# =============================================================================
# AI settings
# =============================================================================
# Default AI provider/model knobs (used by UI + services as a sane fallback).
# NOTE: Presets can still override provider/model per request.
DEFAULT_AI_PROVIDER = "openai"

# Vision-capable model name used for artwork/image analysis.
VISION_MODEL = "gpt-4o"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_PROJECT_ID = os.getenv("OPENAI_PROJECT_ID", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
OPENAI_DEFAULT_MODEL = os.getenv("OPENAI_DEFAULT_MODEL", OPENAI_MODEL)
OPENAI_MODEL_FALLBACK = os.getenv("OPENAI_MODEL_FALLBACK", "gpt-4o-mini")
OPENAI_MODEL_STACK = os.getenv("OPENAI_MODEL_STACK", "gpt-5.2,gpt-5.1,gpt-5,gpt-4o")
OPENAI_MIN_TOKENS_REWORD = _env_int("OPENAI_MIN_TOKENS_REWORD", "8000")
OPENAI_MAX_TOKENS_REWORD = _env_int("OPENAI_MAX_TOKENS_REWORD", "10000")

OPENAI_API_TIMEOUT = _env_float("OPENAI_API_TIMEOUT", "60.0")
OPENAI_API_RETRIES = _env_int("OPENAI_API_RETRIES", "1")
OPENAI_IMAGE_MAX_MB = _env_int("OPENAI_IMAGE_MAX_MB", "20")
ARTWORK_ANALYSIS_MAX_OUTPUT_TOKENS = _env_int("ARTWORK_ANALYSIS_MAX_OUTPUT_TOKENS", "2000")
TEMPERATURE = _env_float("TEMPERATURE", "0.2")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
GEMINI_MODEL_STACK = os.getenv("GEMINI_MODEL_STACK", "gemini-1.5-flash,gemini-1.5-pro")


# =============================================================================
# Logging
# =============================================================================
LOG_TIMESTAMP_FORMAT = "%a-%d-%b-%Y-%I-%M-%p"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_MAX_BYTES = _env_int("LOG_MAX_BYTES", str(5 * 1024 * 1024))
LOG_BACKUP_COUNT = _env_int("LOG_BACKUP_COUNT", "5")
LOG_CONFIG: Dict[str, str] = {
    "APP_STARTUP": "app-lifecycle-logs",
    "DATABASE": "database-logs",
    "SECURITY": "security-logs",
    "GUNICORN": "gunicorn",
    "UPLOAD": "upload",
    "DELETE": "delete",
    "EDITS": "edits",
    "FINALISE": "finalise",
    "LOCK": "lock",
    "ANALYZE_OPENAI": "analyse-openai",
    "ANALYZE_GOOGLE": "analyse-google",
    "COMPOSITE_GEN": "composite-generation-logs",
    "VISION": "vision-logs",
    "ROUTES": "route-logs",
    "DEFAULT": "general-logs",
}


# =============================================================================
# House paths and constraints
# =============================================================================
BUYER_LONG_EDGE = _env_int("BUYER_LONG_EDGE", "14400")
DEFAULT_ASPECT = os.getenv("DEFAULT_ASPECT", "3x4")
SKU_CONFIG = {
    "PREFIX": os.getenv("SKU_PREFIX", "RJC-"),
    "DIGITS": _env_int("SKU_DIGITS", "4"),
}
SKU_LOCK_TIMEOUT_SECONDS = _env_float("SKU_LOCK_TIMEOUT_SECONDS", "2.0")

LISTING_DEFAULTS = {
    "QUANTITY": _env_int("LISTING_DEFAULT_QUANTITY", "25"),
}

HTTP_TIMEOUT = _env_float("HTTP_TIMEOUT", "8.0")


# =============================================================================
# Flask app config (preserves existing AppConfig contract)
# =============================================================================
class AppConfig:
    """Central configuration for the clean-room ArtLomo app."""

    def __init__(self, base_dir: Path | str | None = None) -> None:
        base_override = base_dir or os.environ.get("ARTLOMO_APP_BASE")
        self.BASE_DIR: Path = Path(base_override).resolve() if base_override else Path(__file__).resolve().parent

        self.COMMON_STATIC: Path = self.BASE_DIR / "common" / "ui" / "static"
        self.COMMON_TEMPLATES: Path = self.BASE_DIR / "common" / "ui" / "templates"

        self.LAB_DIR: Path = self.BASE_DIR / "lab"
        self.LAB_UNPROCESSED_DIR: Path = self.LAB_DIR / "unprocessed"
        self.LAB_PROCESSED_DIR: Path = self.LAB_DIR / "processed"
        self.LAB_LOCKED_DIR: Path = self.LAB_DIR / "locked"
        self.LAB_INDEX_DIR: Path = self.LAB_DIR / "index"
        self.ARTWORKS_INDEX_PATH: Path = self.LAB_INDEX_DIR / "artworks.json"

        self.OUTPUTS_DIR: Path = self.BASE_DIR / "outputs"
        self.EXPORTS_DIR: Path = self.OUTPUTS_DIR / "exports"

        # Mockup catalog and preview assets
        self.MOCKUP_CATALOG_PATH: Path = self.BASE_DIR / "mockups" / "catalog" / "catalog.json"
        self.MOCKUP_PREVIEW_ART_ROOT: Path = self.BASE_DIR / "mockups" / "mockup-preview-tests"
        self.MOCKUP_PREVIEW_CACHE_ROOT: Path = self.BASE_DIR / "mockups" / "tmp" / "previews"

        self.THEMES_DIR: Path = self.BASE_DIR / "var" / "themes"
        self.SKU_SEQUENCE_PATH: Path = self.BASE_DIR / "var" / "sku_sequence.txt"

        self.THEME_DEFAULT_CSS: Path = self.COMMON_STATIC / "css" / "presets" / "default.css"
        self.THEME_GENERATED_CSS: Path = self.COMMON_STATIC / "css" / "darkroom.css"

        self.ALLOWED_EXTENSIONS: Set[str] = {"jpg", "jpeg"}
        self.REQUIRED_LONG_EDGE_PX: int = 7200
        self.REQUIRED_DPI: int = 300
        self.THUMB_SIZE: tuple[int, int] = (500, 500)
        self.ANALYSE_LONG_EDGE: int = 2400

        self.SECRET_KEY: str = os.environ.get("FLASK_SECRET_KEY", "dev-secret")
        self.MAX_CONTENT_LENGTH: int = 250 * 1024 * 1024  # 250 MB cap

        self.ARTIST_NAME: str = os.environ.get("ARTLOMO_ARTIST_NAME", "")

        # Provider/model defaults (can be overridden by presets)
        self.DEFAULT_AI_PROVIDER: str = "openai"
        self.VISION_MODEL: str = "gpt-4o"

        self.OPENAI_DEFAULT_MODEL: str = os.getenv("OPENAI_DEFAULT_MODEL", os.getenv("OPENAI_MODEL", "gpt-4o"))
        self.OPENAI_MODEL_STACK: str = os.getenv("OPENAI_MODEL_STACK", "gpt-5.2,gpt-5.1,gpt-5,gpt-4o")
        self.OPENAI_API_TIMEOUT: float = _env_float("OPENAI_API_TIMEOUT", "60.0")
        self.OPENAI_API_RETRIES: int = _env_int("OPENAI_API_RETRIES", "1")
        self.OPENAI_IMAGE_MAX_MB: int = _env_int("OPENAI_IMAGE_MAX_MB", "20")
        self.ARTWORK_ANALYSIS_MAX_OUTPUT_TOKENS: int = _env_int("ARTWORK_ANALYSIS_MAX_OUTPUT_TOKENS", "2000")
        self.TEMPERATURE: float = _env_float("TEMPERATURE", "0.2")

        self.GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")
        self.GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self.GEMINI_MODEL_STACK: str = os.getenv("GEMINI_MODEL_STACK", "gemini-1.5-flash,gemini-1.5-pro")

        self._ensure_directories()

    def _ensure_directories(self) -> None:
        required = [
            self.COMMON_STATIC / "css",
            self.COMMON_STATIC / "js",
            self.LAB_UNPROCESSED_DIR,
            self.LAB_PROCESSED_DIR,
            self.LAB_LOCKED_DIR,
            self.LAB_INDEX_DIR,
            self.EXPORTS_DIR,
            self.THEMES_DIR,
        ]
        for path in required:
            path.mkdir(parents=True, exist_ok=True)


def get_config(base_dir: Path | str | None = None) -> AppConfig:
    return AppConfig(base_dir=base_dir)
