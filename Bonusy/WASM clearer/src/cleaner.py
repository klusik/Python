"""Validated WASM cache deletion logic."""

import os
from pathlib import Path

from .models import CacheEntry, CacheEntryDetails, CacheFileDetail, CleanPlan, CleanPlanItem, CleanResult
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
MAX_DETAIL_ROWS = 10_000


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


def build_clean_plan(entries: tuple[CacheEntry, ...]) -> CleanPlan:
    """Inspect selected entries without changing them and return cleanup totals."""

    items: list[CleanPlanItem] = []
    all_warnings: list[str] = []
    for entry in entries:
        validation_errors = _validate_entry(entry)
        if validation_errors:
            all_warnings.extend(validation_errors)
            items.append(CleanPlanItem(entry, 0, 0, 0, 0, len(validation_errors)))
            continue

        counters = {"files": 0, "directories": 0, "bytes": 0, "preserved": 0}
        warnings: list[str] = []
        target = canonical_path(entry.cache_path, strict=True)
        for child in tuple(safe_iterdir(target)):
            _inspect_path(child, target, counters, warnings)
        all_warnings.extend(warnings)
        items.append(
            CleanPlanItem(
                entry=entry,
                file_count=counters["files"],
                directory_count=counters["directories"],
                byte_count=counters["bytes"],
                preserved_count=counters["preserved"],
                warning_count=len(warnings),
            )
        )
    return CleanPlan(items=tuple(items), warnings=tuple(all_warnings))


def inspect_entry_details(entry: CacheEntry) -> CacheEntryDetails:
    """Return a bounded file listing using the cleanup policy without mutation."""

    validation_errors = _validate_entry(entry)
    if validation_errors:
        return CacheEntryDetails(entry=entry, files=(), warnings=tuple(validation_errors))

    target = canonical_path(entry.cache_path, strict=True)
    details: list[CacheFileDetail] = []
    warnings: list[str] = []
    truncated = [False]
    for child in tuple(safe_iterdir(target)):
        _collect_path_details(child, target, details, warnings, truncated)
        if truncated[0]:
            break
    return CacheEntryDetails(entry, tuple(details), tuple(warnings), truncated[0])


def _collect_path_details(
    path: Path,
    selected_root: Path,
    details: list[CacheFileDetail],
    warnings: list[str],
    truncated: list[bool],
) -> None:
    """Collect safe, display-only metadata up to the detail-row limit."""

    if len(details) >= MAX_DETAIL_ROWS:
        truncated[0] = True
        return

    relative_path = str(path.relative_to(selected_root))
    if _should_preserve_child(path):
        details.append(CacheFileDetail(relative_path, 0, _modified_time(path), "Protected folder", "Preserved"))
        return
    if has_reparse_point(path):
        details.append(CacheFileDetail(relative_path, 0, _modified_time(path), "Reparse point", "Preserved"))
        return
    if not is_relative_to(path, selected_root):
        warnings.append(f"Rejected path outside selected cache folder: {path}")
        return

    try:
        if path.is_dir():
            for child in tuple(path.iterdir()):
                _collect_path_details(child, selected_root, details, warnings, truncated)
                if truncated[0]:
                    return
            return

        stat_result = path.stat()
        details.append(
            CacheFileDetail(
                relative_path=relative_path,
                byte_count=stat_result.st_size,
                modified_time=stat_result.st_mtime,
                kind=_describe_file(path),
                disposition="Will clear",
            )
        )
    except OSError as exc:
        warnings.append(f"Could not inspect {path}: {exc}")


def _modified_time(path: Path) -> float | None:
    """Return a modification timestamp without allowing metadata failure to abort inspection."""

    try:
        return path.stat().st_mtime
    except OSError:
        return None


def _describe_file(path: Path) -> str:
    """Describe a file using extension and a bounded WebAssembly signature check."""

    try:
        with path.open("rb") as file_handle:
            header = file_handle.read(8)
        if header[:4] == b"\x00asm":
            version = int.from_bytes(header[4:8], "little") if len(header) == 8 else None
            return f"WebAssembly module v{version}" if version is not None else "WebAssembly module"
    except OSError:
        pass

    extension = path.suffix.lower().lstrip(".")
    return f"{extension.upper()} file" if extension else "File"


def _inspect_path(
    path: Path,
    selected_root: Path,
    counters: dict[str, int],
    warnings: list[str],
) -> None:
    """Collect the same path categories used by deletion, without mutation."""

    if _should_preserve_child(path) or has_reparse_point(path):
        counters["preserved"] += 1
        return
    if not is_relative_to(path, selected_root):
        warnings.append(f"Rejected path outside selected cache folder: {path}")
        return
    try:
        if path.is_dir():
            counters["directories"] += 1
            for child in tuple(path.iterdir()):
                _inspect_path(child, selected_root, counters, warnings)
        else:
            counters["files"] += 1
            counters["bytes"] += path.stat().st_size
    except OSError as exc:
        warnings.append(f"Could not inspect {path}: {exc}")


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
