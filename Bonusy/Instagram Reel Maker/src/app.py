"""Application composition root for the Instagram Reel Builder."""

import tkinter as tk

from src.controllers.app_controller import AppController
from src.services.export_service import ExportService
from src.services.ffmpeg_service import FFmpegService
from src.services.image_layout_service import ImageLayoutService
from src.services.music_service import MusicService
from src.ui.main_window import MainWindow


class ReelBuilderApplication:
    """Construct and run the full desktop application."""

    def __init__(self) -> None:
        """Create the root window, services, controller, and user interface."""
        self.root = tk.Tk()
        self.root.title("Instagram Reel Builder")
        self.root.geometry("1220x860")
        self.root.minsize(1120, 760)

        self.ffmpeg_service = FFmpegService()
        self.music_service = MusicService(ffmpeg_service=self.ffmpeg_service)
        self.image_layout_service = ImageLayoutService()
        self.export_service = ExportService(
            ffmpeg_service=self.ffmpeg_service,
            music_service=self.music_service,
            image_layout_service=self.image_layout_service,
        )
        self.main_window = MainWindow(self.root)
        self.controller = AppController(
            root_window=self.root,
            main_window=self.main_window,
            export_service=self.export_service,
            music_service=self.music_service,
            ffmpeg_service=self.ffmpeg_service,
        )

    def run(self) -> None:
        """Start the Tkinter event loop."""
        self.root.mainloop()
