"""Narrow Python API exposed to the approved website."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from .config import ReaderSettings, SettingsStore, SettingsValidationError
from .constants import APP_NAME, HOME_URL
from .version import __version__


class ReaderApi:
    """Validated settings API available as ``window.pywebview.api``.

    No method exposes a general filesystem operation, command execution,
    clipboard access, arbitrary URL opening, or generic Python evaluation.
    """

    def __init__(self, store: SettingsStore, logger: logging.Logger) -> None:
        """Initialize the bridge.

        :param store: Persistent validated settings store.
        :param logger: Application logger.
        """

        self._store = store
        self._logger = logger

    def get_settings(self) -> dict[str, Any]:
        """Return current validated settings to the injected toolbar.

        :return: JSON-serializable settings dictionary.
        """

        return self._store.load().to_dict()

    def save_settings(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        """Validate and persist settings submitted by the toolbar.

        :param payload: Untrusted settings mapping from JavaScript.
        :return: Structured result containing sanitized settings or an error.
        """

        try:
            settings = ReaderSettings.from_mapping(payload)
            self._store.save(settings)
            self._logger.info("Reader settings updated")
            return {"ok": True, "settings": settings.to_dict()}
        except (SettingsValidationError, TypeError, ValueError, OSError) as exc:
            self._logger.warning("Rejected settings update: %s", exc)
            return {"ok": False, "error": str(exc)}

    def reset_settings(self) -> dict[str, Any]:
        """Restore and return default settings.

        :return: Structured result containing default settings.
        """

        try:
            settings = self._store.reset()
            self._logger.info("Reader settings reset")
            return {"ok": True, "settings": settings.to_dict()}
        except OSError as exc:
            self._logger.warning("Could not reset settings: %s", exc)
            return {"ok": False, "error": str(exc)}

    def get_app_info(self) -> dict[str, str]:
        """Return non-sensitive application metadata.

        :return: Application name, version, and home URL.
        """

        return {
            "name": APP_NAME,
            "version": __version__,
            "home_url": HOME_URL,
        }
