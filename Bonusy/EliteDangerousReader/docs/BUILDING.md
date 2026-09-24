# Building and development

## Supported development environment

- Windows 10 or Windows 11
- 64-bit Python 3.11, 3.12, or 3.13
- Microsoft Edge WebView2 Runtime
- Command Prompt or PowerShell

Use a clean 64-bit virtual environment. Build Windows executables on Windows because PyInstaller is not a cross-compiler.

## Setup

```bat
scripts\setup_venv.bat
```

The script creates `.venv`, installs pinned runtime and development dependencies, and installs the package in editable mode.

Manual equivalent:

```bat
py -3.12 -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m pip install -e .
```

## Run

```bat
scripts\run.bat
```

Optional arguments:

```text
--url URL
--debug
--reset-settings
--version
```

## Quality checks

```bat
scripts\check.bat
```

This runs:

1. Ruff linting.
2. Ruff formatting verification.
3. mypy strict type checking.
4. pytest with coverage output.

Apply formatting:

```bat
scripts\format.bat
```

## Build a one-file executable

```bat
scripts\build_exe.bat
```

The result is:

```text
dist\EliteDangerousReader.exe
```

The executable is unsigned. Windows SmartScreen and corporate application-control products can flag or block unsigned binaries. Code signing requires a certificate trusted by the target organization and is not automated by this repository.

## PyInstaller notes

`EliteDangerousReader.spec`:

- collects pywebview package data and binaries;
- includes the JavaScript injection resource;
- includes the Windows icon;
- excludes unused Qt, Tk, and CEF backends;
- creates a console-free one-file executable.

One-file startup extracts bundled files to a temporary directory. User settings are never written there. They are stored below `%APPDATA%`.

## Dependency updates

Dependencies are pinned for reproducibility. Update one dependency at a time, then run all checks and build the executable on a clean machine or CI runner.

Important runtime dependency:

```text
pywebview==6.2.1
```

Important build dependency:

```text
pyinstaller==6.21.0
```

## Offline wheelhouse

Prepare dependencies on an internet-connected Windows computer that matches the target Python version and architecture:

```bat
scripts\download_wheels.bat
```

Transfer the complete repository, including `wheelhouse`, then run on the restricted machine:

```bat
scripts\setup_venv_offline.bat
```

A wheelhouse prepared for a different Python ABI or CPU architecture may not install.
