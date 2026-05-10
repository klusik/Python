"""Path utilities with Windows-focused safety helpers."""

from __future__ import annotations

import os
import stat
from pathlib import Path
from typing import Iterable, Iterator


def expanded_path(value: str | Path) -> Path:
    """Expand environment variables and user markers without requiring the path to exist."""

    return Path(os.path.expandvars(str(value))).expanduser()


def canonical_path(path: str | Path, *, strict: bool = False) -> Path:
    """Return a normalized absolute path, resolving links when possible."""

    expanded = expanded_path(path)
    try:
        return expanded.resolve(strict=strict)
    except OSError:
        return expanded.absolute()


def is_relative_to(child: Path, parent: Path) -> bool:
    """Return whether child is contained by parent after canonicalization."""

    child_canon = canonical_path(child)
    parent_canon = canonical_path(parent)
    try:
        child_canon.relative_to(parent_canon)
        return True
    except ValueError:
        return False


def has_reparse_point(path: Path) -> bool:
    """Return True for symlinks, junctions, and other Windows reparse points."""

    try:
        if path.is_symlink():
            return True
        attributes = getattr(os.lstat(path), "st_file_attributes", 0)
        return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))
    except OSError:
        return False


def safe_iterdir(path: Path) -> Iterator[Path]:
    """Yield directory children, returning nothing on common filesystem failures."""

    try:
        yield from path.iterdir()
    except (FileNotFoundError, NotADirectoryError, PermissionError, OSError):
        return


def existing_directories(paths: Iterable[Path]) -> tuple[Path, ...]:
    """Return existing directories after deduplication by canonical path."""

    seen: set[str] = set()
    result: list[Path] = []
    for path in paths:
        canon = canonical_path(path)
        key = os.path.normcase(str(canon))
        if key in seen:
            continue
        seen.add(key)
        if canon.is_dir():
            result.append(canon)
    return tuple(result)


def format_path(path: Path | None) -> str:
    """Return a string path for UI display."""

    return "" if path is None else str(path)
