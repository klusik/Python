#!/usr/bin/env python3
"""
Export an Elite Dangerous commander profile from Frontier journal files.

The exporter uses only Python's standard library. It reads the same Player
Journal source used by EDDiscovery and writes a compact JSON snapshot suitable
for analysis or archival.

Supported data includes:
- commander identity, credits, ranks, reputation and statistics
- current location and Powerplay state
- raw, manufactured and encoded materials
- Odyssey backpack and ship locker snapshots
- current ship and latest known loadout for every previously flown ship
- stored ships and stored modules
- engineer progress
- active missions
- fleet carrier state when present
- current cargo and selected companion JSON snapshots

The journal is append-only, but many profile records are emitted only at game
startup or when opening a relevant panel. For the freshest export, start Elite,
enter the game, open the right-hand inventory and engineers panels, then run
this exporter after EDDiscovery has processed the session.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


DEFAULT_JOURNAL_DIR = (
    Path.home()
    / "Saved Games"
    / "Frontier Developments"
    / "Elite Dangerous"
)

SNAPSHOT_EVENTS = {
    "Commander",
    "LoadGame",
    "Rank",
    "Progress",
    "Reputation",
    "Statistics",
    "Powerplay",
    "Materials",
    "EngineerProgress",
    "Cargo",
    "Missions",
    "StoredShips",
    "StoredModules",
    "Loadout",
    "Location",
    "Docked",
    "CarrierStats",
    "SquadronStartup",
}

AUXILIARY_FILES = (
    "Backpack.json",
    "Cargo.json",
    "FCMaterials.json",
    "Market.json",
    "ModulesInfo.json",
    "NavRoute.json",
    "Outfitting.json",
    "ShipLocker.json",
    "Status.json",
)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Export an Elite Dangerous commander profile to JSON."
    )
    parser.add_argument(
        "--journal-dir",
        type=Path,
        default=DEFAULT_JOURNAL_DIR,
        help=f"Journal directory. Default: {DEFAULT_JOURNAL_DIR}",
    )
    parser.add_argument(
        "--commander",
        help=(
            "Commander name to export. Matching is case-insensitive. "
            "If omitted, the most recently active commander is selected."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("elite_profile.json"),
        help="Output JSON path. Default: elite_profile.json",
    )
    parser.add_argument(
        "--include-event-summary",
        action="store_true",
        help="Include event counts and first/last timestamps.",
    )
    parser.add_argument(
        "--pretty",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Pretty-print JSON. Enabled by default.",
    )
    return parser.parse_args()


def normalize_name(value: Any) -> str:
    """Normalize an Elite internal identifier for stable dictionary keys."""
    if value is None:
        return ""
    text = str(value).strip()
    if text.startswith("$") and text.endswith(";"):
        text = text[1:-1]
    return text.casefold()


def display_name(item: dict[str, Any]) -> str:
    """Return the localized item name when present."""
    for key in ("Name_Localised", "Name_Localized", "Name", "Type_Localised", "Type"):
        value = item.get(key)
        if value:
            return str(value)
    return ""


def read_json_file(path: Path) -> Any:
    """Read a JSON file and return None when it cannot be decoded."""
    try:
        with path.open("r", encoding="utf-8-sig") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None


def iter_journal_files(directory: Path) -> list[Path]:
    """Return journal files in chronological filename order."""
    files = list(directory.glob("Journal.*.log"))
    files.extend(directory.glob("Journal.*.01.log"))
    return sorted(set(files), key=lambda p: p.name)


def iter_events(files: Iterable[Path]) -> Iterable[tuple[Path, int, dict[str, Any]]]:
    """Yield decoded journal events with source file and line number."""
    for path in files:
        try:
            with path.open("r", encoding="utf-8-sig", errors="replace") as handle:
                for line_number, line in enumerate(handle, start=1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(event, dict):
                        yield path, line_number, event
        except OSError:
            continue


def commander_sessions(
    events: list[tuple[Path, int, dict[str, Any]]],
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, str]]:
    """
    Partition journal events by commander.

    Journal files normally contain one commander session. The active commander
    is established by Commander, NewCommander or LoadGame. Events before that
    point are ignored because they cannot be attributed safely.
    """
    sessions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    canonical_names: dict[str, str] = {}
    active_by_file: dict[Path, str] = {}

    for path, _, event in events:
        event_name = event.get("event")
        commander = None
        if event_name in {"Commander", "NewCommander", "LoadGame"}:
            commander = event.get("Name") or event.get("Commander")
        if commander:
            key = str(commander).casefold()
            canonical_names[key] = str(commander)
            active_by_file[path] = key

        key = active_by_file.get(path)
        if key:
            sessions[key].append(event)

    return dict(sessions), canonical_names


def select_commander(
    sessions: dict[str, list[dict[str, Any]]],
    canonical_names: dict[str, str],
    requested: str | None,
) -> tuple[str, list[dict[str, Any]]]:
    """Select the requested or most recently active commander."""
    if not sessions:
        raise RuntimeError("No commander sessions were found in the journal files.")

    if requested:
        key = requested.casefold()
        if key not in sessions:
            available = ", ".join(sorted(canonical_names.values()))
            raise RuntimeError(
                f"Commander {requested!r} was not found. Available: {available}"
            )
        return canonical_names[key], sessions[key]

    def last_timestamp(item: tuple[str, list[dict[str, Any]]]) -> str:
        _, commander_events = item
        return max((str(e.get("timestamp", "")) for e in commander_events), default="")

    key, selected = max(sessions.items(), key=last_timestamp)
    return canonical_names[key], selected


def clean_event(event: dict[str, Any]) -> dict[str, Any]:
    """Return a copy without the redundant event field."""
    result = copy.deepcopy(event)
    result.pop("event", None)
    return result


def set_material_snapshot(
    target: dict[str, dict[str, dict[str, Any]]],
    event: dict[str, Any],
) -> None:
    """Replace material state from a Materials snapshot event."""
    mappings = {
        "Raw": "raw",
        "Manufactured": "manufactured",
        "Encoded": "encoded",
    }
    for source_key, target_key in mappings.items():
        category: dict[str, dict[str, Any]] = {}
        for item in event.get(source_key, []) or []:
            key = normalize_name(item.get("Name"))
            if not key:
                continue
            category[key] = {
                "name": display_name(item),
                "internal_name": item.get("Name"),
                "count": int(item.get("Count", 0)),
            }
        target[target_key] = category


def update_material(
    materials: dict[str, dict[str, dict[str, Any]]],
    event: dict[str, Any],
    delta: int,
) -> None:
    """Apply a MaterialCollected or MaterialDiscarded delta."""
    category_key = str(event.get("Category", "")).casefold()
    category_map = {
        "raw": "raw",
        "manufactured": "manufactured",
        "encoded": "encoded",
    }
    category = category_map.get(category_key)
    if not category:
        return
    name = event.get("Name")
    key = normalize_name(name)
    if not key:
        return
    existing = materials[category].setdefault(
        key,
        {
            "name": event.get("Name_Localised") or name,
            "internal_name": name,
            "count": 0,
        },
    )
    existing["count"] = max(0, int(existing.get("count", 0)) + delta)


def apply_material_trade(
    materials: dict[str, dict[str, dict[str, Any]]],
    event: dict[str, Any],
) -> None:
    """Apply a MaterialTrade journal event."""
    for field, sign in (("Paid", -1), ("Received", 1)):
        item = event.get(field)
        if not isinstance(item, dict):
            continue
        category = str(item.get("Category", "")).casefold()
        if category not in materials:
            continue
        key = normalize_name(item.get("Material"))
        if not key:
            continue
        existing = materials[category].setdefault(
            key,
            {
                "name": item.get("Material_Localised") or item.get("Material"),
                "internal_name": item.get("Material"),
                "count": 0,
            },
        )
        quantity = int(item.get("Quantity", 0))
        existing["count"] = max(0, int(existing.get("count", 0)) + sign * quantity)


def sort_materials(
    materials: dict[str, dict[str, dict[str, Any]]],
) -> dict[str, list[dict[str, Any]]]:
    """Convert material dictionaries to stable, readable arrays."""
    result: dict[str, list[dict[str, Any]]] = {}
    for category, values in materials.items():
        result[category] = sorted(
            values.values(),
            key=lambda item: (str(item.get("name", "")).casefold(), str(item.get("internal_name", ""))),
        )
    return result


def mission_snapshot(event: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Convert a Missions event to a dictionary keyed by mission ID."""
    result: dict[str, dict[str, Any]] = {}
    for bucket in ("Active", "Failed", "Complete"):
        for mission in event.get(bucket, []) or []:
            mission_id = str(mission.get("MissionID", ""))
            if mission_id:
                record = copy.deepcopy(mission)
                record["snapshot_state"] = bucket.casefold()
                result[mission_id] = record
    return result


