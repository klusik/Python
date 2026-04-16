# YouTube Thumbnail Text Maker

Simple Tkinter desktop app for creating YouTube-style thumbnail overlays from a background image.

## Features

- browse for a background image
- enter top title text
- enter bottom subtitle text
- adjust horizontal position for both text lines
- adjust vertical position for both text lines
- adjust font size for both text lines
- live preview in the right panel
- export both PNG and JPG in one click
- keeps the original background image aspect ratio
- keeps rendering logic separate from GUI logic for easier maintenance

## Project Structure

```text
thumb_maker_project/
├── app.py
├── architecture.md
├── requirements.txt
├── README.md
└── thumbnail_maker/
    ├── __init__.py
    ├── config.py
    ├── gui.py
    └── renderer.py
```

## Architecture Notes

The codebase is intentionally split into three responsibilities:

- `app.py` starts the application
- `thumbnail_maker/gui.py` owns the Tkinter interface and event wiring
- `thumbnail_maker/renderer.py` owns Pillow-based image rendering
- `thumbnail_maker/config.py` stores shared defaults and tuning values

For a much more detailed description, see `architecture.md`.

## Requirements

- Python 3.10+
- Pillow
- Tkinter

Tkinter is usually included with standard Python installers on Windows and macOS.

## Installation

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### macOS / Linux

```bash
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Usage

1. Click **Browse image...**
2. Select your background image
3. Enter the top and bottom text
4. Adjust the position sliders if needed
5. Adjust the font size sliders if needed
6. Review the preview on the right side
7. Click **Generate PNG + JPG**
8. Choose an export folder

The app writes both files using the same base name.

Example:

- `thumbnail_output.png`
- `thumbnail_output.jpg`

## Notes

- The app uses a bold font if one of the common system bold fonts is found.
- If no expected bold font is available, Pillow falls back to its default font.
- The app adds a dark readability overlay near the bottom so subtitle text stays visible.
- The original image is not modified.
