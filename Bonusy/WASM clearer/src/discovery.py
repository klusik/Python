"""Discover selectable product folders under approved WASM roots."""

from __future__ import annotations

import os
from pathlib import Path

from .detection import detect_simulator_locations
from .models import CacheEntry, ScanResult, SimulatorLocation
from .path_utils import canonical_path, has_reparse_point, safe_iterdir

SIM_BUCKET_NAMES = {
    "msfs2020",
    "msfs2024",
    "microsoftflightsimulator",
    "microsoftflightsimulator2024",
}


def scan_wasm_caches() -> ScanResult:
    """Detect simulator locations and return all eligible WASM cache entries."""

    warnings: list[str] = []
    locations = detect_simulator_locations()
    entries: list[CacheEntry] = []

    for location in locations:
        for root in location.wasm_roots:
            if not root.exists():
                continue
            if has_reparse_point(root):
                warnings.append(f"Skipped reparse-point WASM root: {root}")
                continue
            entries.extend(_entries_for_root(location, root, warnings))

    deduped_entries = _dedupe_entries(entries)
    return ScanResult(
        locations=tuple(sorted(locations, key=lambda item: item.display_name.lower())),
        entries=tuple(sorted(deduped_entries, key=lambda item: (item.product_name.lower(), str(item.cache_path).lower()))),
        warnings=tuple(warnings),
    )


def _entries_for_root(location: SimulatorLocation, root: Path, warnings: list[str]) -> list[CacheEntry]:
    """Walk one approved WASM root and extract product-level cache entries."""

    entries: list[CacheEntry] = []
    root_canon = canonical_path(root, strict=True)

    for child in safe_iterdir(root_canon):
        if not child.is_dir():
            continue
        if has_reparse_point(child):
            warnings.append(f"Skipped reparse-point folder: {child}")
            continue

        if child.name.replace(" ", "").lower() in SIM_BUCKET_NAMES:
            for product in safe_iterdir(child):
                entry = _entry_from_product(location, product, root_canon, warnings)
                if entry:
                    entries.append(entry)
        else:
            entry = _entry_from_product(location, child, root_canon, warnings)
            if entry:
                entries.append(entry)

    return entries


def _entry_from_product(
    location: SimulatorLocation,
    product_path: Path,
    approved_root: Path,
    warnings: list[str],
) -> CacheEntry | None:
    """Create a CacheEntry only when the product folder is safe to expose."""

    if not product_path.is_dir():
        return None
    if has_reparse_point(product_path):
        warnings.append(f"Skipped reparse-point product folder: {product_path}")
        return None
    if not _looks_like_product_folder(product_path, approved_root):
        warnings.append(f"Skipped ambiguous folder below WASM root: {product_path}")
        return None

    return CacheEntry(
        simulator=location.simulator,
        channel=location.channel,
        product_name=product_path.name,
        cache_path=canonical_path(product_path),
        approved_root=approved_root,
        source=str(approved_root),
    )


def _looks_like_product_folder(product_path: Path, approved_root: Path) -> bool:
    """Conservatively accept product folders one or two levels below a WASM root."""

    try:
        relative_parts = product_path.relative_to(approved_root).parts
    except ValueError:
        return False

    if len(relative_parts) not in (1, 2):
        return False
    if len(relative_parts) == 1 and relative_parts[0].replace(" ", "").lower() in SIM_BUCKET_NAMES:
        return False

    name = product_path.name.strip()
    if not name or name in {".", ".."}:
        return False

    return True


def _dedupe_entries(entries: list[CacheEntry]) -> list[CacheEntry]:
    """Deduplicate entries by canonical cache path."""

    seen: set[str] = set()
    deduped: list[CacheEntry] = []
    for entry in entries:
        key = os.path.normcase(str(canonical_path(entry.cache_path)))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(entry)
    return deduped
