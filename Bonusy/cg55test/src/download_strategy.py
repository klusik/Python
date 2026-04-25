"""Single yt-dlp download strategy definition."""

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class DownloadStrategy:
    """Describes one attempt the downloader can make."""

    name: str
    description: str
    ytdlp_options: Dict[str, Any]
