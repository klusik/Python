"""Configuration helpers.

This module collects file-system paths that are shared across the program.
"""

import os
from pathlib import Path

from .constants import APP_ID, DEFAULT_OUTPUT_FILE_NAME, SETTINGS_FILE_NAME


def get_app_data_directory():
    """Return the directory used for persistent application data.

    The folder is created on demand inside the user's roaming AppData profile.
    """
    appdata_root = os.environ.get("APPDATA")
    if not appdata_root:
        appdata_root = str(Path.home())

    application_directory = Path(appdata_root) / APP_ID
    application_directory.mkdir(parents=True, exist_ok=True)
    return application_directory


def get_settings_file_path():
    """Return the full path to the JSON settings file."""
    return get_app_data_directory() / SETTINGS_FILE_NAME


def get_default_output_file_path():
    """Return the default path suggested for the captured ACARS text file."""
    return get_app_data_directory() / DEFAULT_OUTPUT_FILE_NAME
