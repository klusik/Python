"""System tray integration based on pystray."""

import threading

import pystray

from .icon_factory import IconFactory


class TrayIconController:
    """Create and manage the tray icon and its menu."""

    def __init__(self, on_show_window, on_quit):
        """Store callbacks used by the tray menu."""
        self.on_show_window = on_show_window
        self.on_quit = on_quit
        self.icon = None
        self.icon_thread = None
        self.icon_factory = IconFactory()

    def start(self):
        """Start the tray icon in its own thread."""
        if self.icon is not None:
            return

        tray_image = self.icon_factory.build_tray_icon()
        tray_menu = pystray.Menu(
            pystray.MenuItem("Open", self._handle_open),
            pystray.MenuItem("Quit", self._handle_quit),
        )

        self.icon = pystray.Icon(
            name="acars_virtual_printer",
            title="ACARS Virtual Printer",
            icon=tray_image,
            menu=tray_menu,
        )
        self.icon.visible = True

        self.icon_thread = threading.Thread(target=self.icon.run, name="AVPTrayIcon", daemon=True)
        self.icon_thread.start()

    def stop(self):
        """Stop the tray icon."""
        if self.icon is None:
            return

        self.icon.stop()
        self.icon = None
        self.icon_thread = None

    def _handle_open(self, icon, item):
        """Forward the Open tray command to the application callback."""
        del icon, item
        self.on_show_window()

    def _handle_quit(self, icon, item):
        """Forward the Quit tray command to the application callback."""
        del icon, item
        self.on_quit()
