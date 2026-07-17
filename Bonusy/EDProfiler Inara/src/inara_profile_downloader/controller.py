"""Application workflow orchestration independent of the Tkinter interface."""

from __future__ import annotations

import logging

from .api_client import InaraApiClient
from .configuration import ConfigurationRepository
from .exporter import ProfileExporter
from .models import (
    ApplicationSettings,
    ProfileDownloadRequest,
    ProfileDownloadResult,
)


class ProfileDownloadController:
    """Coordinate settings, API access and JSON export.

    @param api_client: Validated official Inara API client.
    @param profile_exporter: Stable JSON export service.
    @param configuration_repository: Non-secret settings persistence.
    @param application_logger: Configured package logger.
    """

    def __init__(
        self,
        api_client: InaraApiClient,
        profile_exporter: ProfileExporter,
        configuration_repository: ConfigurationRepository,
        application_logger: logging.Logger,
    ) -> None:
        self._api_client = api_client
        self._profile_exporter = profile_exporter
        self._configuration_repository = configuration_repository
        self._application_logger = application_logger

    def download_and_export(
        self,
        download_request: ProfileDownloadRequest,
    ) -> ProfileDownloadResult:
        """Download the Inara profile, export it and save non-secret settings.

        @param download_request: Complete user request containing in-memory credentials.
        @return: Successful output path and profile data.
        """

        self._application_logger.info(
            "Starting getCommanderProfile request for commander '%s' using app '%s'.",
            download_request.commander_name or "<personal-key owner>",
            download_request.credentials.registered_application_name,
        )

        api_response = self._api_client.download_commander_profile(
            credentials=download_request.credentials,
            commander_name=download_request.commander_name,
            commander_frontier_id=download_request.commander_frontier_id,
        )
        output_file = self._profile_exporter.export_profile(
            api_response,
            download_request,
        )

        self._configuration_repository.save(
            ApplicationSettings(
                registered_application_name=(
                    download_request.credentials.registered_application_name
                ),
                commander_name=download_request.commander_name,
                commander_frontier_id=download_request.commander_frontier_id,
                output_directory=str(download_request.output_directory),
                development_mode=download_request.credentials.development_mode,
            )
        )

        self._application_logger.info("Profile export written to %s.", output_file)
        return ProfileDownloadResult(
            output_file=output_file,
            profile_data=api_response.profile_data,
            event_status=api_response.event_status,
        )
