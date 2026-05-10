"""Shared data models for detection, discovery, and cleanup."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class SimulatorLocation:
    """Known user-data and cache paths for one simulator/install channel."""

    simulator: str
    channel: str
    data_root: Path
    source: str
    usercfg_path: Path | None = None
    packages_path: Path | None = None
    install_path: Path | None = None
    wasm_roots: tuple[Path, ...] = field(default_factory=tuple)

    @property
    def display_name(self) -> str:
        """Return a compact human-readable label."""

        return f"{self.simulator} - {self.channel}"


@dataclass(frozen=True)
class CacheEntry:
    """A selectable product-level WASM cache entry."""

    simulator: str
    channel: str
    product_name: str
    cache_path: Path
    approved_root: Path
    source: str

    @property
    def display_name(self) -> str:
        """Return a compact human-readable label."""

        return f"{self.product_name} ({self.simulator}, {self.channel})"


@dataclass(frozen=True)
class ScanResult:
    """Result of a full detection and WASM scan pass."""

    locations: tuple[SimulatorLocation, ...]
    entries: tuple[CacheEntry, ...]
    warnings: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class CleanResult:
    """Cleanup result for one selected cache entry."""

    entry: CacheEntry
    deleted_count: int
    skipped_count: int
    errors: tuple[str, ...] = field(default_factory=tuple)
    skipped: tuple[str, ...] = field(default_factory=tuple)

    @property
    def ok(self) -> bool:
        """Whether cleanup completed without errors."""

        return not self.errors
