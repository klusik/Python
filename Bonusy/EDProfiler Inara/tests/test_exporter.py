"""Unit tests for the stable profile-export format."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT_DIRECTORY = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT_DIRECTORY / "src"
if str(SOURCE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIRECTORY))

from inara_profile_downloader.exporter import ProfileExporter
from inara_profile_downloader.models import (
    ApiCredentials,
    InaraApiResponse,
    ProfileDownloadRequest,
)


class ProfileExporterTests(unittest.TestCase):
    """Verify one-file export behavior and credential exclusion."""

    def test_export_contains_scope_and_never_contains_api_key(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory_name:
            output_directory = Path(temporary_directory_name)
            credentials = ApiCredentials(
                api_key="do-not-export-this-secret",
                registered_application_name="Approved Application",
                application_version="1.0.0",
                development_mode=True,
            )
            download_request = ProfileDownloadRequest(
                credentials=credentials,
                commander_name="KlusikCZ",
                commander_frontier_id="F4110487",
                output_directory=output_directory,
            )
            raw_response = {
                "header": {"eventStatus": 200},
                "events": [
                    {
                        "eventStatus": 200,
                        "eventData": {"commanderName": "KlusikCZ"},
                    }
                ],
            }
            api_response = InaraApiResponse(
                raw_response=raw_response,
                profile_data={"commanderName": "KlusikCZ"},
                header_status=200,
                event_status=200,
            )

            output_file = ProfileExporter().export_profile(api_response, download_request)
            output_text = output_file.read_text(encoding="utf-8")
            exported_document = json.loads(output_text)

            self.assertEqual(output_file.name, "inara_profile.json")
            self.assertNotIn("do-not-export-this-secret", output_text)
            self.assertFalse(
                exported_document["api_scope"]["full_private_profile_download_supported"]
            )
            self.assertIn("profile", exported_document)
            self.assertIn("raw_api_response", exported_document)


if __name__ == "__main__":
    unittest.main()
