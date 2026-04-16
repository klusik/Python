"""End-to-end export pipeline for creating the final vertical MP4 reel."""

import math
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Iterable, List, Optional

from src.models.project_settings import AudioSettings, ExportSettings, FrameSettings
from src.services.ffmpeg_service import FFmpegService
from src.services.image_layout_service import ImageLayoutService
from src.services.music_service import MusicService


class ExportService:
    """Create temporary screen images and encode them into a final MP4 file."""

    def __init__(
        self,
        ffmpeg_service: FFmpegService,
        music_service: MusicService,
        image_layout_service: ImageLayoutService,
    ) -> None:
        """Store dependent services used during export."""
        self.ffmpeg_service = ffmpeg_service
        self.music_service = music_service
        self.image_layout_service = image_layout_service

    def compute_screen_duration_seconds(
        self,
        image_count: int,
        export_settings: ExportSettings,
        audio_settings: AudioSettings,
    ) -> float:
        """Compute the duration for one screen based on the selected timing mode."""
        if image_count <= 0:
            raise ValueError("At least one image is required for duration calculation.")

        screen_count = math.ceil(image_count / max(1, export_settings.photos_per_screen))

        if audio_settings.music_path and audio_settings.use_full_track:
            full_duration_seconds = self.music_service.get_audio_duration_seconds(audio_settings.music_path)
            return max(0.1, full_duration_seconds / screen_count)

        if audio_settings.music_path and audio_settings.use_selected_segment:
            segment_duration_seconds = max(0.0, audio_settings.clip_out_seconds - audio_settings.clip_in_seconds)
            return max(0.1, segment_duration_seconds / screen_count)

        return max(0.1, export_settings.screen_duration_seconds)

    def export_reel(
        self,
        image_paths: List[Path],
        frame_settings: FrameSettings,
        audio_settings: AudioSettings,
        export_settings: ExportSettings,
        status_callback,
    ) -> Path:
        """Build and encode the final reel file.

        The process uses temporary PNG screen images and a concat file because
        that keeps the slideshow timing deterministic and easy to inspect when
        users later want to adjust the project.
        """
        if not image_paths:
            raise ValueError("No images were selected for export.")
        if export_settings.output_path is None:
            raise ValueError("No output path was selected.")

        grouped_images = self.image_layout_service.split_images_into_groups(
            image_paths=image_paths,
            photos_per_screen=export_settings.photos_per_screen,
        )
        screen_duration_seconds = self.compute_screen_duration_seconds(
            image_count=len(image_paths),
            export_settings=export_settings,
            audio_settings=audio_settings,
        )

        with tempfile.TemporaryDirectory(prefix="reel_builder_") as temporary_directory_string:
            temporary_directory = Path(temporary_directory_string)
            screen_image_paths: List[Path] = []

            status_callback("Composing screen images...")
            for group_index, grouped_image_paths in enumerate(grouped_images, start=1):
                screen_image = self.image_layout_service.build_screen_image(
                    image_paths=grouped_image_paths,
                    output_width_pixels=export_settings.output_width_pixels,
                    output_height_pixels=export_settings.output_height_pixels,
                    frame_settings=frame_settings,
                )
                screen_image_path = temporary_directory / f"screen_{group_index:05d}.png"
                screen_image.save(screen_image_path)
                screen_image_paths.append(screen_image_path)
                status_callback(f"Composed screen {group_index} of {len(grouped_images)}")

            concat_file_path = temporary_directory / "screens.txt"
            self._write_concat_file(
                concat_file_path=concat_file_path,
                image_paths=screen_image_paths,
                screen_duration_seconds=screen_duration_seconds,
            )

            silent_video_path = temporary_directory / "silent_video.mp4"
            status_callback("Encoding slideshow video...")
            self._encode_silent_video(
                concat_file_path=concat_file_path,
                output_video_path=silent_video_path,
                export_settings=export_settings,
            )

            if audio_settings.music_path:
                status_callback("Muxing audio...")
                self._mux_audio(
                    silent_video_path=silent_video_path,
                    audio_settings=audio_settings,
                    export_settings=export_settings,
                )
            else:
                shutil.copy2(silent_video_path, export_settings.output_path)

            status_callback("Export finished.")
            return export_settings.output_path

    def _write_concat_file(
        self,
        concat_file_path: Path,
        image_paths: Iterable[Path],
        screen_duration_seconds: float,
    ) -> None:
        """Write an FFmpeg concat-demuxer manifest for still images."""
        image_path_list = list(image_paths)
        concat_lines = []
        for image_path in image_path_list:
            escaped_path = str(image_path).replace("'", r"'\\''")
            concat_lines.append(f"file '{escaped_path}'")
            concat_lines.append(f"duration {screen_duration_seconds:.6f}")

        if image_path_list:
            escaped_last_path = str(image_path_list[-1]).replace("'", r"'\\''")
            concat_lines.append(f"file '{escaped_last_path}'")

        concat_file_path.write_text("\n".join(concat_lines), encoding="utf-8")

    def _encode_silent_video(
        self,
        concat_file_path: Path,
        output_video_path: Path,
        export_settings: ExportSettings,
    ) -> None:
        """Encode the slideshow images into a silent vertical MP4."""
        video_encoder = self.ffmpeg_service.get_preferred_video_encoder(export_settings.prefer_gpu_encoding)
        ffmpeg_command = [
            self.ffmpeg_service.get_ffmpeg_path(),
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file_path),
            "-r",
            str(export_settings.frames_per_second),
            "-pix_fmt",
            "yuv420p",
            "-an",
            "-c:v",
            video_encoder,
        ]

        if video_encoder == "h264_nvenc":
            ffmpeg_command.extend(["-preset", "p4", "-cq", "23", "-movflags", "+faststart"])
        else:
            ffmpeg_command.extend(["-preset", "medium", "-crf", "20", "-movflags", "+faststart"])

        ffmpeg_command.append(str(output_video_path))

        completed_process = subprocess.run(
            ffmpeg_command,
            capture_output=True,
            text=True,
            check=False,
            env=self.ffmpeg_service.build_environment(),
        )
        if completed_process.returncode != 0:
            raise RuntimeError(completed_process.stderr.strip() or "FFmpeg failed to encode the video.")

    def _mux_audio(
        self,
        silent_video_path: Path,
        audio_settings: AudioSettings,
        export_settings: ExportSettings,
    ) -> None:
        """Trim optional audio and mux it with the slideshow video."""
        if audio_settings.music_path is None or export_settings.output_path is None:
            raise ValueError("Audio muxing requires both music and output path.")

        ffmpeg_command = [
            self.ffmpeg_service.get_ffmpeg_path(),
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(silent_video_path),
        ]

        if audio_settings.use_selected_segment:
            ffmpeg_command.extend([
                "-ss",
                f"{max(0.0, audio_settings.clip_in_seconds):.3f}",
                "-to",
                f"{max(audio_settings.clip_in_seconds, audio_settings.clip_out_seconds):.3f}",
            ])

        ffmpeg_command.extend([
            "-i",
            str(audio_settings.music_path),
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(export_settings.output_path),
        ])

        completed_process = subprocess.run(
            ffmpeg_command,
            capture_output=True,
            text=True,
            check=False,
            env=self.ffmpeg_service.build_environment(),
        )
        if completed_process.returncode != 0:
            raise RuntimeError(completed_process.stderr.strip() or "FFmpeg failed to mux the audio.")
