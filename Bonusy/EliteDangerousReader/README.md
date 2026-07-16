# Elite Dangerous Reader

Elite Dangerous Reader is a single-purpose Windows desktop application that opens only the official `elitedangerous.com` website in Microsoft Edge WebView2 and applies configurable readability overrides.

The original online page is rendered directly. The application does not download and re-host the HTML, bypass browser CORS rules, or modify the website on a proxy server.

## Main features

- Opens the official Elite Dangerous update notes by default.
- Uses the installed Microsoft Edge WebView2 runtime through Python and pywebview.
- Blocks top-level navigation outside `elitedangerous.com`.
- Provides Back, Forward, Reload, and Home controls.
- Lets the user select a replacement background color.
- Optionally overrides text color.
- Removes the selected element's background image when enabled.
- Includes a visual element picker for choosing the actual black page background.
- Provides font scaling and line-height controls.
- Persists settings in the user's application data directory.
- Includes rotating diagnostic logs and a native startup-error dialog.
- Disables downloads, file URLs, remote debugging, and external browser launches by default.
- Builds into a single Windows executable with PyInstaller.

## Repository layout

```text
EliteDangerousReader/
├── src/elite_reader/          Python package
├── src/elite_reader/assets/   Injected reader interface
├── tests/                     Unit tests
├── .github/workflows/         Windows CI and executable build
├── docs/                      User, architecture, build, and security notes
├── scripts/                   Windows setup, run, check, and build scripts
├── assets/                    Application icon
├── run_elite_reader.py       Packaging-safe launcher
├── EliteDangerousReader.spec  PyInstaller build specification
├── pyproject.toml             Package and tool configuration
├── requirements*.txt          Pinned dependencies
└── VALIDATION.md              Validation performed for this release
```

## Requirements

- Windows 10 or Windows 11, 64-bit recommended.
- Python 3.11 or newer for source execution.
- Microsoft Edge WebView2 Runtime.
- Internet access to `https://www.elitedangerous.com` and the website's normal static-resource hosts.

WebView2 is commonly present with current Microsoft Edge and Microsoft 365 installations. Corporate application-control policy can still block locally built executables or Python itself.

## Quick start from source

Open Command Prompt or PowerShell in the repository root:

```bat
scripts\setup_venv.bat
scripts\run.bat
```

The default page is:

```text
https://www.elitedangerous.com/update-notes
```

A specific approved page can be supplied:

```bat
scripts\run.bat --url https://www.elitedangerous.com/update-notes/4-4-0-3
```

Direct execution from the repository root is also supported:

```bat
python -m pip install -r requirements.txt
python run_elite_reader.py
```

Installing the project itself is optional for direct execution. For development, an
editable installation still provides the `elite-reader` console command:

```bat
python -m pip install -e .
elite-reader
```

## Using the reader controls

1. The floating **Elite Reader** panel opens in the lower-right corner.
2. Choose a background color.
3. Keep the selector as `body` for the first attempt.
4. When the visible black area does not change, select **Pick area**.
5. Move the pointer over the page until the desired background is outlined.
6. Click the outlined area.
7. The selector and visual settings are applied and saved automatically.
8. Collapse the panel with the close button. Use the **Aa** launcher to reopen it.

The element picker generates the most stable selector it can find from IDs, test attributes, roles, classes, and finally a short structural path. Website redesigns can invalidate a saved selector. Run **Pick area** again after such a redesign.

## Offline dependency preparation

On an internet-connected Windows machine using the same Python version and CPU architecture:

```bat
scripts\download_wheels.bat
```

Copy the repository with its generated `wheelhouse` directory to the restricted machine, then run:

```bat
scripts\setup_venv_offline.bat
```

The wheelhouse is excluded from Git because it is platform-specific and can be large.

## Build the executable

```bat
scripts\build_exe.bat
```

The build runs Ruff, mypy, pytest, and PyInstaller. Successful output:

```text
dist\EliteDangerousReader.exe
```

See [docs/BUILDING.md](docs/BUILDING.md) for details.

## Settings and logs

Settings:

```text
%APPDATA%\EliteDangerousReader\settings.json
```

Logs:

```text
%LOCALAPPDATA%\EliteDangerousReader\logs\elite-reader.log
```

Persistent WebView2 profile:

```text
%LOCALAPPDATA%\EliteDangerousReader\webview
```

Reset from the UI or command line:

```bat
scripts\run.bat --reset-settings
```

## Security model

The application is not a security boundary against a compromised operating system or compromised WebView2 runtime. It does reduce unnecessary capability exposure:

- Native WebView2 navigation is cancelled outside the approved domain.
- A post-load URL check provides a compatibility fallback.
- Normal page links and `window.open` calls are guarded in the injected script.
- The JavaScript-to-Python API only reads, validates, saves, and resets visual settings.
- Unknown settings fields are rejected.
- Downloads and local file URL access are disabled.
- Developer tools are disabled unless `--debug` is supplied.

The website can technically call the narrow settings API because it executes inside the WebView. That API cannot read arbitrary files or execute commands. This design avoids exposing a general-purpose native bridge to remote content.

See [SECURITY.md](SECURITY.md) and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Continuous integration

The included GitHub Actions workflow tests Python 3.11, 3.12, and 3.13 on Windows, then builds and uploads `EliteDangerousReader.exe` as a workflow artifact.

## Development commands

```bat
scripts\format.bat
scripts\check.bat
scripts\clean.bat
```

Debug mode:

```bat
scripts\run.bat --debug
```

Debug mode enables WebView2 developer tools and more verbose logs. Do not use it as the normal company deployment mode.

## License

MIT. The Elite Dangerous name and website belong to Frontier Developments. This project is an independent reader utility and contains no Frontier website assets.
