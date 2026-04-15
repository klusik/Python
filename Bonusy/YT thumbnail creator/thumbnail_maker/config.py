"""Shared configuration values for the thumbnail maker application."""

APP_TITLE = "YouTube Thumbnail Text Maker"
CANVAS_PREVIEW_MAX_SIZE = (900, 420)
DEFAULT_EXPORT_BASENAME = "thumbnail_output"
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
DEFAULT_TITLE_X_RATIO = 0.50
DEFAULT_SUBTITLE_X_RATIO = 0.50
DEFAULT_TITLE_Y_RATIO = 0.08
DEFAULT_SUBTITLE_Y_RATIO = 0.70
DEFAULT_STROKE_WIDTH = 6
DEFAULT_TEXT_COLOR = "#FFFFFF"
DEFAULT_SUBTITLE_COLOR = "#FFD24A"
DEFAULT_STROKE_COLOR = "#000000"
DEFAULT_OVERLAY_OPACITY = 105
DEFAULT_OVERLAY_HEIGHT_RATIO = 0.48
DEFAULT_OVERLAY_START_RATIO = 0.52
DEFAULT_PLANE_ICON = "✈"

# Preview updates are intentionally throttled so the Tkinter UI stays responsive
# while the user is dragging sliders or typing.
PREVIEW_REFRESH_DELAY_MS = 1000
