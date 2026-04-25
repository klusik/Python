"""Startup error reporting that works before Tkinter is available."""

import os
import platform
import subprocess
import sys
from typing import List


class StartupError:
    """Displays critical startup errors without requiring Tkinter."""

    def show(self, title: str, message: str) -> None:
        """Show a platform-appropriate startup error message."""
        system_name: str = platform.system()

        if system_name == "Darwin":
            self._show_macos_dialog(title, message)
            return

        if system_name == "Windows":
            self._show_windows_dialog(title, message)
            return

        self._write_terminal_fallback(title, message)

    def _show_macos_dialog(self, title: str, message: str) -> None:
        """Display a native macOS dialog through AppleScript."""
        script: str = f'display dialog "{self._escape_applescript(message)}" with title "{self._escape_applescript(title)}" buttons {{"OK"}} default button "OK" with icon stop'
        command: List[str] = ["osascript", "-e", script]

        try:
            subprocess.run(command, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except OSError:
            self._write_terminal_fallback(title, message)

    def _show_windows_dialog(self, title: str, message: str) -> None:
        """Display a native Windows error dialog."""
        try:
            import ctypes

            ctypes.windll.user32.MessageBoxW(None, message, title, 0x10)
        except Exception:
            self._write_terminal_fallback(title, message)

    def _write_terminal_fallback(self, title: str, message: str) -> None:
        """Use stderr only when no graphical fallback is available."""
        print(f"{title}: {message}", file=sys.stderr)

    def _escape_applescript(self, value: str) -> str:
        """Escape text for a simple AppleScript string literal."""
        return value.replace("\\", "\\\\").replace('"', '\\"').replace(os.linesep, "\\n")
