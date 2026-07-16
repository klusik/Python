"""Filesystem path helpers for settings, logs, and packaged resources."""

from __future__ import annotations

import os
from pathlib import Path

from .constants import APP_SLUG


def user_config_directory() -> Path:
    """Return the per-user configuration directory.

    On Windows the directory is placed below ``%APPDATA%``. A deterministic
    fallback below the user's home directory is used when ``APPDATA`` is absent,
    which also keeps unit tests and non-Windows development predictable.

    :return: Directory used for mutable application configuration.
    """

    appdata = os.environ.get("APPDATA")
    base = Path(appdata) if appdata else Path.home() / ".config"
    return base / APP_SLUG


def user_data_directory() -> Path:
    """Return the per-user local application-data directory.

    :return: Base directory for logs and the persistent WebView2 profile.
    """

    local_appdata = os.environ.get("LOCALAPPDATA")
    base = Path(local_appdata) if local_appdata else user_config_directory()
    return base / APP_SLUG if local_appdata else base


def user_webview_directory() -> Path:
    """Return the dedicated persistent WebView2 profile directory.

    :return: Directory used by pywebview for cookies and browser storage.
    """

    return user_data_directory() / "webview"


def user_log_directory() -> Path:
    """Return the per-user log directory.

    :return: Directory used for rotating application logs.
    """

    return user_data_directory() / "logs"
