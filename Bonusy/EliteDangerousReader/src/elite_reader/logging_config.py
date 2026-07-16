"""Application logging configuration."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from .constants import LOG_BACKUP_COUNT, LOG_FILE_NAME, MAX_LOG_BYTES
from .paths import user_log_directory


def configure_logging(*, debug: bool = False) -> logging.Logger:
    """Configure rotating file and console logging.

    Repeated calls are idempotent and return the existing application logger.

    :param debug: Enable verbose diagnostic output.
    :return: Configured application logger.
    """

    logger = logging.getLogger("elite_reader")
    if logger.handlers:
        return logger

    level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    try:
        log_directory = user_log_directory()
        log_directory.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_directory / LOG_FILE_NAME,
            maxBytes=MAX_LOG_BYTES,
            backupCount=LOG_BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except OSError as exc:
        logger.warning("File logging is unavailable: %s", exc)

    logger.propagate = False
    return logger
