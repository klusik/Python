"""Tkinter settings window.

The window intentionally stays small and simple. It provides only the settings
needed by the project plus a status line so the user can quickly verify whether
printing capture is active.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .constants import APP_NAME, WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH


class MainWindow:
    """Small Tkinter settings window shown from the tray icon."""

    def __init__(self, root_window, on_save_settings, on_request_hide, on_request_quit):
        """Build the full interface and store command callbacks."""
        self.root_window = root_window
        self.on_save_settings = on_save_settings
        self.on_request_hide = on_request_hide
        self.on_request_quit = on_request_quit

        self.run_after_windows_start_var = tk.BooleanVar(value=False)
        self.output_file_path_var = tk.StringVar(value="")
        self.status_text_var = tk.StringVar(value="Starting...")

        self._configure_window()
        self._build_widgets()
        self._bind_events()

    def set_settings(self, settings):
        """Load settings into the visible form controls."""
        self.run_after_windows_start_var.set(bool(settings.get("run_after_windows_start", False)))
        self.output_file_path_var.set(str(settings.get("output_file_path", "")))

    def get_settings(self):
        """Return the current form values as a settings dictionary."""
        return {
            "run_after_windows_start": bool(self.run_after_windows_start_var.get()),
            "output_file_path": self.output_file_path_var.get().strip(),
        }

    def set_status_text(self, status_text):
        """Update the status line at the bottom of the window."""
        self.status_text_var.set(status_text)

    def show(self):
        """Show the window and bring it to the foreground."""
        self.root_window.deiconify()
        self.root_window.lift()
        self.root_window.focus_force()

    def hide(self):
        """Hide the window while keeping the process alive in the tray."""
        self.root_window.withdraw()

    def _configure_window(self):
        """Apply title, size limits, and basic layout settings."""
        self.root_window.title(APP_NAME)
        self.root_window.geometry("680x280")
        self.root_window.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.root_window.columnconfigure(0, weight=1)
        self.root_window.rowconfigure(0, weight=1)

    def _build_widgets(self):
        """Create the interface widgets.

        The design stays intentionally plain because the utility is meant to be
        configuration-light and primarily tray-driven.
        """
        outer_frame = ttk.Frame(self.root_window, padding=16)
        outer_frame.grid(row=0, column=0, sticky="nsew")
        outer_frame.columnconfigure(1, weight=1)

        title_label = ttk.Label(
            outer_frame,
            text="ACARS Virtual Printer",
            font=("Segoe UI", 13, "bold"),
        )
        title_label.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        description_label = ttk.Label(
            outer_frame,
            text=(
                "This app listens on 127.0.0.1:9100 and stores plain-text print jobs "
                "from the Windows Generic / Text Only printer into a TXT file."
            ),
            wraplength=620,
            justify="left",
        )
        description_label.grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 16))

        startup_checkbutton = ttk.Checkbutton(
            outer_frame,
            text="Run after Windows start",
            variable=self.run_after_windows_start_var,
        )
        startup_checkbutton.grid(row=2, column=0, columnspan=3, sticky="w", pady=(0, 14))

        output_label = ttk.Label(outer_frame, text="Output TXT file")
        output_label.grid(row=3, column=0, sticky="w", pady=(0, 6))

        output_entry = ttk.Entry(outer_frame, textvariable=self.output_file_path_var)
        output_entry.grid(row=4, column=0, columnspan=2, sticky="ew", padx=(0, 8))

        browse_button = ttk.Button(outer_frame, text="Browse", command=self._browse_output_file)
        browse_button.grid(row=4, column=2, sticky="ew")

        instructions_label = ttk.Label(
            outer_frame,
            text=(
                "Use setup_printer.ps1 once to create the Windows printer. "
                "Close or minimize keeps the app in the tray. Right-click the tray icon to quit."
            ),
            wraplength=620,
            justify="left",
        )
        instructions_label.grid(row=5, column=0, columnspan=3, sticky="w", pady=(16, 12))

        actions_frame = ttk.Frame(outer_frame)
        actions_frame.grid(row=6, column=0, columnspan=3, sticky="ew")
        actions_frame.columnconfigure(0, weight=1)

        save_button = ttk.Button(actions_frame, text="Save settings", command=self._handle_save)
        save_button.grid(row=0, column=1, sticky="e")

        hide_button = ttk.Button(actions_frame, text="Hide to tray", command=self.on_request_hide)
        hide_button.grid(row=0, column=2, sticky="e", padx=(8, 0))

        quit_button = ttk.Button(actions_frame, text="Quit", command=self.on_request_quit)
        quit_button.grid(row=0, column=3, sticky="e", padx=(8, 0))

        status_frame = ttk.Frame(outer_frame)
        status_frame.grid(row=7, column=0, columnspan=3, sticky="ew", pady=(18, 0))
        status_frame.columnconfigure(0, weight=1)

        status_label = ttk.Label(status_frame, textvariable=self.status_text_var, relief="sunken", anchor="w")
        status_label.grid(row=0, column=0, sticky="ew")

    def _bind_events(self):
        """Attach standard window events.

        Close and minimize are redirected to tray behavior instead of exiting.
        """
        self.root_window.protocol("WM_DELETE_WINDOW", self.on_request_hide)
        self.root_window.bind("<Unmap>", self._handle_window_unmap)

    def _browse_output_file(self):
        """Let the user choose the TXT destination file."""
        selected_file_path = filedialog.asksaveasfilename(
            title="Select output TXT file",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="acars_log.txt",
        )
        if selected_file_path:
            self.output_file_path_var.set(selected_file_path)

    def _handle_save(self):
        """Validate and forward the settings to the application layer."""
        settings = self.get_settings()
        if not settings["output_file_path"]:
            messagebox.showerror(APP_NAME, "Please choose an output TXT file.")
            return

        try:
            self.on_save_settings(settings)
        except Exception as error:
            messagebox.showerror(APP_NAME, str(error))
            return

        messagebox.showinfo(APP_NAME, "Settings saved.")

    def _handle_window_unmap(self, event):
        """Redirect minimization to tray behavior.

        Tkinter emits <Unmap> for several state changes, so the additional iconify
        state check avoids hiding the window during unrelated updates.
        """
        if event.widget is self.root_window and self.root_window.state() == "iconic":
            self.on_request_hide()
