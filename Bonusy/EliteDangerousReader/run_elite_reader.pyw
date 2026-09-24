"""Repository and PyInstaller launcher for Elite Dangerous Reader.

The project uses the conventional ``src`` package layout. This launcher adds the
repository's ``src`` directory to the import path when running directly from an
uninstalled checkout, while remaining compatible with editable installations and
PyInstaller.
"""

from __future__ import annotations

import sys
from pathlib import Path


def _add_repository_src_to_import_path() -> None:
    """Make the local package importable from an unpacked repository.

    The operation is idempotent and has no effect when the directory is already
    present, such as after an editable package installation.
    """

    source_directory = Path(__file__).resolve().parent / "src"
    source_directory_text = str(source_directory)
    if source_directory_text not in sys.path:
        sys.path.insert(0, source_directory_text)


def run() -> int:
    """Load and run the packaged application entry point.

    :return: Process exit code returned by the application.
    """

    _add_repository_src_to_import_path()
    from elite_reader.__main__ import main

    return main()


if __name__ == "__main__":
    sys.exit(run())
