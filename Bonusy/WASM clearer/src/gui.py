"""Tkinter user interface for the MSFS WASM cache cleaner."""

import queue
import threading
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from .cleaner import build_clean_plan, clean_entry, inspect_entry_details
from .discovery import scan_wasm_caches
from .models import CacheEntry, CacheEntryDetails, CleanPlan, CleanResult, ScanResult
from .path_utils import format_path


def format_bytes(byte_count: int) -> str:
    """Format a byte count using compact binary units."""

    value = float(byte_count)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if value < 1024 or unit == "TiB":
            return f"{value:,.0f} {unit}" if unit == "B" else f"{value:,.1f} {unit}"
        value /= 1024
    return f"{byte_count:,} B"


class ScrollableFrame(ttk.Frame):
    """A vertically scrollable frame for checkbutton rows."""

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.content = ttk.Frame(self.canvas)
        self.window = self.canvas.create_window((0, 0), window=self.content, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.content.bind("<Configure>", self._on_content_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel, add="+")

    def _on_content_configure(self, _event: tk.Event) -> None:
        """Keep the canvas scroll region aligned with the content size."""

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event: tk.Event) -> None:
        """Stretch the inner frame to match the visible canvas width."""

        self.canvas.itemconfigure(self.window, width=event.width)

    def _on_mousewheel(self, event: tk.Event) -> None:
        """Scroll the frame when the user uses the mouse wheel."""

        if self.winfo_ismapped():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class CacheDetailsDialog(tk.Toplevel):
    """Show a bounded on-demand inspection of files in one cache entry."""

    def __init__(self, master: tk.Misc, entry: CacheEntry) -> None:
        super().__init__(master)
        self.owner = master
        self.entry = entry
        self.detail_queue: queue.Queue[CacheEntryDetails | Exception] = queue.Queue()
        self.title(f"Cache details - {entry.product_name}")
        self.geometry("920x560")
        self.minsize(720, 420)
        self.transient(master)
        self.protocol("WM_DELETE_WINDOW", self._close)

        shell = ttk.Frame(self, padding=18)
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(0, weight=1)
        shell.rowconfigure(3, weight=1)
        ttk.Label(shell, text=entry.product_name, style="DialogTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(shell, text=entry.display_name, style="Muted.TLabel").grid(row=1, column=0, sticky="w")
        self.status_var = tk.StringVar(value="Inspecting files...")
        ttk.Label(shell, textvariable=self.status_var).grid(row=2, column=0, sticky="w", pady=(10, 8))

        table = ttk.Frame(shell)
        table.grid(row=3, column=0, sticky="nsew")
        table.columnconfigure(0, weight=1)
        table.rowconfigure(0, weight=1)
        columns = ("path", "kind", "status", "size", "modified")
        self.tree = ttk.Treeview(table, columns=columns, show="headings")
        for column, heading, width, stretch in (
            ("path", "Relative path", 360, True),
            ("kind", "Type", 170, False),
            ("status", "Cleanup", 85, False),
            ("size", "Size", 80, False),
            ("modified", "Modified", 135, False),
        ):
            self.tree.heading(column, text=heading)
            self.tree.column(column, width=width, minwidth=65, stretch=stretch, anchor="w")
        self.tree.grid(row=0, column=0, sticky="nsew")
        vertical = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview)
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal = ttk.Scrollbar(table, orient="horizontal", command=self.tree.xview)
        horizontal.grid(row=1, column=0, sticky="ew")
        self.tree.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)

        footer = ttk.Frame(shell)
        footer.grid(row=4, column=0, sticky="ew", pady=(12, 0))
        footer.columnconfigure(0, weight=1)
        ttk.Label(
            footer,
            text="Type information is signature/extension based; compiled module behavior is not inferred.",
            style="Muted.TLabel",
        ).grid(row=0, column=0, sticky="w")
        ttk.Button(footer, text="Close", command=self._close).grid(row=0, column=1, sticky="e")

        self.grab_set()
        threading.Thread(target=self._inspect_worker, daemon=True).start()
        self.after(100, self._poll_details)

    def _inspect_worker(self) -> None:
        try:
            self.detail_queue.put(inspect_entry_details(self.entry))
        except Exception as exc:
            self.detail_queue.put(exc)

    def _poll_details(self) -> None:
        if not self.winfo_exists():
            return
        try:
            result = self.detail_queue.get_nowait()
        except queue.Empty:
            self.after(100, self._poll_details)
            return
        if isinstance(result, Exception):
            self.status_var.set(f"Inspection failed: {result}")
            return
        self._populate_details(result)

    def _populate_details(self, details: CacheEntryDetails) -> None:
        for file_detail in details.files:
            modified = (
                datetime.fromtimestamp(file_detail.modified_time).strftime("%Y-%m-%d %H:%M")
                if file_detail.modified_time is not None
                else "Unknown"
            )
            self.tree.insert(
                "",
                "end",
                values=(
                    file_detail.relative_path,
                    file_detail.kind,
                    file_detail.disposition,
                    format_bytes(file_detail.byte_count),
                    modified,
                ),
            )
        status = f"{len(details.files):,} item(s) inspected."
        if details.truncated:
            status += " Listing limited to the first 10,000 items."
        if details.warnings:
            status += f" {len(details.warnings)} warning(s)."
        self.status_var.set(status)

    def _close(self) -> None:
        self.grab_release()
        self.destroy()
        if self.owner.winfo_exists():
            self.owner.grab_set()


