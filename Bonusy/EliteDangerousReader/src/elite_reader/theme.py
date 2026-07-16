"""JavaScript resource loading and safe settings serialization."""

from __future__ import annotations

import json
from importlib.resources import files

from .config import ReaderSettings
from .constants import ALLOWED_BASE_DOMAIN, HOME_URL
from .version import __version__


def build_injection_script(settings: ReaderSettings) -> str:
    """Build the complete toolbar and readability injection script.

    ``window.run_js`` executes this script directly, avoiding ``eval`` and the
    related page Content Security Policy limitation documented by pywebview.

    :param settings: Validated settings to apply immediately.
    :return: JavaScript source suitable for direct execution.
    """

    template = (
        files("elite_reader").joinpath("assets/reader_injection.js").read_text(encoding="utf-8")
    )
    replacements = {
        "__INITIAL_SETTINGS_JSON__": _safe_json(settings.to_dict()),
        "__HOME_URL_JSON__": _safe_json(HOME_URL),
        "__ALLOWED_BASE_DOMAIN_JSON__": _safe_json(ALLOWED_BASE_DOMAIN),
        "__APP_VERSION_JSON__": _safe_json(__version__),
    }
    for marker, value in replacements.items():
        template = template.replace(marker, value)
    return template


def _safe_json(value: object) -> str:
    """Serialize data for insertion into JavaScript source.

    The substitutions protect against accidental script termination if future
    string settings contain HTML-sensitive characters.

    :param value: JSON-serializable value.
    :return: Compact JSON with HTML-significant characters escaped.
    """

    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )
