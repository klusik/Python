"""Tests for the restricted JavaScript bridge."""

import logging
from pathlib import Path

from elite_reader.api import ReaderApi
from elite_reader.config import ReaderSettings, SettingsStore


def test_api_saves_valid_settings(tmp_path: Path) -> None:
    """Valid visual settings are persisted and returned sanitized."""

    api = ReaderApi(SettingsStore(tmp_path / "settings.json"), logging.getLogger("test"))
    result = api.save_settings({"background_color": "#414141"})
    assert result["ok"] is True
    assert result["settings"]["background_color"] == "#414141"


def test_api_rejects_unknown_capability(tmp_path: Path) -> None:
    """Unexpected bridge fields are rejected rather than ignored."""

    api = ReaderApi(SettingsStore(tmp_path / "settings.json"), logging.getLogger("test"))
    result = api.save_settings({"open_file": "C:/secret.txt"})
    assert result["ok"] is False


class _FailingStore(SettingsStore):
    """Settings-store stub that simulates a write-permission failure."""

    def reset(self) -> ReaderSettings:
        """Raise the simulated filesystem error."""

        raise OSError("read-only profile")


def test_api_reports_reset_io_failure() -> None:
    """A settings write failure is returned to the toolbar as an error."""

    api = ReaderApi(_FailingStore(), logging.getLogger("test"))
    result = api.reset_settings()
    assert result["ok"] is False
    assert "read-only" in result["error"]
