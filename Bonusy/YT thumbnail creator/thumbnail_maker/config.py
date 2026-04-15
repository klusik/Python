"""Shared configuration values for the thumbnail maker application.

This module acts as the central configuration registry for the entire project.
Keeping user-facing defaults in one place makes the GUI layer simpler and keeps
rendering behavior predictable.
"""

APP_TITLE = "YouTube Thumbnail Text Maker"

# The preview canvas is intentionally capped. The application renders the full
# image first, then creates a smaller preview copy for the Tkinter canvas.
# This keeps preview rendering visually accurate while avoiding a giant image in
# the UI surface.
CANVAS_PREVIEW_MAX_SIZE = (900, 420)

DEFAULT_EXPORT_BASENAME = "thumbnail_output"

# Supported image types are shared by the file picker dialog so the GUI layer
# does not need to hardcode file extension knowledge.
SUPPORTED_IMAGE_TYPES = [
    ("Image files", "*.png *.jpg *.jpeg *.webp *.bmp"),
    ("PNG files", "*.png"),
    ("JPEG files", "*.jpg *.jpeg"),
    ("WebP files", "*.webp"),
    ("Bitmap files", "*.bmp"),
    ("All files", "*.*"),
]

# Default visual tuning for readable YouTube-style text overlays.
DEFAULT_TITLE_SIZE = 92
DEFAULT_SUBTITLE_SIZE = 72
DEFAULT_TITLE_HORIZONTAL_RATIO = 0.50
DEFAULT_SUBTITLE_HORIZONTAL_RATIO = 0.50
DEFAULT_TITLE_VERTICAL_RATIO = 0.08
DEFAULT_SUBTITLE_VERTICAL_RATIO = 0.70
DEFAULT_STROKE_WIDTH = 6
DEFAULT_TEXT_COLOR = "#FFFFFF"
DEFAULT_SUBTITLE_COLOR = "#FFD24A"
DEFAULT_STROKE_COLOR = "#000000"
DEFAULT_OVERLAY_OPACITY = 105
DEFAULT_OVERLAY_HEIGHT_RATIO = 0.48
DEFAULT_OVERLAY_START_RATIO = 0.52
DEFAULT_PLANE_ICON = "✈"

# Preview updates are intentionally throttled so the Tkinter UI stays responsive
# while the user is dragging sliders or typing. The GUI schedules delayed
# redraws instead of rendering on every tiny change event.
PREVIEW_REFRESH_DELAY_MS = 1000
