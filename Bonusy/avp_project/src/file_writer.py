"""Output file writing utilities.

The printer receiver creates short text records. New records are inserted at
the top of the destination file so the latest ACARS printout is always first.
"""

from datetime import datetime, timezone
from pathlib import Path
import tempfile

from .constants import SEPARATOR_LINE


class CapturedTextWriter:
    """Write captured ACARS text into the configured output file."""

    def write_entry(self, output_file_path, payload_text):
        """Prepend one timestamped entry to the output file.

        Parameters
        ----------
        output_file_path:
            Destination TXT file path.
        payload_text:
            Plain text that was received from the Windows printer job.
        """
        normalized_payload = self._normalize_payload(payload_text)
        if not normalized_payload:
            return

        destination_path = Path(output_file_path)
        destination_path.parent.mkdir(parents=True, exist_ok=True)

        timestamp_line = self._build_timestamp_line()
        entry_text = f"{timestamp_line}\n{normalized_payload}\n{SEPARATOR_LINE}\n"

        existing_text = ""
        if destination_path.exists():
            existing_text = destination_path.read_text(encoding="utf-8", errors="replace")

        combined_text = entry_text
        if existing_text:
            combined_text = f"{entry_text}\n{existing_text.lstrip()}"

        self._write_atomically(destination_path, combined_text)

    def _normalize_payload(self, payload_text):
        """Normalize the incoming text for predictable storage.

        This removes zero bytes, unifies line endings, and trims empty outer
        whitespace without touching meaningful inner spacing.
        """
        clean_text = str(payload_text).replace("\x00", "")
        clean_text = clean_text.replace("\r\n", "\n").replace("\r", "\n")
        clean_text = clean_text.strip()
        return clean_text

    def _build_timestamp_line(self):
        """Return a UTC timestamp in the format requested by the project."""
        current_utc_time = datetime.now(timezone.utc)
        return current_utc_time.strftime("%d-%m-%Y %H%MZ:")

    def _write_atomically(self, destination_path, text_content):
        """Write the final content through a temporary file and replace step.

        This reduces the risk of ending up with a partially written capture file
        if the process is interrupted during a write.
        """
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=False,
            dir=str(destination_path.parent),
            suffix=".tmp",
        ) as temporary_file:
            temporary_file.write(text_content)
            temporary_file_path = Path(temporary_file.name)

        temporary_file_path.replace(destination_path)
