"""Threaded worker used to keep the Tkinter interface responsive."""

import queue
import threading
from typing import Optional

from src.download_message import DownloadMessage
from src.download_options import DownloadOptions
from src.youtube_downloader import YoutubeDownloader


class DownloadWorker:
    """Runs a download on a background thread and reports status via a queue."""

    def __init__(self, options: DownloadOptions) -> None:
        self.options: DownloadOptions = options
        self.messages: "queue.Queue[DownloadMessage]" = queue.Queue()
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Start the background download thread."""
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def is_running(self) -> bool:
        """Return whether the worker thread is still active."""
        return self._thread is not None and self._thread.is_alive()

    def _run(self) -> None:
        """Perform the download and convert exceptions into UI messages."""
        downloader: YoutubeDownloader = YoutubeDownloader(self._emit)

        try:
            downloader.download(self.options)
        except Exception as exc:
            self._emit("error", str(exc), 0.0)

    def _emit(self, kind: str, text: str, progress: float) -> None:
        """Place one worker message on the thread-safe queue."""
        self.messages.put(DownloadMessage(kind=kind, text=text, progress=progress))
