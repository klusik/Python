"""Dataclasses describing the current reel export configuration."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class FrameSettings:
    """Visual frame settings applied around each image cell."""

    enabled: bool = True
    color_hex: str = "#FFFFFF"
    thickness_pixels: int = 12
    margin_pixels: int = 5
    corner_style: str = "rounded"
    corner_radius_pixels: int = 28


@dataclass
class AudioSettings:
    """Music configuration and timeline behavior for the export."""

    music_path: Optional[Path] = None
    use_full_track: bool = False
    use_selected_segment: bool = False
    manual_timing: bool = True
    clip_in_seconds: float = 0.0
    clip_out_seconds: float = 0.0


@dataclass
class ExportSettings:
    """Main export parameters controlling layout, timing, and output."""

    photos_per_screen: int = 3
    screen_duration_seconds: float = 1.0
    frames_per_second: int = 30
    output_width_pixels: int = 1080
    output_height_pixels: int = 1920
    prefer_gpu_encoding: bool = True
    output_path: Optional[Path] = None