def update_mission_state(
    missions: dict[str, dict[str, Any]],
    event: dict[str, Any],
) -> None:
    """Apply mission lifecycle events."""
    name = event.get("event")
    mission_id = str(event.get("MissionID", ""))
    if not mission_id:
        return

    if name == "MissionAccepted":
        missions[mission_id] = clean_event(event)
        missions[mission_id]["state"] = "active"
    elif name in {"MissionCompleted", "MissionFailed", "MissionAbandoned"}:
        record = missions.setdefault(mission_id, {})
        record.update(clean_event(event))
        record["state"] = name.removeprefix("Mission").casefold()


def export_profile(
    commander: str,
    events: list[dict[str, Any]],
    journal_dir: Path,
    include_event_summary: bool,
) -> dict[str, Any]:
    """Build the profile snapshot."""
    latest: dict[str, dict[str, Any]] = {}
    materials: dict[str, dict[str, dict[str, Any]]] = {
        "raw": {},
        "manufactured": {},
        "encoded": {},
    }
    ships: dict[str, dict[str, Any]] = {}
    stored_ships: dict[str, dict[str, Any]] = {}
    missions: dict[str, dict[str, Any]] = {}
    engineers: dict[str, dict[str, Any]] = {}
    carrier: dict[str, Any] = {}
    event_counts: dict[str, int] = defaultdict(int)
    first_timestamp = ""
    last_timestamp = ""

    current_ship_id: str | None = None

    for event in events:
        event_name = str(event.get("event", ""))
        timestamp = str(event.get("timestamp", ""))
        if timestamp:
            first_timestamp = first_timestamp or timestamp
            last_timestamp = max(last_timestamp, timestamp)
        event_counts[event_name] += 1

        if event_name in SNAPSHOT_EVENTS:
            latest[event_name] = clean_event(event)

        if event_name in {"LoadGame", "Loadout"} and event.get("ShipID") is not None:
            current_ship_id = str(event["ShipID"])

        if event_name == "Loadout":
            ship_id = str(event.get("ShipID", ""))
            if ship_id:
                ships[ship_id] = clean_event(event)

        elif event_name == "StoredShips":
            stored_ships.clear()
            for item in (event.get("ShipsHere", []) or []) + (event.get("ShipsRemote", []) or []):
                ship_id = str(item.get("ShipID", ""))
                if ship_id:
                    stored_ships[ship_id] = copy.deepcopy(item)

        elif event_name == "ShipyardBuy":
            ship_id = str(event.get("NewShipID", ""))
            if ship_id:
                stored_ships.setdefault(
                    ship_id,
                    {
                        "ShipID": event.get("NewShipID"),
                        "ShipType": event.get("ShipType"),
                        "ShipType_Localised": event.get("ShipType_Localised"),
                    },
                )

        elif event_name == "ShipyardSell":
            sold_id = str(event.get("SellShipID", ""))
            stored_ships.pop(sold_id, None)
            ships.pop(sold_id, None)

        elif event_name == "ShipyardSwap":
            current_ship_id = str(event.get("ShipID", current_ship_id or "")) or current_ship_id

        elif event_name == "Materials":
            set_material_snapshot(materials, event)

        elif event_name == "MaterialCollected":
            update_material(materials, event, int(event.get("Count", 0)))

        elif event_name == "MaterialDiscarded":
            update_material(materials, event, -int(event.get("Count", 0)))

        elif event_name == "MaterialTrade":
            apply_material_trade(materials, event)

        elif event_name == "EngineerProgress":
            for item in event.get("Engineers", []) or []:
                key = str(item.get("EngineerID") or item.get("Engineer", ""))
                if key:
                    engineers[key] = copy.deepcopy(item)

        elif event_name == "EngineerContribution":
            key = str(event.get("EngineerID") or event.get("Engineer", ""))
            if key:
                engineers.setdefault(key, {}).update(clean_event(event))

        elif event_name == "Missions":
            missions = mission_snapshot(event)

        elif event_name.startswith("Mission"):
            update_mission_state(missions, event)

        elif event_name == "CarrierStats":
            carrier.update(clean_event(event))

        elif event_name.startswith("Carrier") or event_name.startswith("FC"):
            if event_name not in {"CarrierJumpRequest", "CarrierJumpCancelled"}:
                carrier["last_event"] = {
                    "type": event_name,
                    **clean_event(event),
                }

    merged_fleet: list[dict[str, Any]] = []
    all_ship_ids = sorted(
        set(ships) | set(stored_ships),
        key=lambda value: int(value) if value.isdigit() else value,
    )
    for ship_id in all_ship_ids:
        merged_fleet.append(
            {
                "ship_id": int(ship_id) if ship_id.isdigit() else ship_id,
                "is_current": ship_id == current_ship_id,
                "stored_ship": stored_ships.get(ship_id),
                "latest_known_loadout": ships.get(ship_id),
            }
        )

    auxiliary: dict[str, Any] = {}
    for filename in AUXILIARY_FILES:
        path = journal_dir / filename
        value = read_json_file(path)
        if value is not None:
            auxiliary[filename] = value

    load_game = latest.get("LoadGame", {})
    commander_event = latest.get("Commander", {})
    location = latest.get("Location") or latest.get("Docked") or {}

    profile: dict[str, Any] = {
        "schema": {
            "name": "elite-profile-export",
            "version": 1,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source": "Frontier Player Journal",
            "journal_directory": str(journal_dir),
        },
        "commander": {
            "name": commander,
            "fid": commander_event.get("FID") or load_game.get("FID"),
            "credits": load_game.get("Credits"),
            "loan": load_game.get("Loan"),
            "game_mode": load_game.get("GameMode"),
            "group": load_game.get("Group"),
            "odyssey": load_game.get("Odyssey"),
            "language": load_game.get("language"),
            "game_version": load_game.get("gameversion"),
        },
        "ranks": latest.get("Rank"),
        "rank_progress": latest.get("Progress"),
        "reputation": latest.get("Reputation"),
        "statistics": latest.get("Statistics"),
        "powerplay": latest.get("Powerplay"),
        "squadron": latest.get("SquadronStartup"),
        "location": location,
        "current_ship_id": int(current_ship_id) if current_ship_id and current_ship_id.isdigit() else current_ship_id,
        "fleet": merged_fleet,
        "stored_modules": latest.get("StoredModules"),
        "materials": sort_materials(materials),
        "engineers": sorted(
            engineers.values(),
            key=lambda item: str(item.get("Engineer", "")).casefold(),
        ),
        "missions": sorted(
            missions.values(),
            key=lambda item: str(item.get("MissionID", "")),
        ),
        "fleet_carrier": carrier or None,
        "auxiliary_snapshots": auxiliary,
        "coverage": {
            "first_event_timestamp": first_timestamp or None,
            "last_event_timestamp": last_timestamp or None,
            "journal_event_count": len(events),
            "known_ship_loadout_count": len(ships),
            "known_stored_ship_count": len(stored_ships),
            "notes": [
                "A ship loadout is available only after that ship produced a Loadout event.",
                "Some snapshots are emitted at game startup or when opening the relevant cockpit panel.",
                "Historical journals improve fleet coverage but are not required for current materials and commander state.",
            ],
        },
    }

    if include_event_summary:
        profile["coverage"]["event_counts"] = dict(sorted(event_counts.items()))

    return profile


def main() -> int:
    """Run the command-line exporter."""
    args = parse_args()
    journal_dir = args.journal_dir.expanduser().resolve()

    if not journal_dir.is_dir():
        print(f"ERROR: Journal directory does not exist: {journal_dir}", file=sys.stderr)
        print(
            "Use --journal-dir to point at the folder containing Journal.*.log files.",
            file=sys.stderr,
        )
        return 2

    files = iter_journal_files(journal_dir)
    if not files:
        print(f"ERROR: No Journal.*.log files found in {journal_dir}", file=sys.stderr)
        return 2

    raw_events = list(iter_events(files))
    sessions, canonical_names = commander_sessions(raw_events)

    try:
        commander, selected_events = select_commander(
            sessions,
            canonical_names,
            args.commander,
        )
        profile = export_profile(
            commander,
            selected_events,
            journal_dir,
            args.include_event_summary,
        )
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(
            profile,
            handle,
            ensure_ascii=False,
            indent=2 if args.pretty else None,
            sort_keys=False,
        )
        handle.write("\n")

    print(f"Commander: {commander}")
    print(f"Journal files: {len(files)}")
    print(f"Commander events: {len(selected_events)}")
    print(f"Fleet entries: {len(profile['fleet'])}")
    print(f"Output: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
