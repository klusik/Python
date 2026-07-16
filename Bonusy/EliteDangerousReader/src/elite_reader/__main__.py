"""Executable module for ``python -m elite_reader`` and PyInstaller."""

from __future__ import annotations

import sys
from collections.abc import Sequence

from .app import EliteReaderApplication
from .cli import parse_arguments
from .config import SettingsStore
from .constants import LOG_FILE_NAME
from .errors import show_fatal_error
from .logging_config import configure_logging
from .paths import user_log_directory


def main(argv: Sequence[str] | None = None) -> int:
    """Run the desktop reader.

    :param argv: Optional arguments excluding the executable name.
    :return: Process exit code.
    """

    arguments = parse_arguments(argv)
    logger = configure_logging(debug=arguments.debug)
    store = SettingsStore()

    try:
        if arguments.reset_settings:
            store.reset()
            logger.info("Settings reset by command-line request")

        application = EliteReaderApplication(
            start_url=arguments.url,
            debug=arguments.debug,
            store=store,
            logger=logger,
        )
        application.run()
        return 0
    except Exception as exc:
        logger.exception("Fatal application error")
        log_path = user_log_directory() / LOG_FILE_NAME
        show_fatal_error(f"{exc}\n\nDiagnostic log: {log_path}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
