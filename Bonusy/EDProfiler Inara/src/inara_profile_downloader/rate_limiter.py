"""Thread-safe local request throttling for polite Inara API usage."""

from __future__ import annotations

import threading
import time
from collections.abc import Callable

from .exceptions import RequestRateLimitError


class RequestRateLimiter:
    """Prevent API requests from occurring more frequently than configured.

    @param minimum_interval_seconds: Minimum time between successful request starts.
    @param monotonic_clock: Injectable monotonic clock used by automated tests.
    """

    def __init__(
        self,
        minimum_interval_seconds: float,
        monotonic_clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._minimum_interval_seconds = minimum_interval_seconds
        self._monotonic_clock = monotonic_clock
        self._last_request_started_at: float | None = None
        self._synchronization_lock = threading.Lock()

    def reserve_request_slot(self) -> None:
        """Reserve the next request slot or raise a descriptive local limit error."""

        with self._synchronization_lock:
            current_monotonic_time = self._monotonic_clock()

            if self._last_request_started_at is not None:
                elapsed_seconds = current_monotonic_time - self._last_request_started_at
                remaining_seconds = self._minimum_interval_seconds - elapsed_seconds
                if remaining_seconds > 0:
                    rounded_remaining_seconds = max(1, int(remaining_seconds + 0.999))
                    raise RequestRateLimitError(
                        "The local Inara request limit is active. "
                        f"Wait approximately {rounded_remaining_seconds} seconds before trying again."
                    )

            self._last_request_started_at = current_monotonic_time
