"""Application entry point for the YouTube thumbnail maker."""

from thumbnail_maker.gui import ThumbnailMakerApp


if __name__ == "__main__":
    app = ThumbnailMakerApp()
    app.run()
