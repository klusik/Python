"""Tkinter user interface for the Inara Profile Downloader."""

from __future__ import annotations

import logging
import os
import queue
import subprocess
import sys
import threading
import tkinter as tkinter_module
import webbrowser
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from .api_client import InaraApiClient
from .configuration import ConfigurationRepository
from .constants import (
    APPLICATION_VERSION,
    INARA_API_DEVELOPER_GUIDE_URL,
    INARA_API_DOCUMENTATION_URL,
    INARA_API_SETTINGS_URL,
    MINIMUM_REQUEST_INTERVAL_SECONDS,
    WINDOW_MINIMUM_HEIGHT,
    WINDOW_MINIMUM_WIDTH,
    WINDOW_TITLE,
)
from .controller import ProfileDownloadController
from .exceptions import InaraProfileDownloaderError
from .exporter import ProfileExporter
from .logging_setup import configure_application_logging
from .models import ApiCredentials, ApplicationSettings, ProfileDownloadRequest, ProfileDownloadResult
from .rate_limiter import RequestRateLimiter


@dataclass(frozen=True, slots=True)
class WorkerOutcome:
    """Message transferred safely from the worker thread to the Tkinter thread.

    @param result: Successful profile-download result, when available.
    @param error_message: User-facing error text, when the operation failed.
    """

    result: ProfileDownloadResult | None
    error_message: str | None


