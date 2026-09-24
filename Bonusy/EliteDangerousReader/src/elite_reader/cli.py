"""Command-line parsing for development and packaged execution."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from dataclasses import dataclass

from .constants import APP_NAME, HOME_URL
from .version import __version__


@dataclass(frozen=True, slots=True)
class CliArguments:
    """Parsed command-line options."""

    url: str
    debug: bool
    reset_settings: bool


def parse_arguments(argv: Sequence[str] | None = None) -> CliArguments:
    """Parse command-line options.

    :param argv: Optional argument sequence excluding the executable name.
    :return: Immutable parsed options.
    """

    parser = argparse.ArgumentParser(
        prog="elite-reader",
        description=(
            "Open the official Elite Dangerous website in a constrained WebView2 "
            "reader with configurable background and text styling."
        ),
    )
    parser.add_argument(
        "--url",
        default=HOME_URL,
        help="Initial HTTPS URL below elitedangerous.com.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable verbose logs and WebView2 developer tools.",
    )
    parser.add_argument(
        "--reset-settings",
        action="store_true",
        help="Reset visual settings before opening the reader.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{APP_NAME} {__version__}",
    )
    namespace = parser.parse_args(argv)
    return CliArguments(
        url=namespace.url,
        debug=bool(namespace.debug),
        reset_settings=bool(namespace.reset_settings),
    )
