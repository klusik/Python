# Architecture

## Overview

The application is a small Tkinter GUI backed by `yt-dlp`. The UI collects user input, starts a worker thread, and displays progress messages produced by the downloader.

## Entry Point

- `ytd.pyw` starts the app in windowed mode.
- On Windows, `.pyw` avoids opening a console window when launched normally.

## Source Layout

- `src/app.py` owns the Tk root and application lifecycle.
- `src/main_window.py` builds the UI and handles user interaction.
- `src/download_worker.py` runs downloads on a background thread.
- `src/youtube_downloader.py` owns fallback download logic.
- `src/download_options.py` contains the user-selected options model.
- `src/download_strategy.py` contains one download strategy model.
- `src/download_message.py` contains worker-to-UI message data.
- `src/ui_logger.py` captures `yt-dlp` logs and forwards them to the UI.
- `src/runtime_environment.py` exposes bundled helper binaries to the packaged app runtime.

## Threading Model

Tkinter must be updated only from the main thread. The download worker writes `DownloadMessage` instances to a thread-safe queue. `MainWindow` polls that queue with `root.after()` and applies UI updates on the Tk thread.

## Download Strategy

The downloader tries multiple `yt-dlp` format configurations. If a strategy raises an exception, the next strategy is attempted. This gives the app practical resilience against videos where a specific container, stream split, or conversion path is unavailable.

## Packaging

PyInstaller is used for Windows and macOS. The scripts intentionally clean generated `build`, `dist`, and `.spec` files after copying the final artifact to the project root. If FFmpeg helper binaries are found during packaging, they are bundled and made available at runtime through `PATH`.
