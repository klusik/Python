"""Official Inara API client for the getCommanderProfile event."""

from __future__ import annotations

import json
import socket
import urllib.error
import urllib.request
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

from .constants import DEFAULT_NETWORK_TIMEOUT_SECONDS, INARA_API_ENDPOINT
from .exceptions import InaraApiError, ValidationError
from .models import ApiCredentials, InaraApiResponse, JsonObject
from .rate_limiter import RequestRateLimiter

UrlOpenCallable = Callable[..., Any]


class InaraApiClient:
    """Send validated profile requests to the official Inara API.

    @param request_rate_limiter: Local throttling service shared by all requests.
    @param api_endpoint: Official Inara API endpoint or an injected test endpoint.
    @param network_timeout_seconds: HTTPS request timeout.
    @param url_open_callable: Injectable urllib opener used by automated tests.
    """

    def __init__(
        self,
        request_rate_limiter: RequestRateLimiter,
        api_endpoint: str = INARA_API_ENDPOINT,
        network_timeout_seconds: float = DEFAULT_NETWORK_TIMEOUT_SECONDS,
        url_open_callable: UrlOpenCallable = urllib.request.urlopen,
    ) -> None:
        self._request_rate_limiter = request_rate_limiter
        self._api_endpoint = api_endpoint
        self._network_timeout_seconds = network_timeout_seconds
        self._url_open_callable = url_open_callable

    def download_commander_profile(
        self,
        credentials: ApiCredentials,
        commander_name: str,
        commander_frontier_id: str,
    ) -> InaraApiResponse:
        """Download and validate the basic commander profile exposed by Inara.

        @param credentials: In-memory personal API key and application identity.
        @param commander_name: Optional exact commander name.
        @param commander_frontier_id: Optional Frontier ID.
        @return: Validated raw response and extracted profile data.
        """

        normalized_commander_name = commander_name.strip()
        normalized_frontier_id = commander_frontier_id.strip()
        self._validate_request_inputs(
            credentials,
            normalized_commander_name,
            normalized_frontier_id,
        )

        request_payload = self.build_get_commander_profile_payload(
            credentials=credentials,
            commander_name=normalized_commander_name,
            commander_frontier_id=normalized_frontier_id,
        )
        encoded_request_payload = json.dumps(
            request_payload,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")

        http_request = urllib.request.Request(
            self._api_endpoint,
            data=encoded_request_payload,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "Accept": "application/json",
                "User-Agent": (
                    f"{credentials.registered_application_name}/"
                    f"{credentials.application_version}"
                ),
            },
            method="POST",
        )

        # Reserve immediately before the network call. Failed API responses still
        # count as requests and must therefore remain throttled.
        self._request_rate_limiter.reserve_request_slot()

        try:
            with self._url_open_callable(
                http_request,
                timeout=self._network_timeout_seconds,
            ) as http_response:
                response_bytes = http_response.read()
        except urllib.error.HTTPError as exception:
            response_text = self._read_http_error_body(exception)
            status_suffix = f" Response: {response_text}" if response_text else ""
            raise InaraApiError(
                f"Inara returned HTTP {exception.code}.{status_suffix}"
            ) from exception
        except urllib.error.URLError as exception:
            reason_text = str(exception.reason) if exception.reason else "unknown network error"
            raise InaraApiError(f"Unable to reach Inara: {reason_text}") from exception
        except (TimeoutError, socket.timeout) as exception:
            raise InaraApiError(
                f"The Inara request timed out after {self._network_timeout_seconds:g} seconds."
            ) from exception
        except OSError as exception:
            raise InaraApiError(f"The Inara request failed: {exception}") from exception

        return self.parse_get_commander_profile_response(response_bytes)

    @staticmethod
    def build_get_commander_profile_payload(
        credentials: ApiCredentials,
        commander_name: str,
        commander_frontier_id: str,
    ) -> JsonObject:
        """Build the exact JSON structure required by Inara API version 1.

        @param credentials: In-memory API credentials and app identity.
        @param commander_name: Optional exact commander name.
        @param commander_frontier_id: Optional Frontier ID.
        @return: JSON-serializable request payload.
        """

        request_header: JsonObject = {
            "appName": credentials.registered_application_name,
            "appVersion": credentials.application_version,
            "isBeingDeveloped": credentials.development_mode,
            "APIkey": credentials.api_key,
        }

        if commander_name:
            request_header["commanderName"] = commander_name
        if commander_frontier_id:
            request_header["commanderFrontierID"] = commander_frontier_id

        event_data: JsonObject = {}
        if commander_name:
            event_data["searchName"] = commander_name

        return {
            "header": request_header,
            "events": [
                {
                    "eventName": "getCommanderProfile",
                    "eventTimestamp": _current_utc_timestamp(),
                    "eventCustomID": 1,
                    "eventData": event_data,
                }
            ],
        }

    @staticmethod
    def parse_get_commander_profile_response(response_bytes: bytes) -> InaraApiResponse:
        """Decode and validate one Inara getCommanderProfile response.

        @param response_bytes: Raw response body returned by the HTTPS request.
        @return: Validated response model.
        """

        if not response_bytes:
            raise InaraApiError("Inara returned an empty response body.")

        try:
            decoded_response = json.loads(response_bytes.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exception:
            raise InaraApiError("Inara returned a response that is not valid JSON.") from exception

        if not isinstance(decoded_response, dict):
            raise InaraApiError("Inara returned a JSON value instead of the expected object.")

        response_header = decoded_response.get("header")
        if not isinstance(response_header, dict):
            raise InaraApiError("The Inara response does not contain a valid header object.")

        header_status = _read_status_code(response_header, "response header")
        _raise_for_unsuccessful_status(response_header, header_status, "Inara authorization")

        response_events = decoded_response.get("events")
        if not isinstance(response_events, list) or not response_events:
            raise InaraApiError("The Inara response does not contain a profile event.")

        profile_event = response_events[0]
        if not isinstance(profile_event, dict):
            raise InaraApiError("The Inara profile event is not a JSON object.")

        event_status = _read_status_code(profile_event, "profile event")
        _raise_for_unsuccessful_status(profile_event, event_status, "getCommanderProfile")

        profile_data = profile_event.get("eventData")
        if not isinstance(profile_data, dict):
            raise InaraApiError(
                "The getCommanderProfile response does not contain a valid eventData object."
            )

        return InaraApiResponse(
            raw_response=decoded_response,
            profile_data=profile_data,
            header_status=header_status,
            event_status=event_status,
        )

    @staticmethod
    def _validate_request_inputs(
        credentials: ApiCredentials,
        commander_name: str,
        commander_frontier_id: str,
    ) -> None:
        """Validate all values before a request is allowed to consume rate quota.

        @param credentials: API credentials supplied by the GUI.
        @param commander_name: Normalized commander name.
        @param commander_frontier_id: Normalized Frontier ID.
        """

        if not credentials.api_key.strip():
            raise ValidationError("Enter a personal Inara API key.")
        if not credentials.registered_application_name.strip():
            raise ValidationError("Enter the exact Inara-whitelisted application name.")
        if not credentials.application_version.strip():
            raise ValidationError("The application version cannot be empty.")
        if len(credentials.api_key.strip()) < 8:
            raise ValidationError("The Inara API key appears to be too short.")
        if len(commander_name) > 128:
            raise ValidationError("The commander name is unexpectedly long.")
        if commander_frontier_id and not _is_valid_frontier_id(commander_frontier_id):
            raise ValidationError(
                "The Frontier ID must contain optional leading F followed by digits, "
                "for example F123456."
            )

    @staticmethod
    def _read_http_error_body(exception: urllib.error.HTTPError) -> str:
        """Read a bounded and credential-safe HTTP error body.

        @param exception: urllib HTTP error with an optional response stream.
        @return: Compact response text limited to 500 characters.
        """

        try:
            error_body = exception.read(2_000).decode("utf-8", errors="replace").strip()
        except OSError:
            return ""
        return error_body[:500]


def _current_utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp accepted by Inara."""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _read_status_code(response_object: JsonObject, context_name: str) -> int:
    """Read an integer eventStatus from a response object.

    @param response_object: Header or event object returned by Inara.
    @param context_name: Human-readable context used in errors.
    @return: Parsed integer status code.
    """

    status_value = response_object.get("eventStatus")
    if isinstance(status_value, bool) or not isinstance(status_value, int):
        raise InaraApiError(f"The {context_name} does not contain a numeric eventStatus.")
    return status_value


def _raise_for_unsuccessful_status(
    response_object: JsonObject,
    status_code: int,
    context_name: str,
) -> None:
    """Raise for warning, soft-error or error statuses that lack usable data.

    @param response_object: Header or event object returned by Inara.
    @param status_code: Parsed event status.
    @param context_name: Operation name used in the error message.
    """

    if status_code == 200:
        return

    status_text_value = response_object.get("eventStatusText")
    status_text = (
        status_text_value.strip()
        if isinstance(status_text_value, str) and status_text_value.strip()
        else "No additional status text was returned."
    )

    if status_code == 202 and isinstance(response_object.get("eventData"), dict):
        # Inara uses 202 for warnings such as multiple possible profile matches.
        # A profile object may still be useful, so allow parsing to continue.
        return

    raise InaraApiError(f"{context_name} returned status {status_code}: {status_text}")


def _is_valid_frontier_id(frontier_id: str) -> bool:
    """Return whether a Frontier ID uses Inara's documented format."""

    numeric_portion = frontier_id[1:] if frontier_id[:1].upper() == "F" else frontier_id
    return bool(numeric_portion) and numeric_portion.isdigit()
