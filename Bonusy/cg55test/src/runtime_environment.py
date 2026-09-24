"""Runtime configuration for packaged PyInstaller builds."""

import os
import sys
from typing import List


def configure_runtime_environment() -> None:
    """Expose bundled helper binaries such as FFmpeg to child processes."""
    bundle_directory: str = _get_bundle_directory()
    path_parts: List[str] = [bundle_directory]
    existing_path: str = os.environ.get("PATH", "")

    if existing_path:
        path_parts.append(existing_path)

    os.environ["PATH"] = os.pathsep.join(path_parts)


def _get_bundle_directory() -> str:
    """Return PyInstaller's extraction folder or the project root in development."""
    bundle_directory: str = str(getattr(sys, "_MEIPASS", ""))

    if bundle_directory:
        return bundle_directory

    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
