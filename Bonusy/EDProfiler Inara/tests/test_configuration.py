"""Unit tests for secret-free settings persistence."""

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

from inara_profile_downloader.configuration import ConfigurationRepository
from inara_profile_downloader.models import ApplicationSettings


class ConfigurationRepositoryTests(unittest.TestCase):
    """Ensure remembered settings never gain an API-key property."""

    def test_save_and_load_non_secret_settings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory_name:
            settings_file = Path(temporary_directory_name) / "settings.json"
            repository = ConfigurationRepository(settings_file=settings_file)
            expected_settings = ApplicationSettings(
                registered_application_name="Approved Application",
                commander_name="KlusikCZ",
                commander_frontier_id="F4110487",
                output_directory="C:/Exports",
                development_mode=True,
            )

            repository.save(expected_settings)
            loaded_settings = repository.load(Path("C:/Default"))
            serialized_settings = json.loads(settings_file.read_text(encoding="utf-8"))

            self.assertEqual(loaded_settings, expected_settings)
            self.assertNotIn("api_key", serialized_settings)
            self.assertNotIn("APIkey", serialized_settings)


if __name__ == "__main__":
    unittest.main()
