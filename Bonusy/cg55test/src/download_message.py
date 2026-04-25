"""Typed progress message used between worker threads and the UI."""

from dataclasses import dataclass


@dataclass
class DownloadMessage:
    """Represents one status update emitted by the download worker."""

    kind: str
    text: str
    progress: float