class CleanupConfirmationDialog(tk.Toplevel):
    """Compact, detailed confirmation for a prepared cleanup plan."""

    def __init__(self, master: tk.Misc, plan: CleanPlan) -> None:
        super().__init__(master)
        self.confirmed = False
        self.plan = plan
        self.selected_items = plan.items
        self.sort_column = "product"
        self.sort_reverse = False
        self.title("Review cleanup")
        self.geometry("860x560")
        self.minsize(740, 480)
        self.transient(master)
        self.protocol("WM_DELETE_WINDOW", self._cancel)

        shell = ttk.Frame(self, padding=18)
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(0, weight=1)
        shell.rowconfigure(4, weight=1)

        ttk.Label(shell, text="Review what will be cleared", style="DialogTitle.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            shell,
            text="Only cache data shown below is targeted. Settings and state folders remain untouched.",
            style="Muted.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 14))

        summary = ttk.Frame(shell, style="Card.TFrame", padding=12)
        summary.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        for column in range(4):
            summary.columnconfigure(column, weight=1)
        self.selected_count_var = tk.StringVar()
        self.selected_size_var = tk.StringVar()
        self.selected_files_var = tk.StringVar()
        self.selected_protected_var = tk.StringVar()
        self._summary_value(summary, 0, self.selected_count_var, "Selected caches")
        self._summary_value(summary, 1, self.selected_size_var, "Data to clear")
        self._summary_value(summary, 2, self.selected_files_var, "Files")
        self._summary_value(summary, 3, self.selected_protected_var, "Protected items")

        filters = ttk.Frame(shell)
        filters.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        filters.columnconfigure(6, weight=1)
        ttk.Label(filters, text="Clean:").grid(row=0, column=0, sticky="w", padx=(0, 6))

        self.simulator_filter = tk.StringVar(value="All simulators")
        simulator_values = ("All simulators",) + tuple(sorted({item.entry.simulator for item in plan.items}))
        simulator_box = ttk.Combobox(
            filters, textvariable=self.simulator_filter, values=simulator_values, state="readonly", width=17
        )
        simulator_box.grid(row=0, column=1, sticky="w", padx=(0, 10))

        self.channel_filter = tk.StringVar(value="All channels")
        channel_values = ("All channels",) + tuple(sorted({item.entry.channel for item in plan.items}))
        channel_box = ttk.Combobox(
            filters, textvariable=self.channel_filter, values=channel_values, state="readonly", width=20
        )
        channel_box.grid(row=0, column=2, sticky="w", padx=(0, 10))

        self.data_filter = tk.StringVar(value="All data sizes")
        data_box = ttk.Combobox(
            filters,
            textvariable=self.data_filter,
            values=("All data sizes", "Non-zero data", "Zero data"),
            state="readonly",
            width=16,
        )
        data_box.grid(row=0, column=3, sticky="w")
        ttk.Label(filters, text="Filters define the cleanup selection.", style="Muted.TLabel").grid(
            row=0, column=6, sticky="e"
        )
        for box in (simulator_box, channel_box, data_box):
            box.bind("<<ComboboxSelected>>", self._apply_filters)

        list_frame = ttk.Frame(shell)
        list_frame.grid(row=4, column=0, sticky="nsew")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        columns = ("product", "simulator", "size", "files", "folders", "protected")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=9)
        self.headings = (
            ("product", "Product", 195, True),
            ("simulator", "Simulator", 110, False),
            ("size", "Data", 90, False),
            ("files", "Files", 65, False),
            ("folders", "Folders", 70, False),
            ("protected", "Protected", 80, False),
        )
        for column, heading, width, stretch in self.headings:
            self.tree.heading(column, text=heading, command=lambda key=column: self._sort_by(key))
            self.tree.column(column, width=width, minwidth=55, anchor="w", stretch=stretch)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind("<Double-1>", self._open_details)
        self.tree.bind("<Return>", self._open_details)
        self.tree.bind("<<TreeviewSelect>>", self._update_details_button)

        note = "This cannot be undone. MSFS will rebuild cleared cache data when needed."
        if plan.warnings:
            note = f"{len(plan.warnings)} item(s) could not be fully inspected and will be revalidated before deletion."
        ttk.Label(shell, text=note, style="Warning.TLabel", wraplength=760).grid(
            row=5, column=0, sticky="w", pady=(12, 12)
        )

        buttons = ttk.Frame(shell)
        buttons.grid(row=6, column=0, sticky="e")
        self.details_button = ttk.Button(buttons, text="View file details", command=self._open_details, state="disabled")
        self.details_button.pack(side="left", padx=(0, 16))
        ttk.Button(buttons, text="Cancel", command=self._cancel).pack(side="left", padx=(0, 8))
        self.clear_button = ttk.Button(
            buttons, text="Clear selected caches", style="Accent.TButton", command=self._confirm
        )
        self.clear_button.pack(side="left")

        self.bind("<Escape>", lambda _event: self._cancel())
        self.bind("<Return>", lambda _event: self._confirm())
        self.grab_set()
        self._refresh_table()
        self.after_idle(self.clear_button.focus_set)

    @staticmethod
    def _summary_value(parent: ttk.Frame, column: int, value: tk.StringVar, label: str) -> None:
        block = ttk.Frame(parent, style="Card.TFrame")
        block.grid(row=0, column=column, sticky="w", padx=(0, 18))
        ttk.Label(block, textvariable=value, style="SummaryValue.TLabel").pack(anchor="w")
        ttk.Label(block, text=label, style="CardMuted.TLabel").pack(anchor="w")

    def _apply_filters(self, _event: tk.Event | None = None) -> None:
        """Make the visible filtered rows the authoritative cleanup selection."""

        simulator = self.simulator_filter.get()
        channel = self.channel_filter.get()
        data_scope = self.data_filter.get()
        self.selected_items = tuple(
            item
            for item in self.plan.items
            if (simulator == "All simulators" or item.entry.simulator == simulator)
            and (channel == "All channels" or item.entry.channel == channel)
            and (data_scope == "All data sizes" or (data_scope == "Non-zero data") == (item.byte_count > 0))
        )
        self._refresh_table()

    def _sort_by(self, column: str) -> None:
        """Sort the selected plan rows by a clicked column heading."""

        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        self._refresh_table()

    def _update_details_button(self, _event: tk.Event | None = None) -> None:
        self.details_button.configure(state="normal" if self.tree.selection() else "disabled")

    def _open_details(self, event: tk.Event | None = None) -> None:
        """Open on-demand file details for the selected cleanup row."""

        if event is not None and getattr(event, "num", None) == 1:
            row_id = self.tree.identify_row(event.y)
            if row_id:
                self.tree.selection_set(row_id)
        selection = self.tree.selection()
        if not selection:
            return
        item = self.row_items.get(selection[0])
        if item is not None:
            CacheDetailsDialog(self, item.entry)

    def _refresh_table(self) -> None:
        """Render the filtered selection, ordering, totals, and heading indicator."""

        key_functions = {
            "product": lambda item: item.entry.product_name.casefold(),
            "simulator": lambda item: item.entry.simulator.casefold(),
            "size": lambda item: item.byte_count,
            "files": lambda item: item.file_count,
            "folders": lambda item: item.directory_count,
            "protected": lambda item: item.preserved_count,
        }
        ordered = sorted(self.selected_items, key=key_functions[self.sort_column], reverse=self.sort_reverse)
        self.row_items = {}
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in ordered:
            row_id = self.tree.insert(
                "",
                "end",
                values=(
                    item.entry.product_name,
                    item.entry.simulator,
                    format_bytes(item.byte_count),
                    f"{item.file_count:,}",
                    f"{item.directory_count:,}",
                    f"{item.preserved_count:,}",
                ),
            )
            self.row_items[row_id] = item

        for column, heading, _width, _stretch in self.headings:
            indicator = " ▲" if column == self.sort_column and not self.sort_reverse else " ▼"
            self.tree.heading(column, text=heading + indicator if column == self.sort_column else heading)

        self.selected_count_var.set(f"{len(self.selected_items)} / {len(self.plan.items)}")
        self.selected_size_var.set(format_bytes(sum(item.byte_count for item in self.selected_items)))
        self.selected_files_var.set(f"{sum(item.file_count for item in self.selected_items):,}")
        self.selected_protected_var.set(f"{sum(item.preserved_count for item in self.selected_items):,}")
        self.clear_button.configure(state="normal" if self.selected_items else "disabled")
        self._update_details_button()

    def _confirm(self) -> None:
        if not self.selected_items:
            return
        self.confirmed = True
        self.destroy()

    def _cancel(self) -> None:
        self.destroy()


