"""Upload workflow specific configuration helpers."""
from ..config import AppConfig


def get_upload_config() -> AppConfig:
    return AppConfig()
