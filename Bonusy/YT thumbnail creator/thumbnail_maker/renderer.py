"""Image rendering helpers for the thumbnail maker application."""

from pathlib import Path
from typing import Optional

from PIL import Image, ImageColor, ImageDraw, ImageFont

from . import config


class ThumbnailRenderer:
    """Render title and subtitle text over a background image."""

    def __init__(self) -> None:
        """Initialize the renderer and load a usable font set."""
        self.font_candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/ARIALBD.TTF",
            "/Library/Fonts/Arial Bold.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        ]

    def render(
        self,
        background_path: str,
        title_text: str,
        subtitle_text: str,
        title_size: int,
        subtitle_size: int,
        title_x_ratio: float,
        subtitle_x_ratio: float,
        title_y_ratio: float = config.DEFAULT_TITLE_Y_RATIO,
        subtitle_y_ratio: float = config.DEFAULT_SUBTITLE_Y_RATIO,
        overlay_opacity: int = config.DEFAULT_OVERLAY_OPACITY,
        overlay_height_ratio: float = config.DEFAULT_OVERLAY_HEIGHT_RATIO,
        overlay_start_ratio: float = config.DEFAULT_OVERLAY_START_RATIO,
        subtitle_color: str = config.DEFAULT_SUBTITLE_COLOR,
    ) -> Image.Image:
        """Return a rendered thumbnail image.

        Args:
            background_path: Path to the source image.
            title_text: Top title text.
            subtitle_text: Bottom subtitle text.
            title_size: Font size in pixels for the top title.
            subtitle_size: Font size in pixels for the bottom subtitle.
            title_x_ratio: Horizontal anchor for title, from 0.0 to 1.0.
            subtitle_x_ratio: Horizontal anchor for subtitle, from 0.0 to 1.0.
            title_y_ratio: Vertical anchor for title, from 0.0 to 1.0.
            subtitle_y_ratio: Vertical anchor for subtitle, from 0.0 to 1.0.
            overlay_opacity: Maximum black overlay opacity under the text area.
            overlay_height_ratio: Height of the bottom readability overlay.
            overlay_start_ratio: Where the bottom overlay starts.
            subtitle_color: Fill color for the subtitle text.
        """
        base_image = Image.open(background_path).convert("RGBA")
        width, height = base_image.size

        composed_image = self._apply_bottom_overlay(
            image=base_image,
            overlay_opacity=overlay_opacity,
            overlay_height_ratio=overlay_height_ratio,
            overlay_start_ratio=overlay_start_ratio,
        )

        draw = ImageDraw.Draw(composed_image)
        title_font = self._load_font(title_size)
        subtitle_font = self._load_font(subtitle_size)

        if title_text.strip():
            title_position = self._calculate_text_position(
                draw=draw,
                text=title_text,
                font=title_font,
                image_width=width,
                x_ratio=title_x_ratio,
                y_ratio=title_y_ratio,
            )
            self._draw_stroked_text(
                draw=draw,
                position=title_position,
                text=title_text,
                font=title_font,
                fill_color=config.DEFAULT_TEXT_COLOR,
                stroke_color=config.DEFAULT_STROKE_COLOR,
                stroke_width=config.DEFAULT_STROKE_WIDTH,
            )

        if subtitle_text.strip():
            subtitle_position = self._calculate_text_position(
                draw=draw,
                text=subtitle_text,
                font=subtitle_font,
                image_width=width,
                x_ratio=subtitle_x_ratio,
                y_ratio=subtitle_y_ratio,
            )
            self._draw_stroked_text(
                draw=draw,
                position=subtitle_position,
                text=subtitle_text,
                font=subtitle_font,
                fill_color=subtitle_color,
                stroke_color=config.DEFAULT_STROKE_COLOR,
                stroke_width=config.DEFAULT_STROKE_WIDTH,
            )

        return composed_image.convert("RGB")

    def save_both_formats(self, image: Image.Image, output_base_path: str) -> tuple[str, str]:
        """Save the rendered image as PNG and JPG, then return both paths."""
        output_path = Path(output_base_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        png_path = str(output_path.with_suffix(".png"))
        jpg_path = str(output_path.with_suffix(".jpg"))

        image.save(png_path, format="PNG")
        image.save(jpg_path, format="JPEG", quality=95, optimize=True)
        return png_path, jpg_path

    def _load_font(self, font_size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        """Load a bold font or fall back to PIL default if needed."""
        for font_path in self.font_candidates:
            if Path(font_path).exists():
                try:
                    return ImageFont.truetype(font_path, font_size)
                except OSError:
                    continue
        return ImageFont.load_default()

    def _apply_bottom_overlay(
        self,
        image: Image.Image,
        overlay_opacity: int,
        overlay_height_ratio: float,
        overlay_start_ratio: float,
    ) -> Image.Image:
        """Apply a vertical gradient overlay to improve text readability."""
        width, height = image.size
        overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)

        overlay_start_y = max(0, min(height - 1, int(height * overlay_start_ratio)))
        overlay_end_y = max(overlay_start_y + 1, min(height, int(height * (overlay_start_ratio + overlay_height_ratio))))
        overlay_height = max(1, overlay_end_y - overlay_start_y)

        for y_coordinate in range(overlay_start_y, overlay_end_y):
            progress = (y_coordinate - overlay_start_y) / overlay_height
            alpha = int(overlay_opacity * progress)
            overlay_draw.line(
                [(0, y_coordinate), (width, y_coordinate)],
                fill=(0, 0, 0, alpha),
            )

        return Image.alpha_composite(image, overlay)

    def _calculate_text_position(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
        image_width: int,
        x_ratio: float,
        y_ratio: float,
    ) -> tuple[int, int]:
        """Calculate a horizontally centered text position around a ratio anchor."""
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        text_width = right - left
        x_center = int(image_width * x_ratio)
        x_position = x_center - text_width // 2
        y_position = int(draw.im.size[1] * y_ratio)
        return x_position, y_position

    def _draw_stroked_text(
        self,
        draw: ImageDraw.ImageDraw,
        position: tuple[int, int],
        text: str,
        font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
        fill_color: str,
        stroke_color: str,
        stroke_width: int,
    ) -> None:
        """Draw thick, readable text with a manual outline."""
        stroke_rgb = ImageColor.getrgb(stroke_color)
        fill_rgb = ImageColor.getrgb(fill_color)
        x_position, y_position = position

        for offset_x in range(-stroke_width, stroke_width + 1):
            for offset_y in range(-stroke_width, stroke_width + 1):
                if offset_x * offset_x + offset_y * offset_y <= stroke_width * stroke_width:
                    draw.text(
                        (x_position + offset_x, y_position + offset_y),
                        text,
                        font=font,
                        fill=stroke_rgb,
                    )

        draw.text((x_position, y_position), text, font=font, fill=fill_rgb)
