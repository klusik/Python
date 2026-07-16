"""User-visible fatal error reporting for windowed builds."""

from __future__ import annotations

import ctypes
import sys

from .constants import APP_NAME


def show_fatal_error(message: str) -> None:
    """Display a native Windows error dialog, with a stderr fallback.

    PyInstaller windowed applications have no console, so logging alone can make
    startup failures appear as if nothing happened.

    :param message: Human-readable failure description.
    """

    text = str(message).strip() or "The application could not start."
    try:
        windll = getattr(ctypes, "windll", None)
        user32 = getattr(windll, "user32", None)
        if user32 is None:
            raise AttributeError("Windows user32 API is unavailable")
        user32.MessageBoxW(None, text, APP_NAME, 0x10)
    except (AttributeError, OSError):
        print(f"{APP_NAME}: {text}", file=sys.stderr)
