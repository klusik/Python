"""Application-specific exception hierarchy."""

from __future__ import annotations


class InaraProfileDownloaderError(Exception):
    """Base class for recoverable application errors."""


class ValidationError(InaraProfileDownloaderError):
    """Raised when user input or structured data fails validation."""


class RequestRateLimitError(InaraProfileDownloaderError):
    """Raised when the local request-rate limit has not yet elapsed."""


class InaraApiError(InaraProfileDownloaderError):
    """Raised when Inara rejects a request or returns an invalid response."""


class ProfileExportError(InaraProfileDownloaderError):
    """Raised when the downloaded profile cannot be written to disk."""


class ConfigurationError(InaraProfileDownloaderError):
    """Raised when non-secret settings cannot be loaded or saved."""
