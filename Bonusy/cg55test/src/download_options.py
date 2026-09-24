"""Download option model used by the UI and downloader."""

from dataclasses import dataclass


@dataclass
class DownloadOptions:
    """Options selected by the user before starting a download."""

    url: str
    output_directory: str
    audio_only: bool
