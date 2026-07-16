"""Tests for JavaScript resource assembly."""

from elite_reader.config import ReaderSettings
from elite_reader.theme import build_injection_script


def test_injection_script_contains_serialized_settings() -> None:
    """Template markers are replaced with validated values."""

    script = build_injection_script(ReaderSettings(background_color="#424242", selector="main"))
    assert "__INITIAL_SETTINGS_JSON__" not in script
    assert '"background_color":"#424242"' in script
    assert '"selector":"main"' in script


def test_injection_script_contains_navigation_boundary() -> None:
    """The JavaScript link guard receives the approved base domain."""

    script = build_injection_script(ReaderSettings())
    assert '"elitedangerous.com"' in script
    assert "External navigation blocked" in script
