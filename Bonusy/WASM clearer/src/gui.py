"""Tkinter user interface for the MSFS WASM cache cleaner."""

from __future__ import annotations

import queue
import threading
import tkinter as tk
from tkinter import messagebox, ttk

from .cleaner import clean_entry, describe_clean_plan
from .discovery import scan_wasm_caches
from .models import CacheEntry, CleanResult, ScanResult
from .path_utils import format_path


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


class WasmCleanerApp(tk.Tk):
    """Main Tkinter application."""

    def __init__(self) -> None:
        super().__init__()
        self.title("MSFS WASM Cache Cleaner")
        self.geometry("1100x720")
        self.minsize(900, 560)

        self.result_queue: queue.Queue[tuple[str, object]] = queue.Queue()
        self.entries: tuple[CacheEntry, ...] = ()
        self.entry_vars: dict[CacheEntry, tk.BooleanVar] = {}
        self.busy = False

        self._build_ui()
        self.after(100, self._poll_queue)
        self.after(250, self.start_scan)

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

        plan = describe_clean_plan(selected)
        if not messagebox.askyesno("Confirm WASM Cache Cleanup", plan, icon="warning"):
            self._append_log("Cleanup cancelled by user.")
            return

        self._set_busy(True, f"Clearing {len(selected)} selected cache entr{'y' if len(selected) == 1 else 'ies'}...")
        self._append_log(f"Cleanup started for {len(selected)} selected entr{'y' if len(selected) == 1 else 'ies'}.")
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

    def _update_selected_status(self) -> None:
        """Refresh the status bar with the current selection count."""

        selected_count = sum(1 for var in self.entry_vars.values() if var.get())
        if self.busy:
            return
        if self.entries:
            self.status_var.set(f"{selected_count} of {len(self.entries)} entries selected.")
        else:
            self.status_var.set("No eligible WASM cache entries found.")


def main() -> None:
    """Run the Tkinter app."""

    app = WasmCleanerApp()
    app.mainloop()
