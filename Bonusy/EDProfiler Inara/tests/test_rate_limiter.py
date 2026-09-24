"""Unit tests for the local two-requests-per-minute limit."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT_DIRECTORY = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = PROJECT_ROOT_DIRECTORY / "src"
if str(SOURCE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIRECTORY))

from inara_profile_downloader.exceptions import RequestRateLimitError
from inara_profile_downloader.rate_limiter import RequestRateLimiter


class MutableClock:
    """Deterministic monotonic clock used by the rate-limiter tests."""

    def __init__(self) -> None:
        self.current_time = 100.0

    def __call__(self) -> float:
        return self.current_time


class RequestRateLimiterTests(unittest.TestCase):
    """Verify local request spacing without sleeping."""

    def test_second_request_is_blocked_until_interval_elapsed(self) -> None:
        mutable_clock = MutableClock()
        rate_limiter = RequestRateLimiter(30.0, monotonic_clock=mutable_clock)

        rate_limiter.reserve_request_slot()
        with self.assertRaises(RequestRateLimitError):
            rate_limiter.reserve_request_slot()

        mutable_clock.current_time += 30.0
        rate_limiter.reserve_request_slot()


if __name__ == "__main__":
    unittest.main()
