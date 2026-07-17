"""Atomic JSON export for downloaded Inara profile data."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .constants import (
    APPLICATION_NAME,
    APPLICATION_VERSION,
    DEFAULT_OUTPUT_FILENAME,
    EXPORT_SCHEMA_NAME,
    EXPORT_SCHEMA_VERSION,
    INARA_API_ENDPOINT,
)
from .exceptions import ProfileExportError
from .models import InaraApiResponse, JsonObject, ProfileDownloadRequest


class ProfileExporter:
    """Create one stable, self-describing JSON file for downstream analysis."""

    def export_profile(
        self,
        api_response: InaraApiResponse,
        download_request: ProfileDownloadRequest,
    ) -> Path:
        """Write the downloaded profile to an atomic stable output file.

        @param api_response: Validated response returned by the Inara client.
        @param download_request: Non-secret request metadata and output directory.
        @return: Absolute path to the generated JSON file.
        """

        output_directory = download_request.output_directory.expanduser().resolve()
        output_file = output_directory / DEFAULT_OUTPUT_FILENAME
        temporary_output_file = output_directory / f".{DEFAULT_OUTPUT_FILENAME}.tmp"

        export_document = self.build_export_document(api_response, download_request)

        try:
            output_directory.mkdir(parents=True, exist_ok=True)
            temporary_output_file.write_text(
                json.dumps(export_document, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            temporary_output_file.replace(output_file)
        except OSError as exception:
            try:
                temporary_output_file.unlink(missing_ok=True)
            except OSError:
                pass
            raise ProfileExportError(
                f"Unable to write the profile export to {output_file}: {exception}"
            ) from exception

        return output_file

    @staticmethod
    def build_export_document(
        api_response: InaraApiResponse,
        download_request: ProfileDownloadRequest,
    ) -> JsonObject:
        """Build a machine-readable export without including the API key.

        @param api_response: Validated Inara API response.
        @param download_request: Request metadata supplied by the user.
        @return: Complete JSON export object.
        """

        generated_timestamp = (
            datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        )

        return {
            "schema": {
                "name": EXPORT_SCHEMA_NAME,
                "version": EXPORT_SCHEMA_VERSION,
                "generated_at": generated_timestamp,
            },
            "source": {
                "provider": "Inara",
                "endpoint": INARA_API_ENDPOINT,
                "api_version": 1,
                "event": "getCommanderProfile",
                "application": APPLICATION_NAME,
                "application_version": APPLICATION_VERSION,
            },
            "request": {
                "registered_application_name": (
                    download_request.credentials.registered_application_name
                ),
                "development_mode": download_request.credentials.development_mode,
                "commander_name": download_request.commander_name or None,
                "commander_frontier_id": (
                    download_request.commander_frontier_id or None
                ),
                "api_key_included_in_export": False,
            },
            "api_scope": {
                "description": (
                    "The official Inara getCommanderProfile event returns only basic "
                    "profile information. Absence from this file does not mean the "
                    "commander does not own or possess the omitted data."
                ),
                "available": [
                    "Inara user identity",
                    "commander identity when matched",
                    "pilot ranks and rank progress",
                    "preferred allegiance and power",
                    "main ship summary",
                    "squadron summary",
                    "preferred game role",
                    "avatar URL",
                    "Inara profile URL",
                    "Inara game-data import activity flag",
                    "possible alternative names when returned by Inara",
                ],
                "not_available": [
                    "raw, manufactured and encoded engineering materials",
                    "Odyssey goods, assets, data and consumables",
                    "backpack and ship-locker inventories",
                    "complete fleet and ship loadouts",
                    "stored modules",
                    "cargo",
                    "credits, assets and loans",
                    "engineer unlock state",
                    "missions",
                    "game statistics",
                    "permits",
                    "travel history",
                ],
                "full_private_profile_download_supported": False,
            },
            "api_status": {
                "header": api_response.header_status,
                "profile_event": api_response.event_status,
            },
            "profile": api_response.profile_data,
            "raw_api_response": api_response.raw_response,
        }
