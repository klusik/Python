"""
config.py

Central configuration and paths.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


def _project_root() -> str:
    """Return absolute path to the project root."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@dataclass(frozen=True)
class Config:
    """Application configuration constants."""

    APP_TITLE: str = "DnD Session HUD"
    DEFAULT_GEOMETRY: str = "1200x720"

    # Paths
    ROOT_DIR: str = _project_root()
    SRC_DIR: str = os.path.join(_project_root(), "src")
    IMG_DIR: str = os.path.join(_project_root(), "img")
    SAVEGAMES_DIR: str = os.path.join(_project_root(), "savegames")

    # API key storage
    STORE_API_KEY_FILENAME: str = ".openai_api_key.txt"

    # Inventory constraints
    DEFAULT_MAX_CARRY_KG: float = 30.0

    # UI constants
    HUD_HEIGHT_PX: int = 44
    LEFT_PANEL_MIN_WIDTH: int = 280
    RIGHT_PANEL_MIN_WIDTH: int = 320
    CENTER_PANEL_MIN_WIDTH: int = 500

    # Command behavior
    COMMAND_PREFIX: str = ""  # keep empty: user types "pick sword", not "/pick sword"


def ensure_directories() -> None:
    """Create required directories if missing."""
    os.makedirs(Config.SAVEGAMES_DIR, exist_ok=True)
    os.makedirs(Config.IMG_DIR, exist_ok=True)