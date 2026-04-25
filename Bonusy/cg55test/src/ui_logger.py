"""Logger adapter that forwards yt-dlp messages into the application UI."""

from typing import Callable


class UiLogger:
    """Collects log messages from yt-dlp without writing to the console."""

    def __init__(self, emit: Callable[[str], None]) -> None:
        self._emit: Callable[[str], None] = emit

    def debug(self, message: str) -> None:
        """Handle verbose yt-dlp messages."""
        if message.strip():
            self._emit(message)

    def warning(self, message: str) -> None:
        """Handle yt-dlp warnings."""
        if message.strip():
            self._emit(f"Warning: {message}")

    def error(self, message: str) -> None:
        """Handle yt-dlp errors."""
        if message.strip():
            self._emit(f"Error: {message}")
