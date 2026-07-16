# Contributing

## Development workflow

1. Create a focused branch.
2. Keep security-sensitive changes small and reviewable.
3. Preserve docstrings and update documentation when behavior changes.
4. Run `scripts\format.bat`.
5. Run `scripts\check.bat`.
6. Build the executable when changing packaging, pywebview integration, or assets.

## Code conventions

- Python 3.11 or newer.
- Full type annotations for public functions and methods.
- Docstrings for modules, classes, functions, and methods.
- No broad JavaScript-to-Python API exposure.
- No arbitrary external navigation.
- No silent weakening of validation.

## Dependency changes

Document why a dependency update is required. Verify the current pywebview Windows backend and PyInstaller packaging behavior before merging.
