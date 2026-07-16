"""Tests for settings validation and persistence."""

import json
from pathlib import Path

from elite_reader.config import (
    ReaderSettings,
    SettingsStore,
    SettingsValidationError,
)


def test_default_settings_are_valid() -> None:
    """Defaults must round-trip through the untrusted mapping validator."""

    defaults = ReaderSettings()
    assert ReaderSettings.from_mapping(defaults.to_dict()) == defaults


def test_colors_are_normalized() -> None:
    """Hex colors are normalized to lowercase."""

    settings = ReaderSettings.from_mapping({"background_color": "#AABBCC"})
    assert settings.background_color == "#aabbcc"


def test_invalid_color_is_rejected() -> None:
    """Malformed CSS color input never reaches the injection script."""

    try:
        ReaderSettings.from_mapping({"background_color": "red"})
    except SettingsValidationError:
        return
    raise AssertionError("Expected SettingsValidationError")


def test_unknown_fields_are_rejected() -> None:
    """The JavaScript bridge cannot smuggle additional capabilities."""

    try:
        ReaderSettings.from_mapping({"run_command": "calc.exe"})
    except SettingsValidationError:
        return
    raise AssertionError("Expected SettingsValidationError")


def test_store_round_trip(tmp_path: Path) -> None:
    """Settings are written and loaded without loss."""

    path = tmp_path / "settings.json"
    store = SettingsStore(path)
    expected = ReaderSettings(background_color="#404040", selector="main")
    store.save(expected)
    assert store.load() == expected
    assert json.loads(path.read_text(encoding="utf-8"))["selector"] == "main"


def test_invalid_file_is_recovered(tmp_path: Path) -> None:
    """Broken JSON is preserved and defaults are returned."""

    path = tmp_path / "settings.json"
    path.write_text("{broken", encoding="utf-8")
    store = SettingsStore(path)
    assert store.load() == ReaderSettings()
    assert path.with_suffix(".json.invalid").exists()
