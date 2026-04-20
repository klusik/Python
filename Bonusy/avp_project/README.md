# ACARS Virtual Printer

ACARS Virtual Printer is a small Windows tray application written in Python and Tkinter.
It receives plain-text print jobs from a Windows printer configured with the built-in **Generic / Text Only** driver and saves them into a text file.

## What this project does

- Runs in the Windows tray
- Listens on `127.0.0.1:9100` for RAW text print jobs
- Saves each new printout at the **top** of the selected TXT file
- Separates entries with `80 * "="`
- Minimizing or closing the window keeps the app running in the tray
- Right-clicking the tray icon allows opening the window or quitting the app
- Optionally registers itself to run after Windows logon

## Important technical note

A true Windows-visible printer is not created by Tkinter itself.
The Windows printer is created by using the built-in **Generic / Text Only** driver and a local TCP printer port that points to this app:

- Host: `127.0.0.1`
- Port: `9100`
- Data type: RAW

This project includes a PowerShell helper script that attempts to create the printer for you:

- `setup_printer.ps1`
- `remove_printer.ps1`

If the built-in **Generic / Text Only** driver is not already available on your system, Windows print management may need to add it first.

## Example output format

```text
17-04-2026 0630Z:
METAR LKPR 170630Z 22008KT 9999 FEW030 08/02 Q1018
================================================================================
16-04-2026 0625Z:
LOADSHEET: ZFW 58.3 / FOB 8.1
```

Each newest message is prepended to the file.

## Running from source

1. Install Python 3.11 or newer.
2. Run `run.bat`.
3. In the app, choose the output TXT file.
4. Start the printer setup script in PowerShell as Administrator if needed:

```powershell
powershell -ExecutionPolicy Bypass -File .\setup_printer.ps1
```

After that, print plain text to **ACARS Virtual Printer** from your ACARS-capable app.

## Building a standalone EXE

Run:

```bat
deploy.bat
```

The script:

- installs build dependencies
- builds a one-file executable with PyInstaller
- copies `AVP.exe` to the project root
- deletes generated build folders and temporary helper artifacts

## Project structure

```text
AVP.pyw
requirements.txt
run.bat
deploy.bat
setup_printer.ps1
remove_printer.ps1
src/
```

## Notes and limitations

- The receiver is designed for plain text only.
- Binary print jobs, graphics, and rich page descriptions are intentionally not supported.
- The printer setup step may require administrator rights.
- If another service already uses TCP port `9100`, the receiver must be moved to a different port and the printer port configuration updated to match.
