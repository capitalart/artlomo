from pathlib import Path
import os


def base_dir() -> Path:
    override = os.environ.get("ARTLOMO_APP_BASE")
    return Path(override).resolve() if override else Path(__file__).resolve().parents[3]


def resolve_path(*parts: str) -> Path:
    return base_dir().joinpath(*parts)
