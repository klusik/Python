"""Shared data models for detection, discovery, and cleanup."""

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


@dataclass(frozen=True)
class CleanPlanItem:
    """Preview statistics for one selected cache entry."""

    entry: CacheEntry
    file_count: int
    directory_count: int
    byte_count: int
    preserved_count: int
    warning_count: int


@dataclass(frozen=True)
class CleanPlan:
    """Complete read-only preview of a proposed cleanup."""

    items: tuple[CleanPlanItem, ...]
    warnings: tuple[str, ...] = field(default_factory=tuple)

    @property
    def file_count(self) -> int:
        return sum(item.file_count for item in self.items)

    @property
    def directory_count(self) -> int:
        return sum(item.directory_count for item in self.items)

    @property
    def byte_count(self) -> int:
        return sum(item.byte_count for item in self.items)

    @property
    def preserved_count(self) -> int:
        return sum(item.preserved_count for item in self.items)


@dataclass(frozen=True)
class CacheFileDetail:
    """One inspected path shown in the cache-details window."""

    relative_path: str
    byte_count: int
    modified_time: float | None
    kind: str
    disposition: str


@dataclass(frozen=True)
class CacheEntryDetails:
    """Bounded, read-only file details for one cache entry."""

    entry: CacheEntry
    files: tuple[CacheFileDetail, ...]
    warnings: tuple[str, ...] = field(default_factory=tuple)
    truncated: bool = False
