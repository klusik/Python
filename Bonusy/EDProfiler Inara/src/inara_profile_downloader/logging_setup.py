"""Rotating application logging configured outside the repository."""

from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

from .constants import (
    LOG_BACKUP_COUNT,
    LOG_DIRECTORY_NAME,
    LOG_FILENAME,
    LOG_MAX_BYTES,
    SETTINGS_DIRECTORY_NAME,
)


def configure_application_logging() -> tuple[logging.Logger, Path]:
    """Configure and return the package logger and its log-file path.

    @return: Tuple containing the configured logger and log-file path.
    """

    log_file = _determine_log_file()
    log_file.parent.mkdir(parents=True, exist_ok=True)

    application_logger = logging.getLogger("inara_profile_downloader")
    application_logger.setLevel(logging.INFO)
    application_logger.propagate = False

    if not application_logger.handlers:
        rotating_handler = RotatingFileHandler(
            log_file,
            maxBytes=LOG_MAX_BYTES,
            backupCount=LOG_BACKUP_COUNT,
            encoding="utf-8",
        )
        rotating_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        application_logger.addHandler(rotating_handler)

    return application_logger, log_file


def _determine_log_file() -> Path:
    """Return a platform-appropriate rotating log path."""

    if os.name == "nt":
        local_application_data = os.environ.get("LOCALAPPDATA")
        if local_application_data:
            return (
                Path(local_application_data)
                / SETTINGS_DIRECTORY_NAME
                / LOG_DIRECTORY_NAME
                / LOG_FILENAME
            )

    return (
        Path.home()
        / ".local"
        / "state"
        / SETTINGS_DIRECTORY_NAME
        / LOG_DIRECTORY_NAME
        / LOG_FILENAME
    )