class WasmCleanerApp(tk.Tk):
    """Main Tkinter application."""

    def __init__(self) -> None:
        super().__init__()
        self.title("MSFS WASM Cache Cleaner")
        self.geometry("1100x720")
        self.minsize(900, 560)

        self._configure_styles()

        self.result_queue: queue.Queue[tuple[str, object]] = queue.Queue()
        self.entries: tuple[CacheEntry, ...] = ()
        self.entry_vars: dict[CacheEntry, tk.BooleanVar] = {}
        self.busy = False

        self._build_ui()
        self.after(100, self._poll_queue)
        self.after(250, self.start_scan)

    def _configure_styles(self) -> None:
        """Apply a restrained Windows-friendly visual hierarchy."""

        style = ttk.Style(self)
        style.configure("DialogTitle.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Muted.TLabel", foreground="#5d6470")
        style.configure("Warning.TLabel", foreground="#8a4b08")
        style.configure("Card.TFrame", background="#f2f5f8")
        style.configure("SummaryValue.TLabel", background="#f2f5f8", font=("Segoe UI", 13, "bold"))
        style.configure("CardMuted.TLabel", background="#f2f5f8", foreground="#5d6470")
        style.configure("Accent.TButton", font=("Segoe UI", 9, "bold"))

    def _build_ui(self) -> None:
        """Construct the full user interface."""

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        header = ttk.Frame(self, padding=(12, 10, 12, 4))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        title = ttk.Label(header, text="MSFS WASM Cache Cleaner", font=("Segoe UI", 15, "bold"))
        title.grid(row=0, column=0, sticky="w")

        self.status_var = tk.StringVar(value="Ready.")
        status = ttk.Label(header, textvariable=self.status_var, foreground="#444")
        status.grid(row=1, column=0, sticky="w", pady=(4, 0))

        controls = ttk.Frame(self, padding=(12, 6))
        controls.grid(row=1, column=0, sticky="ew")
        controls.columnconfigure(5, weight=1)

        self.refresh_button = ttk.Button(controls, text="Refresh / Rescan", command=self.start_scan)
        self.refresh_button.grid(row=0, column=0, padx=(0, 8))

        self.select_all_button = ttk.Button(controls, text="Select All", command=self.select_all)
        self.select_all_button.grid(row=0, column=1, padx=(0, 8))

        self.select_none_button = ttk.Button(controls, text="Select None", command=self.select_none)
        self.select_none_button.grid(row=0, column=2, padx=(0, 8))

        self.clear_button = ttk.Button(controls, text="Clear Selected Cache", command=self.clear_selected)
        self.clear_button.grid(row=0, column=3, padx=(0, 8))

        self.exit_button = ttk.Button(controls, text="Exit", command=self.destroy)
        self.exit_button.grid(row=0, column=4, padx=(0, 8))

        body = ttk.PanedWindow(self, orient="vertical")
        body.grid(row=2, column=0, sticky="nsew", padx=12, pady=(2, 8))

        entries_frame = ttk.LabelFrame(body, text="Eligible WASM Cache Entries", padding=8)
        entries_frame.columnconfigure(0, weight=1)
        entries_frame.rowconfigure(1, weight=1)

        header_row = ttk.Frame(entries_frame)
        header_row.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        header_row.columnconfigure(1, weight=1)
        ttk.Label(header_row, text="", width=4).grid(row=0, column=0, sticky="w")
        ttk.Label(header_row, text="Product", font=("Segoe UI", 9, "bold")).grid(row=0, column=1, sticky="w")
        ttk.Label(header_row, text="Simulator", width=18, font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="w")
        ttk.Label(header_row, text="Path", width=58, font=("Segoe UI", 9, "bold")).grid(row=0, column=3, sticky="w")

        self.entries_scroll = ScrollableFrame(entries_frame)
        self.entries_scroll.grid(row=1, column=0, sticky="nsew")
        body.add(entries_frame, weight=3)

        roots_frame = ttk.LabelFrame(body, text="Detected Simulator Roots", padding=8)
        roots_frame.columnconfigure(0, weight=1)
        roots_frame.rowconfigure(0, weight=1)
        columns = ("simulator", "channel", "data", "packages", "wasm")
        self.roots_tree = ttk.Treeview(roots_frame, columns=columns, show="headings", height=6)
        for column, heading, width in (
            ("simulator", "Simulator", 110),
            ("channel", "Channel", 150),
            ("data", "Data Root", 260),
            ("packages", "Packages", 260),
            ("wasm", "WASM Roots", 300),
        ):
            self.roots_tree.heading(column, text=heading)
            self.roots_tree.column(column, width=width, anchor="w", stretch=True)
        self.roots_tree.grid(row=0, column=0, sticky="nsew")
        roots_scroll = ttk.Scrollbar(roots_frame, orient="vertical", command=self.roots_tree.yview)
        roots_scroll.grid(row=0, column=1, sticky="ns")
        self.roots_tree.configure(yscrollcommand=roots_scroll.set)
        body.add(roots_frame, weight=1)

        log_frame = ttk.LabelFrame(self, text="Status", padding=8)
        log_frame.grid(row=3, column=0, sticky="nsew", padx=12, pady=(0, 12))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        self.log_text = tk.Text(log_frame, height=8, wrap="word", state="disabled")
        self.log_text.grid(row=0, column=0, sticky="nsew")
        log_scroll = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        log_scroll.grid(row=0, column=1, sticky="ns")
        self.log_text.configure(yscrollcommand=log_scroll.set)

    def start_scan(self) -> None:
        """Start a background scan."""

        if self.busy:
            return
        self._set_busy(True, "Scanning for MSFS WASM cache entries...")
        self._append_log("Scan started.")
        thread = threading.Thread(target=self._scan_worker, daemon=True)
        thread.start()

    def _scan_worker(self) -> None:
        """Run the scan off the UI thread and forward the result to the queue."""

        try:
            result = scan_wasm_caches()
            self.result_queue.put(("scan_result", result))
        except Exception as exc:  # Keep the GUI alive on unexpected filesystem issues.
            self.result_queue.put(("error", f"Scan failed: {exc}"))

    def select_all(self) -> None:
        """Select all currently discovered eligible entries."""

        for var in self.entry_vars.values():
            var.set(True)
        self._update_selected_status()

    def select_none(self) -> None:
        """Clear all current selections."""

        for var in self.entry_vars.values():
            var.set(False)
        self._update_selected_status()

    def clear_selected(self) -> None:
        """Confirm and start cleanup for selected entries."""

        selected = tuple(entry for entry, var in self.entry_vars.items() if var.get())
        if not selected:
            messagebox.showinfo("No Selection", "Select one or more WASM cache entries first.")
            return

        self._set_busy(True, "Calculating cleanup size and contents...")
        thread = threading.Thread(target=self._plan_worker, args=(selected,), daemon=True)
        thread.start()

    def _plan_worker(self, selected: tuple[CacheEntry, ...]) -> None:
        """Build the read-only cleanup preview outside the UI thread."""

        try:
            self.result_queue.put(("clean_plan", build_clean_plan(selected)))
        except Exception as exc:
            self.result_queue.put(("error", f"Could not prepare cleanup preview: {exc}"))

    def _show_clean_plan(self, plan: CleanPlan) -> None:
        """Show the detailed plan and start cleanup only after confirmation."""

        self._set_busy(False, f"Reviewed {len(plan.items)} selected cache entries.")
        dialog = CleanupConfirmationDialog(self, plan)
        self.wait_window(dialog)
        if not dialog.confirmed:
            self._append_log("Cleanup cancelled by user.")
            self._update_selected_status()
            return

        selected = tuple(item.entry for item in dialog.selected_items)
        selected_set = set(selected)
        for entry, variable in self.entry_vars.items():
            variable.set(entry in selected_set)
        self._set_busy(True, f"Clearing {len(selected)} selected cache entr{'y' if len(selected) == 1 else 'ies'}...")
        self._append_log(
            f"Cleanup started: {len(selected)} cache entr{'y' if len(selected) == 1 else 'ies'}, "
            f"{sum(item.file_count for item in dialog.selected_items):,} files, "
            f"{format_bytes(sum(item.byte_count for item in dialog.selected_items))} estimated."
        )
        thread = threading.Thread(target=self._clean_worker, args=(selected,), daemon=True)
        thread.start()

    def _clean_worker(self, selected: tuple[CacheEntry, ...]) -> None:
        """Run cleanup for each selected entry on a background thread."""

        results: list[CleanResult] = []
        for entry in selected:
            try:
                results.append(clean_entry(entry))
            except Exception as exc:
                results.append(CleanResult(entry=entry, deleted_count=0, skipped_count=0, errors=(str(exc),)))
        self.result_queue.put(("clean_result", tuple(results)))

    def _poll_queue(self) -> None:
        """Process background worker results without blocking Tkinter."""

        while True:
            try:
                kind, payload = self.result_queue.get_nowait()
            except queue.Empty:
                break

            if kind == "scan_result":
                self._handle_scan_result(payload)  # type: ignore[arg-type]
            elif kind == "clean_plan":
                self._show_clean_plan(payload)  # type: ignore[arg-type]
            elif kind == "clean_result":
                self._handle_clean_result(payload)  # type: ignore[arg-type]
            elif kind == "error":
                self._append_log(str(payload))
                self._set_busy(False, "Ready.")

        self.after(100, self._poll_queue)

    def _handle_scan_result(self, result: ScanResult) -> None:
        """Render the latest scan result into the UI."""

        self.entries = result.entries
        self.entry_vars.clear()
        self._populate_entries(result.entries)
        self._populate_roots(result)

        if result.warnings:
            for warning in result.warnings:
                self._append_log(f"Warning: {warning}")

        if result.entries:
            self._append_log(f"Scan complete. Found {len(result.entries)} eligible WASM cache entr{'y' if len(result.entries) == 1 else 'ies'}.")
            self._set_busy(False, f"Found {len(result.entries)} eligible WASM cache entr{'y' if len(result.entries) == 1 else 'ies'}. All are unchecked.")
        else:
            self._append_log("Scan complete. No eligible WASM cache entries were found.")
            self._set_busy(False, "No eligible WASM cache entries found.")

    def _handle_clean_result(self, results: tuple[CleanResult, ...]) -> None:
        """Render cleanup results and trigger a refresh scan."""

        ok_count = sum(1 for result in results if result.ok)
        for result in results:
            status = "OK" if result.ok else "FAILED"
            self._append_log(
                f"{status}: {result.entry.display_name} - "
                f"deleted {result.deleted_count}, skipped {result.skipped_count}"
            )
            for skipped in result.skipped:
                self._append_log(f"  Preserved: {skipped}")
            for error in result.errors:
                self._append_log(f"  Error: {error}")

        self._set_busy(False, f"Cleanup complete: {ok_count}/{len(results)} entries completed without errors.")
        self.start_scan()

    def _populate_entries(self, entries: tuple[CacheEntry, ...]) -> None:
        """Populate the selectable cache list."""

        for child in self.entries_scroll.content.winfo_children():
            child.destroy()

        if not entries:
            ttk.Label(
                self.entries_scroll.content,
                text="No eligible WASM cache entries found.",
                padding=8,
            ).grid(row=0, column=0, sticky="w")
            return

        for row, entry in enumerate(entries):
            var = tk.BooleanVar(value=False)
            self.entry_vars[entry] = var

            row_frame = ttk.Frame(self.entries_scroll.content, padding=(0, 3))
            row_frame.grid(row=row, column=0, sticky="ew")
            row_frame.columnconfigure(1, weight=1)

            check = ttk.Checkbutton(row_frame, variable=var, command=self._update_selected_status)
            check.grid(row=0, column=0, sticky="w", padx=(0, 8))
            ttk.Label(row_frame, text=entry.product_name).grid(row=0, column=1, sticky="w", padx=(0, 8))
            ttk.Label(row_frame, text=entry.simulator, width=18).grid(row=0, column=2, sticky="w", padx=(0, 8))
            ttk.Label(row_frame, text=str(entry.cache_path), width=90).grid(row=0, column=3, sticky="w")

    def _populate_roots(self, result: ScanResult) -> None:
        """Populate the detected simulator roots table."""

        for item in self.roots_tree.get_children():
            self.roots_tree.delete(item)

        for location in result.locations:
            self.roots_tree.insert(
                "",
                "end",
                values=(
                    location.simulator,
                    location.channel,
                    format_path(location.data_root),
                    format_path(location.packages_path),
                    "; ".join(str(root) for root in location.wasm_roots),
                ),
            )

    def _append_log(self, text: str) -> None:
        """Append a line to the status log."""

        self.log_text.configure(state="normal")
        self.log_text.insert("end", text + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _set_busy(self, busy: bool, status: str) -> None:
        """Toggle button state while a worker thread is active."""

        self.busy = busy
        self.status_var.set(status)
        state = "disabled" if busy else "normal"
        for button in (self.refresh_button, self.select_all_button, self.select_none_button, self.clear_button):
            button.configure(state=state)
        if not busy and not any(var.get() for var in self.entry_vars.values()):
            self.clear_button.configure(state="disabled")

    def _update_selected_status(self) -> None:
        """Refresh the status bar with the current selection count."""

        selected_count = sum(1 for var in self.entry_vars.values() if var.get())
        if self.busy:
            return
        if self.entries:
            self.status_var.set(f"{selected_count} of {len(self.entries)} entries selected.")
            self.clear_button.configure(state="normal" if selected_count else "disabled")
        else:
            self.status_var.set("No eligible WASM cache entries found.")
            self.clear_button.configure(state="disabled")


def main() -> None:
    """Run the Tkinter app."""

    app = WasmCleanerApp()
    app.mainloop()
