"""Tests for the repository launcher bootstrap."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def _load_launcher() -> ModuleType:
    """Load the root launcher as an isolated module.

    :return: Imported launcher module.
    """

    launcher_path = Path(__file__).resolve().parents[1] / "run_elite_reader.py"
    specification = importlib.util.spec_from_file_location(
        "elite_reader_repository_launcher", launcher_path
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def test_launcher_adds_repository_src_directory() -> None:
    """The direct launcher must make the src-layout package importable."""

    launcher = _load_launcher()
    source_directory = str(Path(__file__).resolve().parents[1] / "src")
    original_path = list(sys.path)

    try:
        sys.path[:] = [entry for entry in sys.path if entry != source_directory]
        launcher._add_repository_src_to_import_path()
        assert sys.path[0] == source_directory

        launcher._add_repository_src_to_import_path()
        assert sys.path.count(source_directory) == 1
    finally:
        sys.path[:] = original_path
