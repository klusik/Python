"""Persistent settings storage.

The application keeps only a few simple settings, so a small JSON file is
sufficient and easy to inspect manually if needed.
"""

import json
from copy import deepcopy

from .config import get_default_output_file_path, get_settings_file_path


class SettingsStore:
    """Load and save application settings."""

    def __init__(self):
        """Initialize the store with a fixed default schema."""
        self.settings_file_path = get_settings_file_path()
        self.default_settings = {
            "run_after_windows_start": False,
            "output_file_path": str(get_default_output_file_path()),
        }

    def load(self):
        """Return settings merged with defaults.

        If the file is missing or invalid, the defaults are returned instead.
        """
        if not self.settings_file_path.exists():
            return deepcopy(self.default_settings)

        try:
            with self.settings_file_path.open("r", encoding="utf-8") as settings_file:
                loaded_settings = json.load(settings_file)
        except (OSError, json.JSONDecodeError):
            return deepcopy(self.default_settings)

        merged_settings = deepcopy(self.default_settings)
        if isinstance(loaded_settings, dict):
            merged_settings.update(loaded_settings)
        return merged_settings

    def has_saved_settings(self):
        """Return True when a settings file already exists on disk."""
        return self.settings_file_path.exists()

    def save(self, settings):
        """Persist the provided settings dictionary to disk."""
        safe_settings = deepcopy(self.default_settings)
        if isinstance(settings, dict):
            safe_settings.update(settings)

        with self.settings_file_path.open("w", encoding="utf-8") as settings_file:
            json.dump(safe_settings, settings_file, indent=2, ensure_ascii=False)
