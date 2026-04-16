"""FFmpeg discovery and capability helpers."""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional

import imageio_ffmpeg


class FFmpegService:
    """Provide FFmpeg executable discovery and encoder feature checks."""

    def __init__(self) -> None:
        """Resolve the best FFmpeg executable available on the system."""
        self.ffmpeg_path = self._discover_ffmpeg_path()
        self.ffplay_path = self._discover_ffplay_path()

    def _discover_ffmpeg_path(self) -> str:
        """Return a usable FFmpeg executable path.

        The bundled binary from imageio-ffmpeg is preferred because it makes the
        project easy to run on machines that do not already have FFmpeg in PATH.
        A PATH-installed binary is used as a fallback when necessary.
        """
        try:
            return imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            system_ffmpeg_path = shutil.which("ffmpeg")
            if not system_ffmpeg_path:
                raise RuntimeError(
                    "FFmpeg was not found. Install dependencies with run.bat and try again."
                )
            return system_ffmpeg_path

    def _discover_ffplay_path(self) -> Optional[str]:
        """Return a usable FFplay executable path when available.

        imageio-ffmpeg typically bundles FFmpeg only, not FFplay. If FFplay is
        present next to a system FFmpeg installation or otherwise reachable in
        PATH, audio preview can use it. Preview is optional, so absence is not a
        fatal error.
        """
        ffmpeg_file_path = Path(self.ffmpeg_path).resolve()
        sibling_candidates = [ffmpeg_file_path.with_name("ffplay.exe"), ffmpeg_file_path.with_name("ffplay")]
        for candidate_path in sibling_candidates:
            if candidate_path.exists():
                return str(candidate_path)
        return shutil.which("ffplay")

    def get_ffmpeg_path(self) -> str:
        """Return the resolved FFmpeg executable path."""
        return self.ffmpeg_path

    def get_ffmpeg_directory(self) -> Path:
        """Return the directory containing the FFmpeg executable."""
        return Path(self.ffmpeg_path).resolve().parent

    def get_ffplay_path(self) -> Optional[str]:
        """Return the resolved FFplay executable path when available."""
        return self.ffplay_path

    def get_ffprobe_path(self) -> Optional[str]:
        """Return the sibling ffprobe path when it exists.

        The bundled imageio binary often ships together with ffprobe. When it is
        not present, callers can continue without ffprobe and rely on mutagen for
        music duration discovery.
        """
        ffmpeg_file_path = Path(self.ffmpeg_path).resolve()
        candidate_names = ["ffprobe.exe", "ffprobe"]
        for candidate_name in candidate_names:
            candidate_path = ffmpeg_file_path.with_name(candidate_name)
            if candidate_path.exists():
                return str(candidate_path)
        detected_path = shutil.which("ffprobe")
        return detected_path

    def supports_encoder(self, encoder_name: str) -> bool:
        """Check whether the local FFmpeg build exposes a named encoder."""
        completed_process = subprocess.run(
            [self.ffmpeg_path, "-hide_banner", "-encoders"],
            capture_output=True,
            text=True,
            check=False,
        )
        encoder_list_text = completed_process.stdout + completed_process.stderr
        return encoder_name in encoder_list_text

    def get_preferred_video_encoder(self, prefer_gpu_encoding: bool = True) -> str:
        """Return the preferred video encoder for export.

        The method prefers NVIDIA NVENC H.264 when requested and available,
        otherwise it uses libx264 for broad compatibility.
        """
        if prefer_gpu_encoding and self.supports_encoder("h264_nvenc"):
            return "h264_nvenc"
        return "libx264"

    def build_environment(self) -> dict:
        """Create a process environment that also exposes the FFmpeg folder in PATH."""
        process_environment = os.environ.copy()
        ffmpeg_directory = str(self.get_ffmpeg_directory())
        process_environment["PATH"] = ffmpeg_directory + os.pathsep + process_environment.get("PATH", "")
        return process_environment
