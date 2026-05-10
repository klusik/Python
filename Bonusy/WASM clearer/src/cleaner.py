"""Validated WASM cache deletion logic."""

from __future__ import annotations

import os
from pathlib import Path

from .models import CacheEntry, CleanResult
from .path_utils import canonical_path, has_reparse_point, is_relative_to, safe_iterdir

PROTECTED_CHILD_NAMES = {
    "work",
    "setting",
    "settings",
    "config",
    "configs",
    "configuration",
    "profile",
    "profiles",
    "state",
    "userdata",
    "user-data",
    "log",
    "logs",
}


def clean_entry(entry: CacheEntry) -> CleanResult:
    """Clear one product-level WASM cache entry after strict validation."""

    errors = _validate_entry(entry)
    if errors:
        return CleanResult(entry=entry, deleted_count=0, skipped_count=0, errors=tuple(errors))

    deleted_count = 0
    skipped: list[str] = []
    failures: list[str] = []
    target = canonical_path(entry.cache_path, strict=True)

    for child in tuple(safe_iterdir(target)):
        deleted_count += _remove_path_safely(child, target, skipped, failures)

    _remove_if_empty(target, failures)

    return CleanResult(
        entry=entry,
        deleted_count=deleted_count,
        skipped_count=len(skipped),
        errors=tuple(failures),
        skipped=tuple(skipped),
    )


def describe_clean_plan(entries: tuple[CacheEntry, ...]) -> str:
    """Return a human-readable cleanup summary for confirmation dialogs."""

    lines = [
        "The following selected WASM cache entries will be cleared.",
        "",
        "Likely settings/state folders are preserved: "
        + ", ".join(sorted(PROTECTED_CHILD_NAMES)),
        "",
    ]
    for entry in entries:
        lines.append(f"- {entry.display_name}")
        lines.append(f"  {entry.cache_path}")
    return "\n".join(lines)


def _validate_entry(entry: CacheEntry) -> list[str]:
    """Validate that the selected entry is still a safe cleanup target."""

    errors: list[str] = []
    target = canonical_path(entry.cache_path)
    approved_root = canonical_path(entry.approved_root)

    if not target.exists():
        errors.append(f"Cache path no longer exists: {target}")
        return errors
    if not target.is_dir():
        errors.append(f"Cache path is not a directory: {target}")
    if not approved_root.exists() or not approved_root.is_dir():
        errors.append(f"Approved WASM root is unavailable: {approved_root}")
    if approved_root.name.lower() != "wasm":
        errors.append(f"Approved root is not named WASM: {approved_root}")
    if target == approved_root:
        errors.append("Refusing to clear the WASM root itself.")
    if not is_relative_to(target, approved_root):
        errors.append(f"Cache path is outside the approved WASM root: {target}")
    if has_reparse_point(target):
        errors.append(f"Refusing reparse-point target: {target}")
    if _relative_depth(target, approved_root) not in (1, 2):
        errors.append(f"Refusing ambiguous target depth below WASM root: {target}")

    return errors


def _relative_depth(child: Path, parent: Path) -> int:
    """Return the number of path components between child and parent."""

    try:
        return len(canonical_path(child).relative_to(canonical_path(parent)).parts)
    except ValueError:
        return -1


def _should_preserve_child(path: Path) -> bool:
    """Return True for folders that look like settings or state, not cache."""

    return path.name.strip().lower() in PROTECTED_CHILD_NAMES


def _remove_path_safely(path: Path, selected_root: Path, skipped: list[str], failures: list[str]) -> int:
    """Delete one path if it is still inside the selected cache tree."""

    if _should_preserve_child(path):
        skipped.append(str(path))
        return 0
    if has_reparse_point(path):
        skipped.append(f"{path} (reparse point)")
        return 0
    if not is_relative_to(path, selected_root):
        failures.append(f"Rejected path outside selected cache folder: {path}")
        return 0

    if path.is_dir():
        # Recurse into nested folders so protected names are still respected.
        deleted = 0
        for child in tuple(safe_iterdir(path)):
            deleted += _remove_path_safely(child, selected_root, skipped, failures)
        try:
            if not any(path.iterdir()):
                path.rmdir()
                deleted += 1
        except OSError as exc:
            failures.append(f"{path}: {exc}")
        return deleted

    try:
        path.unlink()
        return 1
    except OSError as exc:
        failures.append(f"{path}: {exc}")
        return 0


def _remove_if_empty(path: Path, failures: list[str]) -> None:
    """Remove the top-level cache folder if the cleanup left it empty."""

    try:
        if not any(path.iterdir()):
            os.rmdir(path)
    except OSError as exc:
        failures.append(f"Could not remove empty cache folder {path}: {exc}")
