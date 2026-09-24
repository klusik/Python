"""Console-free Windows entry point for the Inara Profile Downloader."""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT_DIRECTORY = Path(__file__).resolve().parent
SOURCE_DIRECTORY = PROJECT_ROOT_DIRECTORY / "src"

if str(SOURCE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIRECTORY))

from inara_profile_downloader.gui import launch_application  # noqa: E402


if __name__ == "__main__":
    launch_application()