class InaraProfileDownloaderApplication:
    """Main Tkinter application window and event coordinator.

    @param root_window: Tkinter root window owned by the launcher.
    @param controller: Application workflow controller.
    @param configuration_repository: Non-secret settings repository.
    @param application_logger: Configured application logger.
    @param log_file: Path displayed in the diagnostics tab.
    """

    def __init__(
        self,
        root_window: tkinter_module.Tk,
        controller: ProfileDownloadController,
        configuration_repository: ConfigurationRepository,
        application_logger: logging.Logger,
        log_file: Path,
    ) -> None:
        self._root_window = root_window
        self._controller = controller
        self._configuration_repository = configuration_repository
        self._application_logger = application_logger
        self._log_file = log_file
        self._worker_outcome_queue: queue.Queue[WorkerOutcome] = queue.Queue()
        self._download_in_progress = False
        self._last_output_file: Path | None = None

        self._api_key_variable = tkinter_module.StringVar()
        self._show_api_key_variable = tkinter_module.BooleanVar(value=False)
        self._registered_application_name_variable = tkinter_module.StringVar()
        self._commander_name_variable = tkinter_module.StringVar()
        self._commander_frontier_id_variable = tkinter_module.StringVar()
        self._output_directory_variable = tkinter_module.StringVar()
        self._development_mode_variable = tkinter_module.BooleanVar(value=True)
        self._status_variable = tkinter_module.StringVar(value="Ready.")
        self._profile_summary_variable = tkinter_module.StringVar(
            value="No profile has been downloaded during this session."
        )

        self._configure_window()
        self._create_widgets()
        self._load_non_secret_settings()
        self._root_window.after(150, self._poll_worker_outcomes)

    def _configure_window(self) -> None:
        """Apply stable window sizing and close behavior."""

        self._root_window.title(WINDOW_TITLE)
        self._root_window.minsize(WINDOW_MINIMUM_WIDTH, WINDOW_MINIMUM_HEIGHT)
        self._root_window.geometry("1040x760")
        self._root_window.protocol("WM_DELETE_WINDOW", self._handle_window_close)

    def _create_widgets(self) -> None:
        """Create all widgets and bind them to descriptive event handlers."""

        outer_frame = ttk.Frame(self._root_window, padding=16)
        outer_frame.pack(fill=tkinter_module.BOTH, expand=True)
        outer_frame.columnconfigure(0, weight=1)
        outer_frame.rowconfigure(2, weight=1)

        title_label = ttk.Label(
            outer_frame,
            text=f"Inara Profile Downloader {APPLICATION_VERSION}",
            font=("Segoe UI", 18, "bold"),
        )
        title_label.grid(row=0, column=0, sticky=tkinter_module.W)

        scope_warning = ttk.Label(
            outer_frame,
            text=(
                "Important: the official Inara read API returns only basic commander-profile data. "
                "It does not return materials, Odyssey inventory, the complete fleet, loadouts, "
                "stored modules, cargo, credits or engineer state."
            ),
            wraplength=980,
            justify=tkinter_module.LEFT,
        )
        scope_warning.grid(row=1, column=0, sticky=tkinter_module.EW, pady=(8, 14))

        notebook = ttk.Notebook(outer_frame)
        notebook.grid(row=2, column=0, sticky=tkinter_module.NSEW)

        download_tab = ttk.Frame(notebook, padding=16)
        scope_tab = ttk.Frame(notebook, padding=16)
        diagnostics_tab = ttk.Frame(notebook, padding=16)
        notebook.add(download_tab, text="Download")
        notebook.add(scope_tab, text="API scope")
        notebook.add(diagnostics_tab, text="Diagnostics")

        self._create_download_tab(download_tab)
        self._create_scope_tab(scope_tab)
        self._create_diagnostics_tab(diagnostics_tab)

        status_frame = ttk.Frame(outer_frame)
        status_frame.grid(row=3, column=0, sticky=tkinter_module.EW, pady=(12, 0))
        status_frame.columnconfigure(0, weight=1)
        ttk.Label(status_frame, textvariable=self._status_variable).grid(
            row=0,
            column=0,
            sticky=tkinter_module.W,
        )

        self._progress_bar = ttk.Progressbar(status_frame, mode="indeterminate", length=180)
        self._progress_bar.grid(row=0, column=1, sticky=tkinter_module.E)

    def _create_download_tab(self, parent_frame: ttk.Frame) -> None:
        """Create credentials, request and output controls.

        @param parent_frame: Notebook tab that owns the controls.
        """

        parent_frame.columnconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Personal Inara API key:").grid(
            row=0,
            column=0,
            sticky=tkinter_module.W,
            padx=(0, 12),
            pady=6,
        )
        self._api_key_entry = ttk.Entry(
            parent_frame,
            textvariable=self._api_key_variable,
            show="•",
        )
        self._api_key_entry.grid(row=0, column=1, sticky=tkinter_module.EW, pady=6)
        ttk.Checkbutton(
            parent_frame,
            text="Show",
            variable=self._show_api_key_variable,
            command=self._toggle_api_key_visibility,
        ).grid(row=0, column=2, sticky=tkinter_module.W, padx=(10, 0), pady=6)

        ttk.Label(parent_frame, text="Registered application name:").grid(
            row=1,
            column=0,
            sticky=tkinter_module.W,
            padx=(0, 12),
            pady=6,
        )
        ttk.Entry(
            parent_frame,
            textvariable=self._registered_application_name_variable,
        ).grid(row=1, column=1, columnspan=2, sticky=tkinter_module.EW, pady=6)

        ttk.Label(parent_frame, text="Commander name (optional):").grid(
            row=2,
            column=0,
            sticky=tkinter_module.W,
            padx=(0, 12),
            pady=6,
        )
        ttk.Entry(parent_frame, textvariable=self._commander_name_variable).grid(
            row=2,
            column=1,
            columnspan=2,
            sticky=tkinter_module.EW,
            pady=6,
        )

        ttk.Label(parent_frame, text="Frontier ID (optional):").grid(
            row=3,
            column=0,
            sticky=tkinter_module.W,
            padx=(0, 12),
            pady=6,
        )
        ttk.Entry(parent_frame, textvariable=self._commander_frontier_id_variable).grid(
            row=3,
            column=1,
            columnspan=2,
            sticky=tkinter_module.EW,
            pady=6,
        )

        ttk.Label(parent_frame, text="Output directory:").grid(
            row=4,
            column=0,
            sticky=tkinter_module.W,
            padx=(0, 12),
            pady=6,
        )
        ttk.Entry(parent_frame, textvariable=self._output_directory_variable).grid(
            row=4,
            column=1,
            sticky=tkinter_module.EW,
            pady=6,
        )
        ttk.Button(
            parent_frame,
            text="Browse...",
            command=self._browse_output_directory,
        ).grid(row=4, column=2, sticky=tkinter_module.E, padx=(10, 0), pady=6)

        ttk.Checkbutton(
            parent_frame,
            text="Development mode (recommended until Inara has approved the application name)",
            variable=self._development_mode_variable,
        ).grid(row=5, column=0, columnspan=3, sticky=tkinter_module.W, pady=(8, 6))

        explanation = ttk.Label(
            parent_frame,
            text=(
                "The API key is never saved. Non-secret fields are remembered in the user's "
                "application-data directory. A successful request writes exactly one file named "
                "inara_profile.json and replaces the previous copy atomically."
            ),
            wraplength=900,
            justify=tkinter_module.LEFT,
        )
        explanation.grid(row=6, column=0, columnspan=3, sticky=tkinter_module.EW, pady=(8, 12))

        button_frame = ttk.Frame(parent_frame)
        button_frame.grid(row=7, column=0, columnspan=3, sticky=tkinter_module.EW, pady=(4, 12))
        button_frame.columnconfigure(4, weight=1)

        self._download_button = ttk.Button(
            button_frame,
            text="Download profile",
            command=self._start_profile_download,
        )
        self._download_button.grid(row=0, column=0, padx=(0, 8))

        self._open_output_button = ttk.Button(
            button_frame,
            text="Open output folder",
            command=self._open_output_directory,
            state=tkinter_module.DISABLED,
        )
        self._open_output_button.grid(row=0, column=1, padx=(0, 8))

        ttk.Button(
            button_frame,
            text="Inara API key page",
            command=lambda: webbrowser.open(INARA_API_SETTINGS_URL),
        ).grid(row=0, column=2, padx=(0, 8))

        ttk.Button(
            button_frame,
            text="API documentation",
            command=lambda: webbrowser.open(INARA_API_DOCUMENTATION_URL),
        ).grid(row=0, column=3)

        summary_group = ttk.LabelFrame(parent_frame, text="Last session result", padding=12)
        summary_group.grid(row=8, column=0, columnspan=3, sticky=tkinter_module.EW)
        summary_group.columnconfigure(0, weight=1)
        ttk.Label(
            summary_group,
            textvariable=self._profile_summary_variable,
            wraplength=900,
            justify=tkinter_module.LEFT,
        ).grid(row=0, column=0, sticky=tkinter_module.EW)

    def _create_scope_tab(self, parent_frame: ttk.Frame) -> None:
        """Create a static, explicit explanation of the official API scope.

        @param parent_frame: Notebook tab that owns the explanatory text.
        """

        parent_frame.columnconfigure(0, weight=1)
        parent_frame.rowconfigure(0, weight=1)

        scope_text_widget = tkinter_module.Text(
            parent_frame,
            wrap=tkinter_module.WORD,
            height=24,
            padx=12,
            pady=12,
        )
        scope_text_widget.grid(row=0, column=0, sticky=tkinter_module.NSEW)
        scope_scrollbar = ttk.Scrollbar(
            parent_frame,
            orient=tkinter_module.VERTICAL,
            command=scope_text_widget.yview,
        )
        scope_scrollbar.grid(row=0, column=1, sticky=tkinter_module.NS)
        scope_text_widget.configure(yscrollcommand=scope_scrollbar.set)

        scope_text_widget.insert(
            tkinter_module.END,
            "What getCommanderProfile returns\n\n"
            "• Inara user and commander identity\n"
            "• Pilot ranks and progress\n"
            "• Preferred allegiance and power\n"
            "• Main-ship summary\n"
            "• Squadron summary\n"
            "• Preferred role\n"
            "• Avatar and Inara profile URLs\n"
            "• Inara data-import activity flag\n\n"
            "What it does not return\n\n"
            "• Engineering materials\n"
            "• Odyssey goods, assets, data, consumables, backpack or ship locker\n"
            "• Complete fleet, loadouts or stored modules\n"
            "• Cargo\n"
            "• Credits, assets or loans\n"
            "• Engineer unlock state\n"
            "• Missions, statistics, permits or travel history\n\n"
            "Why this matters\n\n"
            "Inara provides API events that allow applications such as EDMC and EDDiscovery "
            "to send these datasets to Inara. Those write events are not paired with read "
            "events. Therefore, a personal Inara API key cannot download a complete private "
            "commander snapshot. The generated JSON records this limitation explicitly so a "
            "downstream reader cannot mistake omitted data for a zero balance or empty inventory.\n\n"
            "Application registration\n\n"
            "Inara's developer guide requires the exact application name to be identified and "
            "whitelisted. Enter the approved name exactly as registered. Keep development mode "
            "enabled while testing."
        )
        scope_text_widget.configure(state=tkinter_module.DISABLED)

        ttk.Button(
            parent_frame,
            text="Open Inara developer guide",
            command=lambda: webbrowser.open(INARA_API_DEVELOPER_GUIDE_URL),
        ).grid(row=1, column=0, sticky=tkinter_module.W, pady=(12, 0))

    def _create_diagnostics_tab(self, parent_frame: ttk.Frame) -> None:
        """Create non-secret runtime diagnostics and log-file controls.

        @param parent_frame: Notebook tab that owns the diagnostics controls.
        """

        parent_frame.columnconfigure(1, weight=1)

        ttk.Label(parent_frame, text="Settings file:").grid(
            row=0,
            column=0,
            sticky=tkinter_module.NW,
            padx=(0, 12),
            pady=6,
        )
        ttk.Label(
            parent_frame,
            text=str(self._configuration_repository.settings_file),
            wraplength=760,
            justify=tkinter_module.LEFT,
        ).grid(row=0, column=1, sticky=tkinter_module.EW, pady=6)

        ttk.Label(parent_frame, text="Log file:").grid(
            row=1,
            column=0,
            sticky=tkinter_module.NW,
            padx=(0, 12),
            pady=6,
        )
        ttk.Label(
            parent_frame,
            text=str(self._log_file),
            wraplength=760,
            justify=tkinter_module.LEFT,
        ).grid(row=1, column=1, sticky=tkinter_module.EW, pady=6)

        ttk.Label(parent_frame, text="Security:").grid(
            row=2,
            column=0,
            sticky=tkinter_module.NW,
            padx=(0, 12),
            pady=6,
        )
        ttk.Label(
            parent_frame,
            text=(
                "The API key is not persisted, exported or logged. The log records only "
                "commander/app names, status and output paths."
            ),
            wraplength=760,
            justify=tkinter_module.LEFT,
        ).grid(row=2, column=1, sticky=tkinter_module.EW, pady=6)

        ttk.Button(
            parent_frame,
            text="Open log folder",
            command=lambda: self._open_directory_in_file_manager(self._log_file.parent),
        ).grid(row=3, column=0, columnspan=2, sticky=tkinter_module.W, pady=(12, 0))

    def _load_non_secret_settings(self) -> None:
        """Load remembered fields while deliberately leaving the API key blank."""

        default_output_directory = Path.cwd() / "output"
        try:
            application_settings = self._configuration_repository.load(default_output_directory)
        except InaraProfileDownloaderError as exception:
            self._application_logger.warning("Unable to load settings: %s", exception)
            messagebox.showwarning("Settings", str(exception))
            application_settings = ApplicationSettings(
                registered_application_name="Inara Profile Downloader",
                commander_name="",
                commander_frontier_id="",
                output_directory=str(default_output_directory),
                development_mode=True,
            )

        self._registered_application_name_variable.set(
            application_settings.registered_application_name
        )
        self._commander_name_variable.set(application_settings.commander_name)
        self._commander_frontier_id_variable.set(
            application_settings.commander_frontier_id
        )
        self._output_directory_variable.set(application_settings.output_directory)
        self._development_mode_variable.set(application_settings.development_mode)

    def _toggle_api_key_visibility(self) -> None:
        """Switch the API-key entry between masked and visible text."""

        self._api_key_entry.configure(
            show="" if self._show_api_key_variable.get() else "•"
        )

    def _browse_output_directory(self) -> None:
        """Ask the user to select a directory for the single JSON export."""

        initial_directory = self._output_directory_variable.get().strip() or str(Path.cwd())
        selected_directory = filedialog.askdirectory(
            title="Select profile output directory",
            initialdir=initial_directory,
            mustexist=False,
        )
        if selected_directory:
            self._output_directory_variable.set(selected_directory)

    def _start_profile_download(self) -> None:
        """Validate GUI state and start the network workflow in a worker thread."""

        if self._download_in_progress:
            return

        output_directory_text = self._output_directory_variable.get().strip()
        if not output_directory_text:
            messagebox.showerror("Validation", "Select an output directory.")
            return

        try:
            output_directory = Path(output_directory_text).expanduser()
        except (TypeError, ValueError) as exception:
            messagebox.showerror("Validation", f"The output directory is invalid: {exception}")
            return

        download_request = ProfileDownloadRequest(
            credentials=ApiCredentials(
                api_key=self._api_key_variable.get().strip(),
                registered_application_name=(
                    self._registered_application_name_variable.get().strip()
                ),
                application_version=APPLICATION_VERSION,
                development_mode=self._development_mode_variable.get(),
            ),
            commander_name=self._commander_name_variable.get().strip(),
            commander_frontier_id=self._commander_frontier_id_variable.get().strip(),
            output_directory=output_directory,
        )

        self._set_busy_state(True)
        self._status_variable.set("Contacting Inara...")

        worker_thread = threading.Thread(
            target=self._download_worker,
            args=(download_request,),
            name="InaraProfileDownloadWorker",
            daemon=True,
        )
        worker_thread.start()

    def _download_worker(self, download_request: ProfileDownloadRequest) -> None:
        """Execute the blocking controller workflow outside the Tkinter thread.

        @param download_request: Immutable request captured from the GUI.
        """

        try:
            download_result = self._controller.download_and_export(download_request)
        except InaraProfileDownloaderError as exception:
            self._application_logger.warning("Profile download failed: %s", exception)
            self._worker_outcome_queue.put(
                WorkerOutcome(result=None, error_message=str(exception))
            )
        except Exception as exception:  # Defensive boundary around the GUI worker.
            self._application_logger.exception("Unexpected profile-download failure.")
            self._worker_outcome_queue.put(
                WorkerOutcome(
                    result=None,
                    error_message=(
                        "An unexpected error occurred. Review the application log for details: "
                        f"{exception}"
                    ),
                )
            )
        else:
            self._worker_outcome_queue.put(
                WorkerOutcome(result=download_result, error_message=None)
            )

    def _poll_worker_outcomes(self) -> None:
        """Process worker messages on the Tkinter thread at a small fixed interval."""

        try:
            while True:
                worker_outcome = self._worker_outcome_queue.get_nowait()
                self._handle_worker_outcome(worker_outcome)
        except queue.Empty:
            pass
        finally:
            self._root_window.after(150, self._poll_worker_outcomes)

    def _handle_worker_outcome(self, worker_outcome: WorkerOutcome) -> None:
        """Update GUI state after one worker operation completes.

        @param worker_outcome: Success result or user-facing failure message.
        """

        self._set_busy_state(False)

        if worker_outcome.error_message:
            self._status_variable.set("Download failed.")
            messagebox.showerror("Inara profile download", worker_outcome.error_message)
            return

        download_result = worker_outcome.result
        if download_result is None:
            self._status_variable.set("Download failed without a result.")
            return

        self._last_output_file = download_result.output_file
        self._open_output_button.configure(state=tkinter_module.NORMAL)
        self._status_variable.set(f"Profile saved to {download_result.output_file}")

        commander_name_value = download_result.profile_data.get("commanderName")
        user_name_value = download_result.profile_data.get("userName")
        display_name = (
            commander_name_value
            if isinstance(commander_name_value, str) and commander_name_value
            else user_name_value
            if isinstance(user_name_value, str) and user_name_value
            else "profile"
        )
        self._profile_summary_variable.set(
            f"Downloaded {display_name}. API event status: {download_result.event_status}. "
            f"Output: {download_result.output_file}. The file contains only the basic data "
            "exposed by getCommanderProfile; it does not contain inventory or complete fleet data."
        )
        messagebox.showinfo(
            "Inara profile download",
            f"Profile saved successfully:\n\n{download_result.output_file}",
        )

    def _set_busy_state(self, is_busy: bool) -> None:
        """Enable or disable controls during a background request.

        @param is_busy: True while a network operation is active.
        """

        self._download_in_progress = is_busy
        self._download_button.configure(
            state=tkinter_module.DISABLED if is_busy else tkinter_module.NORMAL
        )
        if is_busy:
            self._progress_bar.start(12)
        else:
            self._progress_bar.stop()

    def _open_output_directory(self) -> None:
        """Open the directory containing the most recent exported profile."""

        output_directory = (
            self._last_output_file.parent
            if self._last_output_file is not None
            else Path(self._output_directory_variable.get().strip() or Path.cwd())
        )
        self._open_directory_in_file_manager(output_directory)

    def _open_directory_in_file_manager(self, directory_path: Path) -> None:
        """Open one directory using the platform's native file manager.

        @param directory_path: Directory to display.
        """

        resolved_directory = directory_path.expanduser().resolve()
        try:
            resolved_directory.mkdir(parents=True, exist_ok=True)
            if os.name == "nt":
                os.startfile(resolved_directory)  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.run(["open", str(resolved_directory)], check=True)
            else:
                subprocess.run(["xdg-open", str(resolved_directory)], check=True)
        except (OSError, subprocess.SubprocessError) as exception:
            messagebox.showerror(
                "Open folder",
                f"Unable to open {resolved_directory}: {exception}",
            )

    def _handle_window_close(self) -> None:
        """Close the application, warning only when a request is still active."""

        if self._download_in_progress:
            should_close = messagebox.askyesno(
                "Exit",
                "A request is still running. Exit anyway?",
            )
            if not should_close:
                return
        self._root_window.destroy()


