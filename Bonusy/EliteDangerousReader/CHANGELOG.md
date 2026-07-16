# Changelog

## 1.0.1 - 2026-07-16

- Fixed direct execution from an unpacked repository using `python run_elite_reader.py`.
- Added an explicit `src`-layout bootstrap to the repository launcher.
- Updated `scripts\run.bat` to use the same reliable launcher path.
- Added regression coverage for launcher path initialization.
- Deferred GUI backend import until after command-line parsing.

## 1.0.0 - 2026-07-16

- Initial repository-ready release.
- Added Microsoft Edge WebView2 reader through pywebview.
- Added strict Elite Dangerous top-level navigation policy.
- Added configurable background and optional text color.
- Added background-image removal.
- Added visual page-element picker.
- Added font scale and line-height controls.
- Added persistent settings and rotating logs.
- Added tests, linting, strict type checking, build scripts, documentation, and PyInstaller packaging.
