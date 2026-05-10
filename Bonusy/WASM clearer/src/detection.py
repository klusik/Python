"""Detect MSFS user-data roots, package roots, and likely WASM cache roots."""

from __future__ import annotations

import os
import re
from pathlib import Path

from .models import SimulatorLocation
from .path_utils import canonical_path, existing_directories, expanded_path

INSTALLED_PACKAGES_RE = re.compile(r'^\s*InstalledPackagesPath\s+"?([^"\r\n]+)"?', re.IGNORECASE)


def detect_simulator_locations() -> tuple[SimulatorLocation, ...]:
    """Return known MSFS 2020/2024 locations for Steam and Microsoft Store/Xbox installs."""

    candidates = _known_user_data_locations()
    steam_installs = _detect_steam_install_paths()
    locations: list[SimulatorLocation] = []

    for candidate in candidates:
        data_root = canonical_path(candidate["data_root"])
        usercfg_path = candidate.get("usercfg_path")
        usercfg = canonical_path(usercfg_path) if usercfg_path else None
        configured_packages = _read_installed_packages_path(usercfg) if usercfg else None
        default_packages = tuple(canonical_path(path) for path in candidate.get("package_paths", ()))

        packages_path = configured_packages or next((path for path in default_packages if path.exists()), None)
        wasm_roots = _existing_or_named_wasm_roots(candidate.get("wasm_roots", ()))
        install_path = steam_installs.get((candidate["simulator"], candidate["channel"]))

        if not _location_has_signal(data_root, usercfg, packages_path, wasm_roots, install_path):
            continue

        locations.append(
            SimulatorLocation(
                simulator=candidate["simulator"],
                channel=candidate["channel"],
                data_root=data_root,
                source=candidate["source"],
                usercfg_path=usercfg,
                packages_path=packages_path,
                install_path=install_path,
                wasm_roots=wasm_roots,
            )
        )

    return tuple(_dedupe_locations(locations))


def _known_user_data_locations() -> tuple[dict[str, object], ...]:
    """Build conservative candidate roots for supported MSFS install channels."""

    localappdata = expanded_path(os.environ.get("LOCALAPPDATA", r"%LOCALAPPDATA%"))
    appdata = expanded_path(os.environ.get("APPDATA", r"%APPDATA%"))

    fs2020_store_base = localappdata / "Packages" / "Microsoft.FlightSimulator_8wekyb3d8bbwe"
    fs2024_store_base = localappdata / "Packages" / "Microsoft.Limitless_8wekyb3d8bbwe"
    fs2020_steam_base = appdata / "Microsoft Flight Simulator"
    fs2024_steam_base = appdata / "Microsoft Flight Simulator 2024"

    return (
        {
            "simulator": "MSFS 2020",
            "channel": "Microsoft Store/Xbox",
            "data_root": fs2020_store_base,
            "usercfg_path": fs2020_store_base / "LocalCache" / "UserCfg.opt",
            "package_paths": (fs2020_store_base / "LocalCache" / "Packages",),
            "wasm_roots": (
                fs2020_store_base / "LocalState" / "WASM",
                fs2020_store_base / "LocalCache" / "WASM",
            ),
            "source": "Known Microsoft Store/Xbox package identity",
        },
        {
            "simulator": "MSFS 2020",
            "channel": "Steam",
            "data_root": fs2020_steam_base,
            "usercfg_path": fs2020_steam_base / "UserCfg.opt",
            "package_paths": (fs2020_steam_base / "Packages",),
            "wasm_roots": (fs2020_steam_base / "WASM",),
            "source": "Known Steam roaming profile folder",
        },
        {
            "simulator": "MSFS 2024",
            "channel": "Microsoft Store/Xbox",
            "data_root": fs2024_store_base,
            "usercfg_path": fs2024_store_base / "LocalCache" / "UserCfg.opt",
            "package_paths": (fs2024_store_base / "LocalCache" / "Packages",),
            "wasm_roots": (
                fs2024_store_base / "LocalState" / "WASM",
                fs2024_store_base / "LocalCache" / "WASM",
            ),
            "source": "Known Microsoft Store/Xbox package identity",
        },
        {
            "simulator": "MSFS 2024",
            "channel": "Steam",
            "data_root": fs2024_steam_base,
            "usercfg_path": fs2024_steam_base / "UserCfg.opt",
            "package_paths": (fs2024_steam_base / "Packages",),
            "wasm_roots": (fs2024_steam_base / "WASM",),
            "source": "Known Steam roaming profile folder",
        },
    )


