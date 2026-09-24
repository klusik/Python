"""Application-wide constants.

Keeping user-visible defaults and security boundaries in one module makes the
application easier to audit and avoids unrelated magic values in the codebase.
"""

from __future__ import annotations

APP_NAME = "Elite Dangerous Reader"
APP_SLUG = "EliteDangerousReader"
APP_AUTHOR = "Rudolf Klusal"

HOME_URL = "https://www.elitedangerous.com/update-notes"
ALLOWED_BASE_DOMAIN = "elitedangerous.com"
ALLOWED_SCHEMES = frozenset({"https"})

WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 950
WINDOW_MIN_WIDTH = 900
WINDOW_MIN_HEIGHT = 620
WINDOW_BACKGROUND_COLOR = "#30343a"

SETTINGS_FILE_NAME = "settings.json"
LOG_FILE_NAME = "elite-reader.log"
MAX_LOG_BYTES = 2_000_000
LOG_BACKUP_COUNT = 3

MAX_SELECTOR_LENGTH = 2_000
MIN_FONT_SCALE_PERCENT = 75
MAX_FONT_SCALE_PERCENT = 180
MIN_LINE_HEIGHT = 1.0
MAX_LINE_HEIGHT = 2.5
