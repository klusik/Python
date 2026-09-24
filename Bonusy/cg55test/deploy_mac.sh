#!/usr/bin/env bash
set -euo pipefail

APP_NAME="YouTube Downloader"
DMG_NAME="YouTube-Downloader.dmg"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

if ! python -c "import tkinter" >/dev/null 2>&1; then
    echo "Tkinter is not available in this Python installation."
    echo "For Homebrew Python, install the matching package, for example: brew install python-tk@3.14"
    echo "Alternatively, use a Python.org macOS installer that includes Tkinter."
    exit 1
fi

PYINSTALLER_ARGS=()

if command -v ffmpeg >/dev/null 2>&1; then
    PYINSTALLER_ARGS+=(--add-binary "$(command -v ffmpeg):.")
fi

if command -v ffprobe >/dev/null 2>&1; then
    PYINSTALLER_ARGS+=(--add-binary "$(command -v ffprobe):.")
fi

pyinstaller --noconfirm --clean --windowed --name "$APP_NAME" "${PYINSTALLER_ARGS[@]}" ytd.pyw

rm -rf "$APP_NAME.app"
cp -R "dist/$APP_NAME.app" "$APP_NAME.app"

rm -rf build dist "$APP_NAME.spec"
rm -f "$DMG_NAME"

if command -v hdiutil >/dev/null 2>&1; then
    mkdir -p dmg_stage
    cp -R "$APP_NAME.app" dmg_stage/
    ln -s /Applications dmg_stage/Applications
    hdiutil create -volname "$APP_NAME" -srcfolder dmg_stage -ov -format UDZO "$DMG_NAME"
    rm -rf dmg_stage
    echo "Created $DMG_NAME and $APP_NAME.app in the project root."
else
    echo "hdiutil is not available. Created $APP_NAME.app in the project root."
fi
