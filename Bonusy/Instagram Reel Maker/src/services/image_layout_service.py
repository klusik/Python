"""Image layout generation for stacked vertical reel screens."""

from pathlib import Path
from typing import Iterable, List

from PIL import Image, ImageColor, ImageDraw, ImageOps

from src.models.project_settings import FrameSettings


class ImageLayoutService:
    """Compose one vertical reel frame image from multiple source photos."""

    def build_screen_image(
        self,
        image_paths: Iterable[Path],
        output_width_pixels: int,
        output_height_pixels: int,
        frame_settings: FrameSettings,
        background_color_hex: str = "#111111",
    ) -> Image.Image:
        """Create a full vertical screen image with stacked photo cells.

        Each source photo is letterboxed into an equal-height cell. The layout is
        deterministic and easy to reason about, which keeps the tool simple.
        """
        source_image_paths = list(image_paths)
        if not source_image_paths:
            raise ValueError("At least one image is required to build a screen.")

        screen_image = Image.new(
            "RGB",
            (output_width_pixels, output_height_pixels),
            ImageColor.getrgb(background_color_hex),
        )

        photo_count = len(source_image_paths)
        cell_height_pixels = output_height_pixels // photo_count
        top_offset_pixels = 0

        for source_image_path in source_image_paths:
            composed_cell_image = self._build_cell_image(
                source_image_path=source_image_path,
                cell_width_pixels=output_width_pixels,
                cell_height_pixels=cell_height_pixels,
                frame_settings=frame_settings,
                background_color_hex=background_color_hex,
            )
            screen_image.paste(composed_cell_image, box=(0, top_offset_pixels))
            top_offset_pixels += cell_height_pixels

        return screen_image

    def _build_cell_image(
        self,
        source_image_path: Path,
        cell_width_pixels: int,
        cell_height_pixels: int,
        frame_settings: FrameSettings,
        background_color_hex: str,
    ) -> Image.Image:
        """Create one photo cell fitted into the target strip slot.

        The reserved outer margin is applied before the frame and before the
        photo fit. This keeps rounded frames inside the visible video area and
        keeps the image inside the frame.
        """
        base_cell_image = Image.new(
            "RGB",
            (cell_width_pixels, cell_height_pixels),
            ImageColor.getrgb(background_color_hex),
        )

        outer_margin_pixels = max(0, frame_settings.margin_pixels if frame_settings.enabled else 0)
        frame_thickness_pixels = max(0, frame_settings.thickness_pixels if frame_settings.enabled else 0)

        available_width_pixels = max(1, cell_width_pixels - outer_margin_pixels * 2)
        available_height_pixels = max(1, cell_height_pixels - outer_margin_pixels * 2)

        inner_photo_fit_width_pixels = max(1, available_width_pixels - frame_thickness_pixels * 2)
        inner_photo_fit_height_pixels = max(1, available_height_pixels - frame_thickness_pixels * 2)

        with Image.open(source_image_path) as source_image:
            source_rgb_image = source_image.convert("RGB")
            scaled_image = ImageOps.contain(
                source_rgb_image,
                (inner_photo_fit_width_pixels, inner_photo_fit_height_pixels),
            )

        if frame_settings.enabled:
            framed_image = self._apply_frame(scaled_image, frame_settings)
            paste_x_pixels = (cell_width_pixels - framed_image.width) // 2
            paste_y_pixels = (cell_height_pixels - framed_image.height) // 2
            base_cell_image.paste(
                framed_image,
                (paste_x_pixels, paste_y_pixels),
                mask=framed_image.split()[-1],
            )
        else:
            paste_x_pixels = (cell_width_pixels - scaled_image.width) // 2
            paste_y_pixels = (cell_height_pixels - scaled_image.height) // 2
            base_cell_image.paste(scaled_image, (paste_x_pixels, paste_y_pixels))

        return base_cell_image

    def _apply_frame(self, source_image: Image.Image, frame_settings: FrameSettings) -> Image.Image:
        """Wrap the source image in a simple configurable border.

        Rounded corners use an alpha mask so the result pastes cleanly onto the
        screen background.
        """
        frame_thickness_pixels = max(0, frame_settings.thickness_pixels)
        outer_margin_pixels = max(0, frame_settings.margin_pixels)

        framed_width_pixels = source_image.width + frame_thickness_pixels * 2 + outer_margin_pixels * 2
        framed_height_pixels = source_image.height + frame_thickness_pixels * 2 + outer_margin_pixels * 2
        frame_rgba_image = Image.new("RGBA", (framed_width_pixels, framed_height_pixels), (0, 0, 0, 0))
        frame_drawer = ImageDraw.Draw(frame_rgba_image)
        frame_color_rgba = ImageColor.getrgb(frame_settings.color_hex) + (255,)

        frame_left_pixels = outer_margin_pixels
        frame_top_pixels = outer_margin_pixels
        frame_right_pixels = framed_width_pixels - outer_margin_pixels - 1
        frame_bottom_pixels = framed_height_pixels - outer_margin_pixels - 1
        frame_rectangle = [frame_left_pixels, frame_top_pixels, frame_right_pixels, frame_bottom_pixels]

        if frame_settings.corner_style == "rounded":
            frame_drawer.rounded_rectangle(
                frame_rectangle,
                radius=max(0, frame_settings.corner_radius_pixels),
                fill=frame_color_rgba,
            )
        else:
            frame_drawer.rectangle(frame_rectangle, fill=frame_color_rgba)

        source_rgba_image = source_image.convert("RGBA")
        paste_position = (
            outer_margin_pixels + frame_thickness_pixels,
            outer_margin_pixels + frame_thickness_pixels,
        )

        if frame_settings.corner_style == "rounded":
            image_mask = Image.new("L", source_rgba_image.size, 0)
            image_mask_drawer = ImageDraw.Draw(image_mask)
            inner_radius_pixels = max(0, frame_settings.corner_radius_pixels - frame_thickness_pixels)
            image_mask_drawer.rounded_rectangle(
                [0, 0, source_rgba_image.width - 1, source_rgba_image.height - 1],
                radius=inner_radius_pixels,
                fill=255,
            )
            source_rgba_image.putalpha(image_mask)

        frame_rgba_image.paste(source_rgba_image, paste_position, source_rgba_image)
        return frame_rgba_image

    def split_images_into_groups(self, image_paths: List[Path], photos_per_screen: int) -> List[List[Path]]:
        """Split source image paths into consecutive screen groups."""
        safe_group_size = max(1, photos_per_screen)
        grouped_image_paths: List[List[Path]] = []
        for start_index in range(0, len(image_paths), safe_group_size):
            grouped_image_paths.append(image_paths[start_index:start_index + safe_group_size])
        return grouped_image_paths
