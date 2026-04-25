"""Application bootstrap and top-level window configuration."""

import tkinter as tk
from typing import Optional

from src.main_window import MainWindow


class App:
    """Owns the Tk root instance and starts the event loop."""

    def __init__(self) -> None:
        self.root: tk.Tk = tk.Tk()
        self.window: Optional[MainWindow] = None
        self._configure_root()

    def _configure_root(self) -> None:
        """Apply root window settings before widgets are created."""
        self.root.title("YouTube Downloader")
        self.root.geometry("760x560")
        self.root.minsize(680, 500)

    def run(self) -> None:
        """Create the main window and enter Tk's main loop."""
        self.window = MainWindow(self.root)
        self.root.mainloop()
