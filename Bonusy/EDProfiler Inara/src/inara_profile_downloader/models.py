"""Typed data models shared across the application layers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

JsonObject = dict[str, Any]


@dataclass(frozen=True, slots=True)
class ApiCredentials:
    """Credentials and application identity used for one API request.

    @param api_key: Personal Inara API key. The value must remain in memory only.
    @param registered_application_name: Exact application name whitelisted by Inara.
    @param application_version: Semantic application version sent to Inara.
    @param development_mode: Whether Inara should treat the application as being developed.
    """

    api_key: str
    registered_application_name: str
    application_version: str
    development_mode: bool


@dataclass(frozen=True, slots=True)
class ProfileDownloadRequest:
    """Complete user request passed from the GUI to the controller.

    @param credentials: In-memory Inara credentials and application identity.
    @param commander_name: Optional exact in-game commander name.
    @param commander_frontier_id: Optional Frontier identifier in F123456 form.
    @param output_directory: Directory where the stable JSON export is written.
    """

    credentials: ApiCredentials
    commander_name: str
    commander_frontier_id: str
    output_directory: Path


@dataclass(frozen=True, slots=True)
class InaraApiResponse:
    """Validated response returned by the Inara API client.

    @param raw_response: Complete decoded JSON object returned by Inara.
    @param profile_data: The eventData object returned by getCommanderProfile.
    @param header_status: Numeric status from the response header.
    @param event_status: Numeric status from the getCommanderProfile event.
    """

    raw_response: JsonObject
    profile_data: JsonObject
    header_status: int
    event_status: int


@dataclass(frozen=True, slots=True)
class ProfileDownloadResult:
    """Result returned after a successful download and export.

    @param output_file: Absolute path to the generated JSON file.
    @param profile_data: Normalized profile data returned by Inara.
    @param event_status: API event status code.
    """

    output_file: Path
    profile_data: JsonObject
    event_status: int


@dataclass(slots=True)
class ApplicationSettings:
    """Persisted non-secret application settings.

    @param registered_application_name: Exact Inara application identity.
    @param commander_name: Optional commander name remembered for convenience.
    @param commander_frontier_id: Optional Frontier ID remembered for convenience.
    @param output_directory: Last selected export directory.
    @param development_mode: Whether development mode is enabled.
    """

    registered_application_name: str
    commander_name: str
    commander_frontier_id: str
    output_directory: str
    development_mode: bool
