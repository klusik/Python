# Elite Profile Exporter

Exports a current Elite Dangerous commander profile from Frontier Player Journal
files into one JSON file that can be uploaded for analysis.

The exporter deliberately reads the Frontier journals rather than EDDiscovery's
private SQLite schema. EDDiscovery itself reads these journals, and its database
layout can change between releases.

## Requirements

- Windows
- Python 3.11 or newer
- Elite Dangerous journal files
- No third-party Python packages

## Fastest use

Double-click:

```text
export_profile.bat
```

The output is written next to the script:

```text
elite_profile.json
```

Upload that JSON whenever you want a complete fleet, materials, engineering or
build analysis.

## PowerShell use

```powershell
py -3 .\elite_profile_exporter.py
```

Explicit commander and output:

```powershell
py -3 .\elite_profile_exporter.py `
  --commander KlusikCZ `
  --output .\KlusikCZ_elite_profile.json `
  --include-event-summary
```

Custom journal directory:

```powershell
py -3 .\elite_profile_exporter.py `
  --journal-dir "D:\Elite Journals" `
  --output .\elite_profile.json
```

## Before exporting

For the freshest available profile:

1. Start Elite Dangerous and enter the game.
2. Open the right-hand inventory/materials panel.
3. Open Engineer progress if convenient.
4. Open the shipyard and stored modules screens if you want refreshed storage.
5. Exit to the main menu or leave the game running.
6. Run the exporter.

Elite writes some snapshot events only at startup or when a relevant screen is
opened. Old journal files improve coverage of loadouts for ships you previously
flew.

## Included data

- Commander name, Frontier ID, credits and mode
- Ranks, progress, reputation and statistics
- Current location and Powerplay state
- Raw, manufactured and encoded materials
- Odyssey backpack and ship locker companion files
- Current ship, always included even when its matching loadout snapshot is missing
- Latest known loadout for each previously flown ship, explicitly marked current/historical/stale/missing
- Stored ships and stored modules
- Engineer unlock/progress state
- Active and recently changed missions
- Fleet carrier snapshot when available
- Cargo, market, outfitting, module information and other companion snapshots

## Important limitations

Frontier does not continuously emit the complete loadout of every stored ship.
The exporter retains the latest `Loadout` event found for each ShipID. A ship
that has never been flown within the available journal history may appear in
the fleet without a detailed loadout.

Inara may contain additional server-synchronized information, but its public API
does not provide a simple unrestricted "download my entire profile" endpoint.
The journal export is the safest portable source for commander-owned data.

## Privacy

The JSON can include:

- Commander name and Frontier account ID
- Credit balance
- Fleet and loadouts
- Current or recent location
- Missions and cargo

Review it before publishing publicly. Uploading it privately for analysis is the
intended workflow.

## Git ignore

The included `.gitignore` excludes generated profile exports:

```text
elite_profile.json
*_elite_profile.json
```
