"""Tray icon image factory."""

from PIL import Image, ImageDraw


class IconFactory:
    """Create simple in-memory icons for the tray application."""

    def build_tray_icon(self):
        """Return a Pillow image used by pystray."""
        icon_size = 64
        icon_image = Image.new("RGBA", (icon_size, icon_size), (255, 255, 255, 0))
        image_draw = ImageDraw.Draw(icon_image)

        image_draw.rounded_rectangle((6, 6, 58, 58), radius=10, fill=(25, 118, 210, 255))
        image_draw.rectangle((18, 16, 46, 22), fill=(255, 255, 255, 255))
        image_draw.rectangle((18, 28, 46, 34), fill=(255, 255, 255, 255))
        image_draw.rectangle((18, 40, 38, 46), fill=(255, 255, 255, 255))

        return icon_image
