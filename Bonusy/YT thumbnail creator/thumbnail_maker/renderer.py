"""Rendering logic for the YouTube thumbnail maker application.

The renderer is intentionally independent from Tkinter. It only depends on
Pillow and plain Python values. That separation makes the rendering pipeline
reusable from a GUI, a script, or a future command-line wrapper.
"""

from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFont

from . import config


class ThumbnailRenderer:
    """Render title and subtitle text over a background image."""

    def __init__(self) -> None:
        """Initialize the renderer and load a usable font set.

        The renderer maintains a font candidate list instead of a single hardcoded
        font path so the app can work across Linux, Windows, and macOS without
        forcing the user to configure anything manually.
        """
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
        title_horizontal_ratio: float,
        subtitle_horizontal_ratio: float,
        title_vertical_ratio: float = config.DEFAULT_TITLE_VERTICAL_RATIO,
        subtitle_vertical_ratio: float = config.DEFAULT_SUBTITLE_VERTICAL_RATIO,
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
            title_horizontal_ratio: Horizontal anchor for title, from 0.0 to 1.0.
            subtitle_horizontal_ratio: Horizontal anchor for subtitle, from 0.0 to 1.0.
            title_vertical_ratio: Vertical anchor for title, from 0.0 to 1.0.
            subtitle_vertical_ratio: Vertical anchor for subtitle, from 0.0 to 1.0.
            overlay_opacity: Maximum black overlay opacity under the text area.
            overlay_height_ratio: Height of the bottom readability overlay.
            overlay_start_ratio: Where the bottom overlay starts.
            subtitle_color: Fill color for the subtitle text.
        """
        base_image = Image.open(background_path).convert("RGBA")
        image_width, image_height = base_image.size

        composed_image = self._apply_bottom_overlay(
            image=base_image,
            overlay_opacity=overlay_opacity,
            overlay_height_ratio=overlay_height_ratio,
            overlay_start_ratio=overlay_start_ratio,
        )

        drawing_context = ImageDraw.Draw(composed_image)
        title_font = self._load_font(title_size)
        subtitle_font = self._load_font(subtitle_size)

        if title_text.strip():
            title_position = self._calculate_text_position(
                drawing_context=drawing_context,
                text=title_text,
                font=title_font,
                image_width=image_width,
                image_height=image_height,
                horizontal_ratio=title_horizontal_ratio,
                vertical_ratio=title_vertical_ratio,
            )
            self._draw_stroked_text(
                drawing_context=drawing_context,
                position=title_position,
                text=title_text,
                font=title_font,
                fill_color=config.DEFAULT_TEXT_COLOR,
                stroke_color=config.DEFAULT_STROKE_COLOR,
                stroke_width=config.DEFAULT_STROKE_WIDTH,
            )

        if subtitle_text.strip():
            subtitle_position = self._calculate_text_position(
                drawing_context=drawing_context,
                text=subtitle_text,
                font=subtitle_font,
                image_width=image_width,
                image_height=image_height,
                horizontal_ratio=subtitle_horizontal_ratio,
                vertical_ratio=subtitle_vertical_ratio,
            )
            self._draw_stroked_text(
                drawing_context=drawing_context,
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

        png_output_path = str(output_path.with_suffix(".png"))
        jpg_output_path = str(output_path.with_suffix(".jpg"))

        image.save(png_output_path, format="PNG")
        image.save(jpg_output_path, format="JPEG", quality=95, optimize=True)
        return png_output_path, jpg_output_path

    def _load_font(self, font_size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        """Load a bold font or fall back to the Pillow default if needed."""
        for candidate_font_path in self.font_candidates:
            if Path(candidate_font_path).exists():
                try:
                    return ImageFont.truetype(candidate_font_path, font_size)
                except OSError:
                    # A font file may exist but still be unreadable or unsupported.
                    # In that case, the renderer continues with the next candidate.
                    continue
        return ImageFont.load_default()

    def _apply_bottom_overlay(
        self,
        image: Image.Image,
        overlay_opacity: int,
        overlay_height_ratio: float,
        overlay_start_ratio: float,
    ) -> Image.Image:
        """Apply a vertical gradient overlay to improve text readability.

        The overlay is rendered into a transparent RGBA image first and then
        composited over the background. That keeps the logic explicit and avoids
        mutating the original image in-place.
        """
        image_width, image_height = image.size
        overlay_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
        overlay_drawing_context = ImageDraw.Draw(overlay_image)

        overlay_start_pixel = max(0, min(image_height - 1, int(image_height * overlay_start_ratio)))
        overlay_end_pixel = max(
            overlay_start_pixel + 1,
            min(image_height, int(image_height * (overlay_start_ratio + overlay_height_ratio))),
        )
        overlay_pixel_height = max(1, overlay_end_pixel - overlay_start_pixel)

        for vertical_pixel in range(overlay_start_pixel, overlay_end_pixel):
            overlay_progress_ratio = (vertical_pixel - overlay_start_pixel) / overlay_pixel_height
            overlay_alpha = int(overlay_opacity * overlay_progress_ratio)
            overlay_drawing_context.line(
                [(0, vertical_pixel), (image_width, vertical_pixel)],
                fill=(0, 0, 0, overlay_alpha),
            )

        return Image.alpha_composite(image, overlay_image)

    def _calculate_text_position(
        self,
        drawing_context: ImageDraw.ImageDraw,
        text: str,
        font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
        image_width: int,
        image_height: int,
        horizontal_ratio: float,
        vertical_ratio: float,
    ) -> tuple[int, int]:
        """Calculate a horizontally centered text position around a ratio anchor.

        The horizontal ratio defines the center point for the rendered text. The
        method measures the actual text width so the visual center stays aligned
        regardless of title length.
        """
        left_edge, top_edge, right_edge, bottom_edge = drawing_context.textbbox(
            (0, 0),
            text,
            font=font,
        )
        text_width = right_edge - left_edge
        horizontal_center_pixel = int(image_width * horizontal_ratio)
        horizontal_position = horizontal_center_pixel - text_width // 2
        vertical_position = int(image_height * vertical_ratio)
        _unused_top_edge = top_edge
        _unused_bottom_edge = bottom_edge
        return horizontal_position, vertical_position

    def _draw_stroked_text(
        self,
        drawing_context: ImageDraw.ImageDraw,
        position: tuple[int, int],
        text: str,
        font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
        fill_color: str,
        stroke_color: str,
        stroke_width: int,
    ) -> None:
        """Draw thick, readable text with a manual outline.

        Pillow offers built-in stroke support in newer versions, but the manual
        outline keeps behavior explicit and predictable across environments.
        The circular distance check produces a softer outline than drawing the
        full square neighborhood.
        """
        stroke_rgb_color = ImageColor.getrgb(stroke_color)
        fill_rgb_color = ImageColor.getrgb(fill_color)
        horizontal_position, vertical_position = position

        for horizontal_offset in range(-stroke_width, stroke_width + 1):
            for vertical_offset in range(-stroke_width, stroke_width + 1):
                distance_squared = (
                    horizontal_offset * horizontal_offset
                    + vertical_offset * vertical_offset
                )
                if distance_squared <= stroke_width * stroke_width:
                    drawing_context.text(
                        (
                            horizontal_position + horizontal_offset,
                            vertical_position + vertical_offset,
                        ),
                        text,
                        font=font,
                        fill=stroke_rgb_color,
                    )

        drawing_context.text(
            (horizontal_position, vertical_position),
            text,
            font=font,
            fill=fill_rgb_color,
        )