def launch_application() -> None:
    """Construct all application services and start the Tkinter event loop."""

    application_logger, log_file = configure_application_logging()
    application_logger.info("Starting Inara Profile Downloader %s.", APPLICATION_VERSION)

    project_root_directory = Path(__file__).resolve().parents[2]
    default_output_directory = project_root_directory / "output"
    configuration_repository = ConfigurationRepository()

    request_rate_limiter = RequestRateLimiter(MINIMUM_REQUEST_INTERVAL_SECONDS)
    api_client = InaraApiClient(request_rate_limiter=request_rate_limiter)
    profile_exporter = ProfileExporter()
    controller = ProfileDownloadController(
        api_client=api_client,
        profile_exporter=profile_exporter,
        configuration_repository=configuration_repository,
        application_logger=application_logger,
    )

    # Pre-create the default output directory where possible. Failure is not fatal;
    # the exporter will present a precise error if the user later selects it.
    try:
        default_output_directory.mkdir(parents=True, exist_ok=True)
    except OSError:
        application_logger.warning(
            "Unable to pre-create default output directory %s.",
            default_output_directory,
        )

    root_window = tkinter_module.Tk()
    InaraProfileDownloaderApplication(
        root_window=root_window,
        controller=controller,
        configuration_repository=configuration_repository,
        application_logger=application_logger,
        log_file=log_file,
    )
    root_window.mainloop()
