"""Music loading, timing, and preview playback helpers."""

import subprocess
import tempfile
import winsound
from pathlib import Path
from typing import Optional

from mutagen import File as MutagenFile

from src.services.ffmpeg_service import FFmpegService


class MusicService:
    """Handle music metadata and lightweight preview playback."""

    def __init__(self, ffmpeg_service: FFmpegService) -> None:
        """Initialize runtime state for optional preview playback."""
        self.ffmpeg_service = ffmpeg_service
        self._current_music_path: Optional[Path] = None
        self._temp_preview_file: Optional[Path] = None

    def get_audio_duration_seconds(self, audio_path: Path) -> float:
        """Read the audio duration in seconds using mutagen metadata."""
        metadata = MutagenFile(str(audio_path))
        if metadata is None or metadata.info is None or metadata.info.length is None:
            raise RuntimeError(f"Unable to read duration from audio file: {audio_path}")
        return float(metadata.info.length)

    def load_music(self, audio_path: Path) -> None:
        """Store the current music file."""
        self._current_music_path = audio_path

    def stop_preview(self) -> None:
        """Stop preview playback if running."""
        winsound.PlaySound(None, winsound.SND_PURGE)

    def play_preview_segment(self, audio_path: Path, clip_in_seconds: float, clip_out_seconds: float) -> None:
        """Preview a selected segment of audio.

        The selected interval is first decoded into a temporary WAV file with
        FFmpeg. The WAV is then played asynchronously through the built-in
        Windows winsound module.
        """
        ffmpeg_path = self.ffmpeg_service.get_ffmpeg_path()
        if not ffmpeg_path:
            raise RuntimeError("FFmpeg is required for audio preview.")

        segment_duration_seconds = max(0.0, clip_out_seconds - clip_in_seconds)
        if segment_duration_seconds <= 0:
            raise RuntimeError("Preview segment duration must be greater than zero.")

        self.stop_preview()

        temporary_preview_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temporary_preview_file.close()
        self._temp_preview_file = Path(temporary_preview_file.name)

        command = [
            ffmpeg_path,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            f"{max(0.0, clip_in_seconds):.3f}",
            "-t",
            f"{segment_duration_seconds:.3f}",
            "-i",
            str(audio_path),
            str(self._temp_preview_file),
        ]

        completed_process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            env=self.ffmpeg_service.build_environment(),
        )
        if completed_process.returncode != 0:
            raise RuntimeError(completed_process.stderr.strip() or "FFmpeg failed to prepare the audio preview.")

        winsound.PlaySound(str(self._temp_preview_file), winsound.SND_FILENAME | winsound.SND_ASYNC)
