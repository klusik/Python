"""Persistence for non-secret application settings."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .constants import (
    DEFAULT_REGISTERED_APPLICATION_NAME,
    SETTINGS_DIRECTORY_NAME,
    SETTINGS_FILENAME,
)
from .exceptions import ConfigurationError
from .models import ApplicationSettings


class ConfigurationRepository:
    """Load and save non-secret settings outside the source tree.

    @param settings_file: Optional explicit settings path used by tests or portable setups.
    """

    def __init__(self, settings_file: Path | None = None) -> None:
        self._settings_file = settings_file or self._determine_default_settings_file()

    @property
    def settings_file(self) -> Path:
        """Return the absolute settings-file path."""

        return self._settings_file

    def load(self, default_output_directory: Path) -> ApplicationSettings:
        """Load settings, falling back to safe defaults when no file exists.

        @param default_output_directory: Output directory used for first launch.
        @return: Loaded and validated non-secret settings.
        """

        if not self._settings_file.exists():
            return self._create_default_settings(default_output_directory)

        try:
            decoded_settings = json.loads(self._settings_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exception:
            raise ConfigurationError(
                f"Unable to read settings from {self._settings_file}: {exception}"
            ) from exception

        if not isinstance(decoded_settings, dict):
            raise ConfigurationError("The settings file must contain a JSON object.")

        return ApplicationSettings(
            registered_application_name=self._read_string(
                decoded_settings,
                "registered_application_name",
                DEFAULT_REGISTERED_APPLICATION_NAME,
            ),
            commander_name=self._read_string(decoded_settings, "commander_name", ""),
            commander_frontier_id=self._read_string(
                decoded_settings,
                "commander_frontier_id",
                "",
            ),
            output_directory=self._read_string(
                decoded_settings,
                "output_directory",
                str(default_output_directory),
            ),
            development_mode=bool(decoded_settings.get("development_mode", True)),
        )

    def save(self, application_settings: ApplicationSettings) -> None:
        """Atomically save non-secret settings.

        @param application_settings: Settings to persist. No API-key field exists.
        """

        serialized_settings = {
            "registered_application_name": application_settings.registered_application_name,
            "commander_name": application_settings.commander_name,
            "commander_frontier_id": application_settings.commander_frontier_id,
            "output_directory": application_settings.output_directory,
            "development_mode": application_settings.development_mode,
        }

        try:
            self._settings_file.parent.mkdir(parents=True, exist_ok=True)
            temporary_settings_file = self._settings_file.with_suffix(".tmp")
            temporary_settings_file.write_text(
                json.dumps(serialized_settings, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            temporary_settings_file.replace(self._settings_file)
        except OSError as exception:
            raise ConfigurationError(
                f"Unable to save settings to {self._settings_file}: {exception}"
            ) from exception

    @staticmethod
    def _determine_default_settings_file() -> Path:
        """Return the platform-appropriate application settings path."""

        if os.name == "nt":
            roaming_application_data = os.environ.get("APPDATA")
            if roaming_application_data:
                return (
                    Path(roaming_application_data)
                    / SETTINGS_DIRECTORY_NAME
                    / SETTINGS_FILENAME
                )

        return Path.home() / ".config" / SETTINGS_DIRECTORY_NAME / SETTINGS_FILENAME

    @staticmethod
    def _create_default_settings(default_output_directory: Path) -> ApplicationSettings:
        """Create first-launch settings without secrets."""

        return ApplicationSettings(
            registered_application_name=DEFAULT_REGISTERED_APPLICATION_NAME,
            commander_name="",
            commander_frontier_id="",
            output_directory=str(default_output_directory),
            development_mode=True,
        )

    @staticmethod
    def _read_string(
        decoded_settings: dict[str, Any],
        property_name: str,
        default_value: str,
    ) -> str:
        """Read one string setting and reject unrelated JSON value types.

        @param decoded_settings: Parsed settings object.
        @param property_name: Property to retrieve.
        @param default_value: Value used when the property is absent or invalid.
        @return: Normalized string value.
        """

        candidate_value = decoded_settings.get(property_name, default_value)
        return candidate_value if isinstance(candidate_value, str) else default_value
