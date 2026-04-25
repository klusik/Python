# YouTube Downloader

A pure windowed Tkinter application for downloading a YouTube video from a user-provided link. The app uses `yt-dlp` and automatically tries multiple download methods until one succeeds.

## Features

- Tkinter desktop UI with no terminal interaction required.
- Background downloads so the window remains responsive.
- Video download fallbacks:
  - best video plus best audio
  - MP4-compatible formats
  - best single-file stream
  - smallest available stream
- Audio-only mode with MP3 conversion when FFmpeg is available.
- Progress and backend messages are shown inside the app instead of printed to a console.
- Windows `.exe` and macOS `.app`/`.dmg` deployment scripts.

## Requirements

- Python 3.10 or newer with Tkinter support.
- Internet access.
- `yt-dlp`.
- Optional but recommended: FFmpeg installed and available on `PATH`.

FFmpeg is required for reliable video/audio merging and MP3 conversion. Without FFmpeg, some downloads still work, but merged formats and audio conversion may fail.

On macOS Homebrew Python, Tkinter may be packaged separately. If `python3 ytd.pyw` reports that `_tkinter` is missing, install the matching Tk package, for example:

```bash
brew install python-tk@3.14
```

If that package is unavailable for your Python version, use a Python.org macOS installer or another Python build that includes Tkinter.

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python ytd.pyw
```

On Windows:

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python ytd.pyw
```

## Usage

1. Run `ytd.pyw`.
2. Paste a YouTube URL.
3. Choose an output folder.
4. Select audio-only mode if needed.
5. Click **Start Download**.

Downloaded files are saved to the selected output folder using the video title and video ID.

## Packaging

### Windows

Run:

```bat
deploy.bat
```

The script creates a one-file executable with PyInstaller, copies it to the project root, and removes build helper folders/files created during packaging. If `ffmpeg` and `ffprobe` are available on the build machine, they are bundled into the executable.

### macOS

Run:

```bash
chmod +x deploy_mac.sh
./deploy_mac.sh
```

The script creates `YouTube Downloader.app` and attempts to create `YouTube-Downloader.dmg`. If `ffmpeg` and `ffprobe` are available on the build machine, they are bundled into the app. If `hdiutil` is unavailable, the `.app` bundle remains in the project root.

## Legal Note

Only download content you own, have permission to download, or are legally allowed to save for offline use. This app does not bypass DRM and relies on `yt-dlp` behavior.
