"""Tkinter widgets and UI behavior for the downloader window."""

import os
import queue
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from src.download_message import DownloadMessage
from src.download_options import DownloadOptions
from src.download_worker import DownloadWorker


class MainWindow:
    """Main Tkinter interface for collecting input and showing progress."""

    def __init__(self, root: tk.Tk) -> None:
        self.root: tk.Tk = root
        self.url_var: tk.StringVar = tk.StringVar()
        self.directory_var: tk.StringVar = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.audio_only_var: tk.BooleanVar = tk.BooleanVar(value=False)
        self.status_var: tk.StringVar = tk.StringVar(value="Ready.")
        self.worker: Optional[DownloadWorker] = None

        self.progress_bar: ttk.Progressbar
        self.download_button: ttk.Button
        self.log_text: tk.Text

        self._configure_style()
        self._build_widgets()

    def _configure_style(self) -> None:
        """Configure ttk styles used by the interface."""
        style: ttk.Style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f4f0e8")
        style.configure("Title.TLabel", background="#f4f0e8", foreground="#23313d", font=("Georgia", 22, "bold"))
        style.configure("Body.TLabel", background="#f4f0e8", foreground="#23313d", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"))
        style.configure("TCheckbutton", background="#f4f0e8", foreground="#23313d", font=("Segoe UI", 10))

    def _build_widgets(self) -> None:
        """Create and place all UI widgets."""
        container: ttk.Frame = ttk.Frame(self.root, padding=24)
        container.pack(fill=tk.BOTH, expand=True)

        title: ttk.Label = ttk.Label(
            container,
            text="YouTube Downloader",
            style="Title.TLabel",
        )
        title.pack(anchor=tk.W)

        subtitle: ttk.Label = ttk.Label(
            container,
            text="Paste a video link, choose an output folder, and download with automatic fallback methods.",
            style="Body.TLabel",
        )
        subtitle.pack(anchor=tk.W, pady=(6, 22))

        url_label: ttk.Label = ttk.Label(container, text="Video URL", style="Body.TLabel")
        url_label.pack(anchor=tk.W)

        url_entry: ttk.Entry = ttk.Entry(container, textvariable=self.url_var, font=("Segoe UI", 11))
        url_entry.pack(fill=tk.X, pady=(4, 14))
        url_entry.focus_set()

        folder_label: ttk.Label = ttk.Label(container, text="Output folder", style="Body.TLabel")
        folder_label.pack(anchor=tk.W)

        folder_row: ttk.Frame = ttk.Frame(container)
        folder_row.pack(fill=tk.X, pady=(4, 14))

        folder_entry: ttk.Entry = ttk.Entry(folder_row, textvariable=self.directory_var, font=("Segoe UI", 10))
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        browse_button: ttk.Button = ttk.Button(folder_row, text="Browse", command=self._choose_directory)
        browse_button.pack(side=tk.LEFT, padx=(8, 0))

        audio_check: ttk.Checkbutton = ttk.Checkbutton(
            container,
            text="Download audio only as MP3 when FFmpeg is available",
            variable=self.audio_only_var,
        )
        audio_check.pack(anchor=tk.W, pady=(0, 18))

        self.download_button = ttk.Button(
            container,
            text="Start Download",
            style="Accent.TButton",
            command=self._start_download,
        )
        self.download_button.pack(anchor=tk.W)

        self.progress_bar = ttk.Progressbar(container, maximum=100, mode="determinate")
        self.progress_bar.pack(fill=tk.X, pady=(20, 8))

        status_label: ttk.Label = ttk.Label(container, textvariable=self.status_var, style="Body.TLabel")
        status_label.pack(anchor=tk.W)

        self.log_text = tk.Text(
            container,
            height=12,
            wrap=tk.WORD,
            bg="#fffaf0",
            fg="#23313d",
            insertbackground="#23313d",
            relief=tk.FLAT,
            font=("Consolas", 10),
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(14, 0))
        self.log_text.configure(state=tk.DISABLED)

    def _choose_directory(self) -> None:
        """Let the user select a target download directory."""
        selected_directory: str = filedialog.askdirectory(initialdir=self.directory_var.get())

        if selected_directory:
            self.directory_var.set(selected_directory)

    def _start_download(self) -> None:
        """Validate input and start a background download."""
        url: str = self.url_var.get().strip()
        directory: str = self.directory_var.get().strip()

        if not url:
            messagebox.showerror("Missing URL", "Paste a YouTube video URL first.")
            return

        if not directory:
            messagebox.showerror("Missing Folder", "Choose an output folder first.")
            return

        if not os.path.isdir(directory):
            messagebox.showerror("Invalid Folder", "The selected output folder does not exist.")
            return

        options: DownloadOptions = DownloadOptions(
            url=url,
            output_directory=directory,
            audio_only=self.audio_only_var.get(),
        )
        self.worker = DownloadWorker(options)
        self.worker.start()

        self.progress_bar["value"] = 0
        self.download_button.configure(state=tk.DISABLED)
        self._set_status("Starting download.")
        self._append_log(f"Queued URL: {url}")
        self.root.after(150, self._poll_worker)

    def _poll_worker(self) -> None:
        """Read worker messages and update the interface."""
        if self.worker is None:
            return

        while True:
            try:
                message: DownloadMessage = self.worker.messages.get_nowait()
            except queue.Empty:
                break

            self._handle_worker_message(message)

        if self.worker.is_running():
            self.root.after(150, self._poll_worker)
        else:
            self.download_button.configure(state=tk.NORMAL)

    def _handle_worker_message(self, message: DownloadMessage) -> None:
        """Apply one worker event to the visible UI."""
        if message.kind in {"status", "progress", "complete"}:
            self._set_status(message.text)

        if message.progress > 0:
            self.progress_bar["value"] = message.progress

        if message.kind == "error":
            self._set_status("Download failed.")
            self._append_log(message.text)
            messagebox.showerror("Download failed", message.text)
        elif message.kind == "complete":
            self.progress_bar["value"] = 100
            self._append_log(message.text)
            messagebox.showinfo("Download complete", message.text)
        else:
            self._append_log(message.text)

    def _set_status(self, text: str) -> None:
        """Update the status label."""
        self.status_var.set(text)

    def _append_log(self, text: str) -> None:
        """Append one line to the read-only log box."""
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{text}\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)
