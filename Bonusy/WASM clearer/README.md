# MSFS WASM Cache Cleaner

Windows Tkinter utility for selectively clearing Microsoft Flight Simulator WASM cache entries.

## Usage

Run with the system Python installation:

```powershell
python .\WASM_clear.pyw
```

## Start Menu Shortcut

Run [`install.bat`](/C:/GIT/Python/Bonusy/WASM%20clearer/install.bat) once to create a Start Menu folder named `WASM clearer` with a shortcut to the app. After that, Windows search should find it when you type `wasm`.

The app scans known MSFS 2020 and MSFS 2024 user-data locations for Steam and Microsoft Store/Xbox installs. It also reads `UserCfg.opt` when available to show package roots.

No item is selected by default. Select only the aircraft or products whose WASM cache should be cleared, then use **Clear Selected Cache**. A confirmation dialog is shown before anything is deleted.

## Safety Notes

- Only folders discovered under known `WASM` roots are eligible.
- Deletion is refused if a selected target is outside its approved `WASM` root.
- Symlinks and junctions are skipped.
- Likely settings/state folders such as `work`, `settings`, `config`, and `logs` are preserved.
- The app continues processing other selected items if one item fails.
