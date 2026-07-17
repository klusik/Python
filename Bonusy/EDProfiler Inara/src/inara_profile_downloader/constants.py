"""Application-wide constants kept in one explicit location."""

from __future__ import annotations

APPLICATION_NAME = "Inara Profile Downloader"
APPLICATION_VERSION = "1.0.0"
EXPORT_SCHEMA_NAME = "inara-profile-download"
EXPORT_SCHEMA_VERSION = 1

INARA_API_ENDPOINT = "https://inara.cz/inapi/v1/"
INARA_API_DOCUMENTATION_URL = "https://inara.cz/elite/inara-api-docs/"
INARA_API_DEVELOPER_GUIDE_URL = "https://inara.cz/elite/inara-api-devguide/"
INARA_API_SETTINGS_URL = "https://inara.cz/elite/cmdr-settings-api/"

DEFAULT_REGISTERED_APPLICATION_NAME = "Inara Profile Downloader"
DEFAULT_OUTPUT_FILENAME = "inara_profile.json"
DEFAULT_NETWORK_TIMEOUT_SECONDS = 30.0
MINIMUM_REQUEST_INTERVAL_SECONDS = 30.0

SETTINGS_DIRECTORY_NAME = "InaraProfileDownloader"
SETTINGS_FILENAME = "settings.json"
LOG_DIRECTORY_NAME = "logs"
LOG_FILENAME = "application.log"
LOG_MAX_BYTES = 1_000_000
LOG_BACKUP_COUNT = 3

WINDOW_TITLE = f"{APPLICATION_NAME} {APPLICATION_VERSION}"
WINDOW_MINIMUM_WIDTH = 900
WINDOW_MINIMUM_HEIGHT = 670
