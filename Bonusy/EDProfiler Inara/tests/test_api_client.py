"""Unit tests for payload construction and Inara response validation."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

PROJECT_ROOT_DIRECTORY = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT_DIRECTORY / "src"
if str(SOURCE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIRECTORY))

from inara_profile_downloader.api_client import InaraApiClient
from inara_profile_downloader.exceptions import InaraApiError, ValidationError
from inara_profile_downloader.models import ApiCredentials


class InaraApiClientTests(unittest.TestCase):
    """Verify request and response behavior without contacting Inara."""

    def setUp(self) -> None:
        self.credentials = ApiCredentials(
            api_key="personal-api-key-123456",
            registered_application_name="Registered Test Application",
            application_version="1.0.0",
            development_mode=True,
        )

    def test_payload_contains_expected_event_and_identity(self) -> None:
        payload = InaraApiClient.build_get_commander_profile_payload(
            credentials=self.credentials,
            commander_name="KlusikCZ",
            commander_frontier_id="F4110487",
        )

        self.assertEqual(
            payload["header"]["appName"],
            "Registered Test Application",
        )
        self.assertEqual(payload["header"]["APIkey"], "personal-api-key-123456")
        self.assertEqual(payload["header"]["commanderName"], "KlusikCZ")
        self.assertEqual(payload["header"]["commanderFrontierID"], "F4110487")
        self.assertEqual(payload["events"][0]["eventName"], "getCommanderProfile")
        self.assertEqual(payload["events"][0]["eventData"]["searchName"], "KlusikCZ")

    def test_payload_allows_personal_key_owner_lookup_without_name(self) -> None:
        payload = InaraApiClient.build_get_commander_profile_payload(
            credentials=self.credentials,
            commander_name="",
            commander_frontier_id="",
        )

        self.assertNotIn("commanderName", payload["header"])
        self.assertEqual(payload["events"][0]["eventData"], {})

    def test_successful_response_is_parsed(self) -> None:
        response_document = {
            "header": {"eventStatus": 200, "eventData": {"userID": 1}},
            "events": [
                {
                    "eventStatus": 200,
                    "eventData": {
                        "userID": 1,
                        "commanderName": "KlusikCZ",
                        "preferredPowerName": "Li Yong-Rui",
                    },
                }
            ],
        }

        parsed_response = InaraApiClient.parse_get_commander_profile_response(
            json.dumps(response_document).encode("utf-8")
        )

        self.assertEqual(parsed_response.header_status, 200)
        self.assertEqual(parsed_response.event_status, 200)
        self.assertEqual(parsed_response.profile_data["commanderName"], "KlusikCZ")

    def test_no_results_status_raises_descriptive_error(self) -> None:
        response_document = {
            "header": {"eventStatus": 200},
            "events": [
                {
                    "eventStatus": 204,
                    "eventStatusText": "No results found.",
                }
            ],
        }

        with self.assertRaisesRegex(InaraApiError, "No results found"):
            InaraApiClient.parse_get_commander_profile_response(
                json.dumps(response_document).encode("utf-8")
            )

    def test_invalid_json_raises_api_error(self) -> None:
        with self.assertRaises(InaraApiError):
            InaraApiClient.parse_get_commander_profile_response(b"not-json")

    def test_invalid_frontier_id_is_rejected_before_network_request(self) -> None:
        class NeverUsedRateLimiter:
            def reserve_request_slot(self) -> None:
                raise AssertionError("Rate limiter should not be called after validation failure.")

        client = InaraApiClient(request_rate_limiter=NeverUsedRateLimiter())  # type: ignore[arg-type]

        with self.assertRaises(ValidationError):
            client.download_commander_profile(
                credentials=self.credentials,
                commander_name="KlusikCZ",
                commander_frontier_id="invalid-id",
            )


if __name__ == "__main__":
    unittest.main()
