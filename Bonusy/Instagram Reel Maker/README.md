# Instagram Reel Builder

Desktop utility for building simple vertical Instagram-style MP4 reels from wide photos.

## What it does

- Loads many images at once
- Groups `N` photos into one vertical screen
- Stacks them under each other as a strip
- Keeps each screen visible for a configurable duration
- Can fill the whole loaded song automatically
- Can use a selected song segment with IN and OUT controls
- Can also run in manual timing mode
- Adds optional rectangular or rounded frames around each photo
- Exports an MP4 using FFmpeg
- Prefers NVIDIA H.264 NVENC when the local FFmpeg build supports it
- Falls back to CPU H.264 automatically when NVENC is not available

## Default export choices

The project defaults to `1080x1920`, `30 FPS`, and H.264 output. Those defaults align with common Instagram Reel guidance for 9:16 vertical delivery and practical mobile playback.

## Audio modes

There are three timeline modes:

1. **Use whole song**
   - The app reads the full music duration.
   - It computes the number of screens from image count and `photos per screen`.
   - It divides the song duration evenly across all screens.

2. **Use selected song segment**
   - You choose `IN` and `OUT`.
   - The segment duration is divided evenly across all screens.
   - Final trimming is done by FFmpeg during muxing.

3. **Manual timing**
   - You choose how many photos go on one screen.
   - You choose how long one screen stays visible.
   - Optional music can still be loaded.
   - In this mode the app uses the selected `IN` point and computes the effective `OUT` from video length.

## Layout behavior

The application uses a simple, deterministic layout:

- Each screen is a full vertical image
- The selected number of photos is placed into equal-height stacked cells
- Each source photo is scaled to fit inside its cell without cropping
- Wide photos are centered inside the cell
- Background stays dark to keep contrast clean

This is intentionally conservative. It makes the result predictable and easy to maintain.

## GPU encoding

FFmpeg supports NVIDIA NVENC through encoders such as `h264_nvenc`. This app checks whether the local FFmpeg build exposes `h264_nvenc`. If yes and GPU encoding is enabled in the UI, the export uses NVENC. Otherwise it falls back to `libx264`.

## Project structure

```text
main.pyw
requirements.txt
run.bat
README.md
src/
  app.py
  controllers/
    app_controller.py
  models/
    project_settings.py
  services/
    export_service.py
    ffmpeg_service.py
    image_layout_service.py
    music_service.py
  ui/
    main_window.py
  utils/
    threading_utils.py
```

## Requirements

- Windows
- Python 3.11+ recommended
- FFmpeg is automatically provided through `imageio-ffmpeg` in most cases
- Optional NVIDIA GPU for faster H.264 export

## Running the app

### Option 1: Windows batch file

Double-click `run.bat`.

What it does:

- checks whether Python launcher `py` exists
- checks whether required Python libraries are importable
- installs missing libraries from `requirements.txt`
- launches the windowed app with `pyw`

### Option 2: Manual

```bat
py -m pip install -r requirements.txt
pyw main.pyw
```

## Notes

- Audio preview uses `ffplay` when it is available on the machine.
- Final audio trimming and muxing are done by FFmpeg.
- Export does not depend on `ffplay`, only preview does.
- The application is intentionally simple. It does not yet implement transitions, waveform views, project save files, or per-photo timing.


## Recent updates

- Added a Reverse order button for the photo list.
- Added configurable frame margin.
- Rounded frames now stay inside the video area.
- Audio preview uses FFmpeg plus Windows winsound.
