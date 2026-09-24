"""Download orchestration built around yt-dlp fallback strategies."""

import os
from typing import Any, Callable, Dict, List

from src.download_options import DownloadOptions
from src.download_strategy import DownloadStrategy
from src.ui_logger import UiLogger


class YoutubeDownloader:
    """Attempts to download a video using multiple yt-dlp configurations."""

    def __init__(self, status_callback: Callable[[str, str, float], None]) -> None:
        self._status_callback: Callable[[str, str, float], None] = status_callback

    def download(self, options: DownloadOptions) -> None:
        """Download the requested URL, trying strategies until one succeeds."""
        strategies: List[DownloadStrategy] = self._build_strategies(options.audio_only)
        last_error: str = "No download strategy was attempted."

        for index, strategy in enumerate(strategies, start=1):
            self._emit(
                "status",
                f"Trying method {index}/{len(strategies)}: {strategy.description}",
                0.0,
            )

            try:
                self._run_strategy(strategy, options)
                self._emit("complete", f"Download complete using {strategy.name}.", 100.0)
                return
            except Exception as exc:
                last_error = str(exc)
                self._emit("status", f"{strategy.name} failed: {last_error}", 0.0)

        raise RuntimeError(f"All download methods failed. Last error: {last_error}")

    def _run_strategy(self, strategy: DownloadStrategy, options: DownloadOptions) -> None:
        """Execute one concrete yt-dlp strategy."""
        try:
            from yt_dlp import YoutubeDL
        except ImportError as exc:
            raise RuntimeError("Missing dependency: install requirements.txt before downloading.") from exc

        output_template: str = os.path.join(
            options.output_directory,
            "%(title).180B [%(id)s].%(ext)s",
        )
        ytdlp_options: Dict[str, Any] = dict(strategy.ytdlp_options)
        ytdlp_options.update(
            {
                "logger": UiLogger(self._emit_log),
                "noprogress": True,
                "outtmpl": output_template,
                "progress_hooks": [self._handle_progress],
                "quiet": True,
                "restrictfilenames": False,
            }
        )

        with YoutubeDL(ytdlp_options) as ydl:
            ydl.download([options.url])

    def _build_strategies(self, audio_only: bool) -> List[DownloadStrategy]:
        """Create fallback methods for video or audio downloads."""
        if audio_only:
            return [
                DownloadStrategy(
                    "Best audio",
                    "best available audio with metadata",
                    {
                        "format": "bestaudio/best",
                        "postprocessors": [
                            {
                                "key": "FFmpegExtractAudio",
                                "preferredcodec": "mp3",
                                "preferredquality": "192",
                            }
                        ],
                    },
                ),
                DownloadStrategy(
                    "Raw audio",
                    "best audio without conversion",
                    {"format": "bestaudio/best"},
                ),
                DownloadStrategy(
                    "Generic fallback",
                    "best generic media stream",
                    {"format": "best"},
                ),
            ]

        return [
            DownloadStrategy(
                "Best video and audio",
                "best video plus best audio merged when possible",
                {"format": "bv*+ba/best"},
            ),
            DownloadStrategy(
                "MP4-compatible",
                "best MP4 video and audio combination",
                {"format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best"},
            ),
            DownloadStrategy(
                "Single file fallback",
                "best single-file stream",
                {"format": "best"},
            ),
            DownloadStrategy(
                "Worst acceptable fallback",
                "smallest available stream if better formats fail",
                {"format": "worst"},
            ),
        ]

    def _handle_progress(self, data: Dict[str, Any]) -> None:
        """Translate yt-dlp progress dictionaries into UI messages."""
        status: str = str(data.get("status", ""))

        if status == "downloading":
            percent: float = self._calculate_percent(data)
            speed: str = str(data.get("_speed_str", "")).strip()
            eta: str = str(data.get("_eta_str", "")).strip()
            message_parts: List[str] = [f"Downloading: {percent:.1f}%"]

            if speed:
                message_parts.append(f"speed {speed}")
            if eta:
                message_parts.append(f"ETA {eta}")

            self._emit("progress", " | ".join(message_parts), percent)
        elif status == "finished":
            self._emit("status", "Download finished, processing file if needed.", 100.0)

    def _calculate_percent(self, data: Dict[str, Any]) -> float:
        """Calculate progress percentage from yt-dlp progress data."""
        downloaded: float = float(data.get("downloaded_bytes") or 0)
        total: float = float(data.get("total_bytes") or data.get("total_bytes_estimate") or 0)

        if total <= 0:
            return 0.0

        return max(0.0, min(100.0, downloaded / total * 100.0))

    def _emit_log(self, message: str) -> None:
        """Forward backend log messages to the UI."""
        self._emit("log", message, 0.0)

    def _emit(self, kind: str, text: str, progress: float) -> None:
        """Send a status event to the caller."""
        self._status_callback(kind, text, progress)
