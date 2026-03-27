"""Admin Hub configuration bridge."""
from ...config import AppConfig


def get_hub_config() -> AppConfig:
    return AppConfig()