def _read_installed_packages_path(usercfg_path: Path) -> Path | None:
    """Extract the InstalledPackagesPath entry from a UserCfg.opt file."""

    if not usercfg_path.exists():
        return None

    try:
        for line in usercfg_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            match = INSTALLED_PACKAGES_RE.match(line)
            if match:
                return canonical_path(match.group(1))
    except OSError:
        return None

    return None


def _existing_or_named_wasm_roots(paths: tuple[Path, ...]) -> tuple[Path, ...]:
    """Return paths named WASM when they exist; named candidates remain discoverable in UI roots."""

    return existing_directories(path for path in paths if path.name.lower() == "wasm")


def _location_has_signal(
    data_root: Path,
    usercfg_path: Path | None,
    packages_path: Path | None,
    wasm_roots: tuple[Path, ...],
    install_path: Path | None,
) -> bool:
    """Return True when a candidate location has at least one real filesystem signal."""

    return any(
        (
            data_root.exists(),
            bool(usercfg_path and usercfg_path.exists()),
            bool(packages_path and packages_path.exists()),
            bool(wasm_roots),
            bool(install_path and install_path.exists()),
        )
    )


def _dedupe_locations(locations: list[SimulatorLocation]) -> list[SimulatorLocation]:
    """Deduplicate detected locations by simulator, channel, and canonical root path."""

    seen: set[tuple[str, str, str]] = set()
    deduped: list[SimulatorLocation] = []
    for location in locations:
        key = (
            location.simulator,
            location.channel,
            os.path.normcase(str(canonical_path(location.data_root))),
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(location)
    return deduped


def _detect_steam_install_paths() -> dict[tuple[str, str], Path]:
    """Return Steam install directories when discoverable from library manifests."""

    result: dict[tuple[str, str], Path] = {}
    app_ids = {
        "1250410": "MSFS 2020",
        "2537590": "MSFS 2024",
    }

    for library in _steam_library_paths():
        steamapps = library / "steamapps"
        for app_id, simulator in app_ids.items():
            manifest = steamapps / f"appmanifest_{app_id}.acf"
            install_dir = _read_steam_install_dir(manifest)
            if install_dir:
                result[(simulator, "Steam")] = canonical_path(steamapps / "common" / install_dir)

    return result


def _steam_library_paths() -> tuple[Path, ...]:
    roots: list[Path] = []

    for value in (
        os.environ.get("PROGRAMFILES(X86)"),
        os.environ.get("PROGRAMFILES"),
    ):
        if value:
            roots.append(expanded_path(value) / "Steam")

    roots.extend(_steam_roots_from_registry())

    libraries: list[Path] = []
    for root in roots:
        if root.is_dir():
            libraries.append(root)
            libraries.extend(_read_steam_libraryfolders(root / "steamapps" / "libraryfolders.vdf"))

    seen: set[str] = set()
    deduped: list[Path] = []
    for library in libraries:
        canon = canonical_path(library)
        key = os.path.normcase(str(canon))
        if key not in seen:
            seen.add(key)
            deduped.append(canon)
    return tuple(deduped)


def _steam_roots_from_registry() -> tuple[Path, ...]:
    """Read Steam install roots from the Windows registry when available."""

    try:
        import winreg
    except ImportError:
        return ()

    roots: list[Path] = []
    keys = (
        (winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Valve\Steam"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Valve\Steam"),
    )
    for hive, name in keys:
        try:
            with winreg.OpenKey(hive, name) as key:
                for value_name in ("SteamPath", "InstallPath"):
                    try:
                        value, _ = winreg.QueryValueEx(key, value_name)
                    except OSError:
                        continue
                    if value:
                        roots.append(expanded_path(value))
        except OSError:
            continue
    return tuple(roots)


def _read_steam_libraryfolders(path: Path) -> tuple[Path, ...]:
    """Parse Steam library folder declarations from libraryfolders.vdf."""

    if not path.exists():
        return ()

    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ()

    libraries: list[Path] = []
    for match in re.finditer(r'"path"\s+"([^"]+)"', text, re.IGNORECASE):
        libraries.append(expanded_path(match.group(1).replace("\\\\", "\\")))
    return tuple(libraries)


def _read_steam_install_dir(manifest: Path) -> str | None:
    """Read the installed directory name from a Steam appmanifest file."""

    if not manifest.exists():
        return None

    try:
        text = manifest.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None

    match = re.search(r'"installdir"\s+"([^"]+)"', text, re.IGNORECASE)
    return match.group(1) if match else None
