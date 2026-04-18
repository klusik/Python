"""Main application orchestration.

This module connects the Tkinter window, the tray icon, the TCP printer
receiver, the output writer, and the persistent settings store.
"""

import queue
import socket
import tkinter as tk
from tkinter import messagebox

from .constants import APP_NAME, DEFAULT_LISTEN_HOST, DEFAULT_LISTEN_PORT
from .file_writer import CapturedTextWriter
from .gui import MainWindow
from .server import PrintReceiverServer
from .settings_store import SettingsStore
from .startup import StartupManager
from .tray_icon import TrayIconController


class ACARSVirtualPrinterApp:
    """Top-level application controller."""

    def __init__(self):
        """Create services, load settings, and prepare the UI state."""
        self.settings_store = SettingsStore()
        self.startup_manager = StartupManager()
        self.captured_text_writer = CapturedTextWriter()
        self.has_saved_settings = self.settings_store.has_saved_settings()
        self.settings = self.settings_store.load()

        self.root_window = tk.Tk()
        self.root_window.withdraw()

        self.main_window = MainWindow(
            root_window=self.root_window,
            on_save_settings=self.save_settings,
            on_request_hide=self.hide_window,
            on_request_quit=self.quit_application,
        )
        self.main_window.set_settings(self.settings)

        self.tray_icon_controller = TrayIconController(
            on_show_window=self.show_window_from_tray,
            on_quit=self.quit_application,
        )

        self.print_events_queue = queue.Queue()
        self.print_receiver_server = PrintReceiverServer(
            host=DEFAULT_LISTEN_HOST,
            port=DEFAULT_LISTEN_PORT,
            on_text_received=self._enqueue_received_text,
        )

        self.is_quitting = False

    def run(self):
        """Start background services and enter the Tkinter event loop."""
        tray_started = False

        try:
            self.tray_icon_controller.start()
            tray_started = True
        except Exception as error:
            self.main_window.set_status_text(f"Tray icon failed to start: {error}")
            self.main_window.show()
            self.root_window.after(200, self._show_startup_error, error)

        try:
            self.print_receiver_server.start()
            self.main_window.set_status_text(
                f"Listening on {DEFAULT_LISTEN_HOST}:{DEFAULT_LISTEN_PORT}. Ready to capture ACARS text."
            )
        except OSError as error:
            self.main_window.set_status_text(
                f"Receiver failed to start on {DEFAULT_LISTEN_HOST}:{DEFAULT_LISTEN_PORT}: {error}"
            )
            self.main_window.show()
            self.root_window.after(200, self._show_startup_error, error)
        else:
            if tray_started and self.has_saved_settings:
                self.main_window.hide()
            else:
                self.main_window.show()

        self.root_window.after(250, self._process_print_events)
        self.root_window.mainloop()

    def save_settings(self, settings):
        """Persist settings and apply startup registration changes."""
        output_file_path = str(settings.get("output_file_path", "")).strip()
        if not output_file_path:
            raise ValueError("Please select an output TXT file.")

        run_after_windows_start = bool(settings.get("run_after_windows_start", False))

        self.startup_manager.set_enabled(run_after_windows_start)
        self.settings_store.save(settings)
        self.settings = dict(settings)
        self.main_window.set_status_text(
            f"Settings saved. Captured text will be written to: {output_file_path}"
        )

    def hide_window(self):
        """Hide the main window to keep the app in the tray."""
        self.main_window.hide()

    def show_window_from_tray(self):
        """Show the settings window when requested from the tray icon.

        pystray callbacks are not executed on the Tkinter UI thread, so the call
        is marshalled through `after` for thread-safe interaction with Tk.
        """
        self.root_window.after(0, self.main_window.show)

    def quit_application(self):
        """Stop all services and exit the process cleanly."""
        if self.is_quitting:
            return

        self.is_quitting = True
        self.print_receiver_server.stop()
        self.tray_icon_controller.stop()
        self.root_window.after(0, self.root_window.destroy)

    def _enqueue_received_text(self, received_text):
        """Push a new print payload into the Tkinter polling queue."""
        self.print_events_queue.put(received_text)

    def _process_print_events(self):
        """Consume queued print jobs and write them to the output file.

        The server receives data on worker threads, while Tkinter expects UI and
        related application updates on the main thread. This polling bridge keeps
        those responsibilities separated and predictable.
        """
        try:
            while True:
                received_text = self.print_events_queue.get_nowait()
                self.captured_text_writer.write_entry(self.settings["output_file_path"], received_text)
                self.main_window.set_status_text("Received text and saved it successfully.")
        except queue.Empty:
            pass
        except OSError as error:
            self.main_window.set_status_text(f"File write error: {error}")
        except Exception as error:
            self.main_window.set_status_text(f"Unexpected processing error: {error}")
        finally:
            if not self.is_quitting:
                self.root_window.after(250, self._process_print_events)

    def _show_startup_error(self, error):
        """Display a detailed startup error to the user."""
        detailed_message = self._build_receiver_error_message(error)
        messagebox.showerror(APP_NAME, detailed_message)

    def _build_receiver_error_message(self, error):
        """Return a more helpful explanation for common bind failures."""
        if isinstance(error, OSError) and getattr(error, "errno", None) in (48, 98, 10048):
            return (
                "The local print receiver could not start because TCP port 9100 is already in use.\n\n"
                "Stop the conflicting service or change the receiver port in the source code and in the Windows printer port configuration."
            )

        if isinstance(error, socket.error):
            return f"The local print receiver failed to start: {error}"

        return str(error)
