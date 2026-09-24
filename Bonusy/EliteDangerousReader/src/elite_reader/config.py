"""Validated application settings and atomic JSON persistence."""

from __future__ import annotations

import json
import re
import threading
from collections.abc import Mapping
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any

from .constants import (
    MAX_FONT_SCALE_PERCENT,
    MAX_LINE_HEIGHT,
    MAX_SELECTOR_LENGTH,
    MIN_FONT_SCALE_PERCENT,
    MIN_LINE_HEIGHT,
    SETTINGS_FILE_NAME,
)
from .paths import user_config_directory

_HEX_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


class SettingsValidationError(ValueError):
    """Raised when settings contain unsupported or unsafe values."""


@dataclass(frozen=True, slots=True)
class ReaderSettings:
    """Readability settings applied to approved pages.

    The values are intentionally limited to visual customization. The website
    cannot use the Python bridge to access arbitrary files, execute commands, or
    call unrestricted operating-system APIs.
    """

    background_color: str = "#30343a"
    text_color: str = ""
    selector: str = "body"
    remove_background_image: bool = True
    include_descendants_for_text: bool = False
    font_scale_percent: int = 100
    line_height: float = 1.55
    panel_collapsed: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable settings dictionary.

        :return: Shallow dictionary containing all persisted fields.
        """

        return asdict(self)

    @classmethod
    def from_mapping(
        cls,
        raw: Mapping[str, Any] | None,
        *,
        merge_with_defaults: bool = True,
    ) -> ReaderSettings:
        """Validate and construct settings from an arbitrary mapping.

        :param raw: Untrusted mapping, commonly loaded from JSON or received from
            the JavaScript bridge.
        :param merge_with_defaults: Fill omitted fields with defaults when true.
        :return: A fully validated immutable settings object.
        :raises SettingsValidationError: If a supplied value is invalid.
        """

        raw = raw or {}
        allowed_names = {field.name for field in fields(cls)}
        unknown = set(raw) - allowed_names
        if unknown:
            raise SettingsValidationError(
                f"Unsupported settings fields: {', '.join(sorted(unknown))}"
            )

        values: dict[str, Any] = cls().to_dict() if merge_with_defaults else {}
        values.update(raw)

        background_color = _validate_color(
            values.get("background_color"),
            field_name="background_color",
            allow_empty=False,
        )
        text_color = _validate_color(
            values.get("text_color", ""),
            field_name="text_color",
            allow_empty=True,
        )

        selector = str(values.get("selector", "")).strip()
        if not selector:
            raise SettingsValidationError("selector must not be empty")
        if len(selector) > MAX_SELECTOR_LENGTH:
            raise SettingsValidationError(
                f"selector must be at most {MAX_SELECTOR_LENGTH} characters"
            )
        if any(character in selector for character in ("\x00", "\r", "\n")):
            raise SettingsValidationError("selector contains unsupported characters")

        font_scale_percent = _validate_int_range(
            values.get("font_scale_percent"),
            field_name="font_scale_percent",
            minimum=MIN_FONT_SCALE_PERCENT,
            maximum=MAX_FONT_SCALE_PERCENT,
        )
        line_height = _validate_float_range(
            values.get("line_height"),
            field_name="line_height",
            minimum=MIN_LINE_HEIGHT,
            maximum=MAX_LINE_HEIGHT,
        )

        return cls(
            background_color=background_color,
            text_color=text_color,
            selector=selector,
            remove_background_image=_validate_bool(
                values.get("remove_background_image"),
                "remove_background_image",
            ),
            include_descendants_for_text=_validate_bool(
                values.get("include_descendants_for_text"),
                "include_descendants_for_text",
            ),
            font_scale_percent=font_scale_percent,
            line_height=line_height,
            panel_collapsed=_validate_bool(
                values.get("panel_collapsed"),
                "panel_collapsed",
            ),
        )


def _validate_color(value: Any, *, field_name: str, allow_empty: bool) -> str:
    """Validate a six-digit hexadecimal color value.

    :param value: Candidate color.
    :param field_name: Name used in validation errors.
    :param allow_empty: Permit an empty string to disable the override.
    :return: Normalized lowercase color.
    :raises SettingsValidationError: If the color is malformed.
    """

    normalized = str(value or "").strip().lower()
    if allow_empty and not normalized:
        return ""
    if not _HEX_COLOR_RE.fullmatch(normalized):
        raise SettingsValidationError(f"{field_name} must use #RRGGBB hexadecimal notation")
    return normalized


def _validate_bool(value: Any, field_name: str) -> bool:
    """Validate a strict boolean value.

    :param value: Candidate value.
    :param field_name: Name used in validation errors.
    :return: The validated boolean.
    :raises SettingsValidationError: If the value is not a boolean.
    """

    if not isinstance(value, bool):
        raise SettingsValidationError(f"{field_name} must be true or false")
    return value


def _validate_int_range(
    value: Any,
    *,
    field_name: str,
    minimum: int,
    maximum: int,
) -> int:
    """Validate an integer within an inclusive range.

    :param value: Candidate value.
    :param field_name: Name used in validation errors.
    :param minimum: Inclusive lower bound.
    :param maximum: Inclusive upper bound.
    :return: Validated integer.
    :raises SettingsValidationError: If conversion or range validation fails.
    """

    if isinstance(value, bool):
        raise SettingsValidationError(f"{field_name} must be an integer")
    try:
        converted = int(value)
    except (TypeError, ValueError) as exc:
        raise SettingsValidationError(f"{field_name} must be an integer") from exc
    if converted < minimum or converted > maximum:
        raise SettingsValidationError(f"{field_name} must be between {minimum} and {maximum}")
    return converted


def _validate_float_range(
    value: Any,
    *,
    field_name: str,
    minimum: float,
    maximum: float,
) -> float:
    """Validate a floating-point number within an inclusive range.

    :param value: Candidate value.
    :param field_name: Name used in validation errors.
    :param minimum: Inclusive lower bound.
    :param maximum: Inclusive upper bound.
    :return: Validated float rounded to two decimal places.
    :raises SettingsValidationError: If conversion or range validation fails.
    """

    if isinstance(value, bool):
        raise SettingsValidationError(f"{field_name} must be a number")
    try:
        converted = float(value)
    except (TypeError, ValueError) as exc:
        raise SettingsValidationError(f"{field_name} must be a number") from exc
    if converted < minimum or converted > maximum:
        raise SettingsValidationError(f"{field_name} must be between {minimum} and {maximum}")
    return round(converted, 2)


class SettingsStore:
    """Thread-safe JSON settings store using atomic file replacement."""

    def __init__(self, path: Path | None = None) -> None:
        """Initialize the store.

        :param path: Optional explicit settings path, primarily for tests.
        """

        self.path = path or user_config_directory() / SETTINGS_FILE_NAME
        self._lock = threading.RLock()

    def load(self) -> ReaderSettings:
        """Load settings, recovering safely from missing or invalid files.

        Invalid files are preserved with a ``.invalid`` suffix when possible so
        that a developer can inspect them. Defaults are returned afterward.

        :return: Validated settings or defaults.
        """

        with self._lock:
            if not self.path.exists():
                return ReaderSettings()

            try:
                payload = json.loads(self.path.read_text(encoding="utf-8"))
                if not isinstance(payload, dict):
                    raise SettingsValidationError("settings root must be an object")
                return ReaderSettings.from_mapping(payload)
            except (OSError, json.JSONDecodeError, SettingsValidationError):
                self._preserve_invalid_file()
                return ReaderSettings()

    def save(self, settings: ReaderSettings) -> None:
        """Persist settings atomically.

        :param settings: Validated settings object to store.
        """

        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            temporary_path = self.path.with_suffix(self.path.suffix + ".tmp")
            serialized = json.dumps(
                settings.to_dict(),
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
            )
            temporary_path.write_text(serialized + "\n", encoding="utf-8")
            temporary_path.replace(self.path)

    def reset(self) -> ReaderSettings:
        """Replace current settings with defaults.

        :return: The persisted default settings.
        """

        settings = ReaderSettings()
        self.save(settings)
        return settings

    def _preserve_invalid_file(self) -> None:
        """Move an invalid settings file aside on a best-effort basis."""

        try:
            invalid_path = self.path.with_suffix(self.path.suffix + ".invalid")
            if invalid_path.exists():
                invalid_path.unlink()
            self.path.replace(invalid_path)
        except OSError:
            return
