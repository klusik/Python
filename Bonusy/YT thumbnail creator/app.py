"""Application entry point for the YouTube thumbnail maker.

This file intentionally stays very small.

Design note:
The executable entry point is separated from the UI implementation so the GUI
class can remain importable without immediately starting the Tkinter event loop.
That keeps the project easier to package, test, and reason about.
"""

from thumbnail_maker.gui import ThumbnailMakerApp


if __name__ == "__main__":
    application = ThumbnailMakerApp()
    application.run()
