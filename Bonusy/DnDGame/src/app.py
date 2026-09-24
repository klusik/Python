"""
app.py

Tkinter application:
- HUD bar on top
- Left: player stats
- Center: chat and input
- Right: inventory and ground
- Startup prompt: OpenAI API key, with optional storage
"""

from __future__ import annotations

import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from typing import Optional

from api import ApiConfig, OpenAIClient
from config import Config, ensure_directories
from models import GameState, Item, Player
from tools import (
    format_kg,
    item_from_catalog,
    load_game,
    normalize_item_name,
    parse_command,
    parse_quantity_and_name,
    save_game,
)


class ApiKeyDialog(tk.Toplevel):
    """Modal dialog that requests API key and an optional 'store key' checkbox."""

    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.title("OpenAI API Key")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self._api_key_var = tk.StringVar(value="")
        self._store_var = tk.BooleanVar(value=False)

        frm = ttk.Frame(self, padding=12)
        frm.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frm, text="Enter OpenAI API key:").grid(row=0, column=0, sticky="w")
        entry = ttk.Entry(frm, textvariable=self._api_key_var, width=44, show="*")
        entry.grid(row=1, column=0, sticky="ew", pady=(6, 8))
        entry.focus_set()

        ttk.Checkbutton(frm, text="Store code (writes to savegames/.openai_api_key.txt)", variable=self._store_var).grid(
            row=2, column=0, sticky="w"
        )

        btns = ttk.Frame(frm)
        btns.grid(row=3, column=0, sticky="e", pady=(12, 0))

        ttk.Button(btns, text="Cancel", command=self._cancel).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(btns, text="OK", command=self._ok).grid(row=0, column=1)

        self._result_api_key: Optional[str] = None
        self._result_store: bool = False

        self.bind("<Return>", lambda _e: self._ok())
        self.bind("<Escape>", lambda _e: self._cancel())

    def _ok(self) -> None:
        key = self._api_key_var.get().strip()
        if not key:
            messagebox.showerror("Missing key", "API key cannot be empty.")
            return
        self._result_api_key = key
        self._result_store = bool(self._store_var.get())
        self.destroy()

    def _cancel(self) -> None:
        self._result_api_key = None
        self._result_store = False
        self.destroy()

    def result(self) -> Optional[ApiConfig]:
        """Return ApiConfig or None if canceled."""
        if self._result_api_key is None:
            return None
        return ApiConfig(api_key=self._result_api_key, store_key=self._result_store)


class App:
    """Main application orchestrator."""

    def __init__(self) -> None:
        ensure_directories()

        self.root = tk.Tk()
        self.root.title(Config.APP_TITLE)
        self.root.geometry(Config.DEFAULT_GEOMETRY)

        self._api_cfg: Optional[ApiConfig] = None
        self._client: Optional[OpenAIClient] = None

        self.state = self._default_new_game()

        self._build_ui()
        self._wire_events()

        self.root.after(50, self._startup_api_key_flow)
        self._refresh_all()

    def run(self) -> None:
        """Run Tk mainloop."""
        self.root.mainloop()

    # --------------------------
    # Startup and persistence
    # --------------------------

    def _default_new_game(self) -> GameState:
        """Create a default game state for a new game."""
        player = Player(name="Player")
        player.inventory.max_carry_kg = Config.DEFAULT_MAX_CARRY_KG
        return GameState(player=player)

    def _startup_api_key_flow(self) -> None:
        """
        Ask for API key on startup.

        If key is stored, load it automatically next launches, otherwise always ask.
        """
        stored_key_path = os.path.join(Config.SAVEGAMES_DIR, Config.STORE_API_KEY_FILENAME)
        if os.path.isfile(stored_key_path):
            try:
                with open(stored_key_path, "r", encoding="utf-8") as f:
                    key = f.read().strip()
                if key:
                    self._set_api_config(ApiConfig(api_key=key, store_key=True))
                    self._hud_status_var.set("API key loaded from disk")
                    return
            except OSError:
                pass

        dialog = ApiKeyDialog(self.root)
        self.root.wait_window(dialog)
        cfg = dialog.result()
        if cfg is None:
            self._set_api_config(None)
            return

        self._set_api_config(cfg)

    def _set_api_config(self, cfg: Optional[ApiConfig]) -> None:
        """
        Apply a new API configuration at runtime.

        - If cfg is None: disable API (offline mode)
        - If cfg.store_key is True: persist to savegames/.openai_api_key.txt
        - If cfg.store_key is False: remove persisted key if it exists
        """
        stored_key_path = os.path.join(Config.SAVEGAMES_DIR, Config.STORE_API_KEY_FILENAME)

        if cfg is None:
            self._api_cfg = None
            self._client = None
            self._hud_status_var.set("No API key. Running in offline mode.")
            return

        self._api_cfg = cfg
        self._client = OpenAIClient(cfg)

        if cfg.store_key:
            try:
                with open(stored_key_path, "w", encoding="utf-8") as f:
                    f.write(cfg.api_key)
                self._hud_status_var.set("API key stored to disk")
            except OSError:
                self._hud_status_var.set("API key not stored (write failed)")
        else:
            # Best-effort delete of a previously stored key
            try:
                if os.path.isfile(stored_key_path):
                    os.remove(stored_key_path)
            except OSError:
                pass
            self._hud_status_var.set("API key kept in memory only")

    def _on_change_api_key(self) -> None:
        """Open the API key dialog and apply the new key or switch to offline mode."""
        dialog = ApiKeyDialog(self.root)
        self.root.wait_window(dialog)
        cfg = dialog.result()
        if cfg is None:
            # Treat cancel as: do nothing (keep current config)
            self._hud_status_var.set("API key unchanged")
            return

        self._set_api_config(cfg)

    # --------------------------
    # UI layout
    # --------------------------

    def _build_ui(self) -> None:
        """Create all Tkinter widgets."""
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # HUD (top)
        hud = ttk.Frame(self.root, padding=(10, 8))
        hud.grid(row=0, column=0, sticky="ew")
        hud.columnconfigure(0, weight=1)  # left label expands

        self._hud_status_var = tk.StringVar(value="Starting...")
        self._hud_weight_var = tk.StringVar(value="Weight: 0.0 / 0.0 kg")
        self._hud_profile_var = tk.StringVar(value="Profile: (none)")

        ttk.Label(hud, textvariable=self._hud_profile_var).grid(row=0, column=0, sticky="w")

        # HUD action buttons (keep small, top-level)
        ttk.Button(hud, text="API Key...", command=self._on_change_api_key).grid(row=0, column=1, sticky="e",
                                                                                 padx=(12, 8))

        ttk.Label(hud, textvariable=self._hud_status_var).grid(row=0, column=2, sticky="e", padx=(0, 12))
        ttk.Label(hud, textvariable=self._hud_weight_var).grid(row=0, column=3, sticky="e")

        # Main body with 3 columns
        body = ttk.Frame(self.root, padding=10)
        body.grid(row=1, column=0, sticky="nsew")
        body.rowconfigure(0, weight=1)
        body.columnconfigure(0, weight=0, minsize=Config.LEFT_PANEL_MIN_WIDTH)
        body.columnconfigure(1, weight=1, minsize=Config.CENTER_PANEL_MIN_WIDTH)
        body.columnconfigure(2, weight=0, minsize=Config.RIGHT_PANEL_MIN_WIDTH)

        # Left panel: player stats
        left = ttk.Labelframe(body, text="Player", padding=10)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.columnconfigure(0, weight=1)

        self._player_name_var = tk.StringVar(value=self.state.player.name)
        self._hp_var = tk.StringVar(value="HP: 0/0")

        ttk.Label(left, text="Name").grid(row=0, column=0, sticky="w")
        self._player_name_entry = ttk.Entry(left, textvariable=self._player_name_var)
        self._player_name_entry.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        ttk.Label(left, textvariable=self._hp_var).grid(row=2, column=0, sticky="w", pady=(0, 8))

        ttk.Label(left, text="Stats").grid(row=3, column=0, sticky="w")
        self._stats_box = tk.Listbox(left, height=8)
        self._stats_box.grid(row=4, column=0, sticky="nsew", pady=(4, 10))

        ttk.Label(left, text="Skills").grid(row=5, column=0, sticky="w")
        self._skills_box = tk.Listbox(left, height=8)
        self._skills_box.grid(row=6, column=0, sticky="nsew", pady=(4, 0))

        # Center panel: chat
        center = ttk.Labelframe(body, text="Session", padding=10)
        center.grid(row=0, column=1, sticky="nsew", padx=(0, 8))
        center.rowconfigure(0, weight=1)
        center.columnconfigure(0, weight=1)

        self._chat = tk.Text(center, wrap="word", height=10, state="disabled")
        self._chat.grid(row=0, column=0, sticky="nsew")
        chat_scroll = ttk.Scrollbar(center, orient="vertical", command=self._chat.yview)
        chat_scroll.grid(row=0, column=1, sticky="ns")
        self._chat.configure(yscrollcommand=chat_scroll.set)

        input_row = ttk.Frame(center)
        input_row.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        input_row.columnconfigure(0, weight=1)

        self._input_var = tk.StringVar(value="")
        self._input_entry = ttk.Entry(input_row, textvariable=self._input_var)
        self._input_entry.grid(row=0, column=0, sticky="ew")

        self._send_btn = ttk.Button(input_row, text="Send", command=self._on_send)
        self._send_btn.grid(row=0, column=1, padx=(8, 0))

        cmd_row = ttk.Frame(center)
        cmd_row.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        cmd_row.columnconfigure(0, weight=1)

        ttk.Label(cmd_row, text="Command").grid(row=0, column=0, sticky="w")
        self._cmd_var = tk.StringVar(value="")
        self._cmd_entry = ttk.Entry(cmd_row, textvariable=self._cmd_var)
        self._cmd_entry.grid(row=1, column=0, sticky="ew")

        self._exec_btn = ttk.Button(cmd_row, text="Execute", command=self._on_execute_command)
        self._exec_btn.grid(row=1, column=1, padx=(8, 0))

        # Right panel: inventory and ground
        right = ttk.Labelframe(body, text="Inventory", padding=10)
        right.grid(row=0, column=2, sticky="nsew")
        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)

        inv_toolbar = ttk.Frame(right)
        inv_toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        inv_toolbar.columnconfigure(0, weight=1)

        self._max_carry_var = tk.DoubleVar(value=self.state.player.inventory.max_carry_kg)
        ttk.Label(inv_toolbar, text="Max carry (kg)").grid(row=0, column=0, sticky="w")
        self._max_carry_entry = ttk.Entry(inv_toolbar, textvariable=self._max_carry_var, width=10)
        self._max_carry_entry.grid(row=0, column=1, sticky="e")

        self._inv_box = tk.Listbox(right, height=10)
        self._inv_box.grid(row=1, column=0, sticky="nsew", pady=(0, 10))

        ground = ttk.Labelframe(right, text="Ground", padding=8)
        ground.grid(row=2, column=0, sticky="nsew")
        ground.rowconfigure(0, weight=1)
        ground.columnconfigure(0, weight=1)

        self._ground_box = tk.Listbox(ground, height=8)
        self._ground_box.grid(row=0, column=0, sticky="nsew")

        bottom = ttk.Frame(right)
        bottom.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        bottom.columnconfigure(0, weight=1)

        self._save_btn = ttk.Button(bottom, text="Save...", command=self._on_save)
        self._save_btn.grid(row=0, column=0, sticky="w")

        self._load_btn = ttk.Button(bottom, text="Load...", command=self._on_load)
        self._load_btn.grid(row=0, column=1, sticky="e")

    def _wire_events(self) -> None:
        """Bind keyboard shortcuts and UI events."""
        self._input_entry.bind("<Return>", lambda _e: self._on_send())
        self._cmd_entry.bind("<Return>", lambda _e: self._on_execute_command())

        self._player_name_entry.bind("<FocusOut>", lambda _e: self._apply_player_name())
        self._max_carry_entry.bind("<FocusOut>", lambda _e: self._apply_max_carry())

        # Double click inventory item to drop one to ground (fast interaction)
        self._inv_box.bind("<Double-Button-1>", lambda _e: self._drop_selected_inventory_item())

        # Double click ground item to pick it up (fast interaction)
        self._ground_box.bind("<Double-Button-1>", lambda _e: self._pick_selected_ground_item())

    # --------------------------
    # UI refresh
    # --------------------------

    def _refresh_all(self) -> None:
        """Refresh all UI elements from current state."""
        self._player_name_var.set(self.state.player.name)
        self._hp_var.set(f"HP: {self.state.player.hp_current}/{self.state.player.hp_max}")

        self._stats_box.delete(0, tk.END)
        for key, val in self.state.player.stats.items():
            self._stats_box.insert(tk.END, f"{key}: {val}")

        self._skills_box.delete(0, tk.END)
        for key, val in self.state.player.skills.items():
            self._skills_box.insert(tk.END, f"{key}: {val:+d}")

        self._inv_box.delete(0, tk.END)
        for it in self.state.player.inventory.items:
            self._inv_box.insert(tk.END, self._format_item_row(it))

        self._ground_box.delete(0, tk.END)
        for it in self.state.ground_items:
            self._ground_box.insert(tk.END, self._format_item_row(it))

        self._max_carry_var.set(self.state.player.inventory.max_carry_kg)

        carry = self.state.player.inventory.carry_weight_kg()
        max_carry = self.state.player.inventory.max_carry_kg
        self._hud_weight_var.set(f"Weight: {format_kg(carry)} / {format_kg(max_carry)}")

        self._hud_profile_var.set(f"Profile: {self.state.player.name}")

    @staticmethod
    def _format_item_row(it: Item) -> str:
        """Format an inventory listbox row."""
        qty = f"x{it.quantity}" if it.quantity != 1 else ""
        return f"{it.name} {qty} ({format_kg(it.total_weight_kg())})".strip()

    # --------------------------
    # Chat helpers
    # --------------------------

    def _chat_append(self, who: str, text: str) -> None:
        """Append a line to the chat box."""
        self._chat.configure(state="normal")
        self._chat.insert(tk.END, f"{who}: {text}\n")
        self._chat.see(tk.END)
        self._chat.configure(state="disabled")

    # --------------------------
    # Apply edits
    # --------------------------

    def _apply_player_name(self) -> None:
        """Apply player name from entry to state."""
        name = self._player_name_var.get().strip()
        if name:
            self.state.player.name = name
            self._refresh_all()

    def _apply_max_carry(self) -> None:
        """Apply max carry weight from entry to state."""
        try:
            value = float(self._max_carry_var.get())
        except (ValueError, tk.TclError):
            return

        value = max(0.0, value)
        self.state.player.inventory.max_carry_kg = value
        self._refresh_all()

    # --------------------------
    # Actions: send text, execute commands
    # --------------------------

    def _on_send(self) -> None:
        """Send user freeform text to DM (stub for now)."""
        text = self._input_var.get().strip()
        if not text:
            return
        self._input_var.set("")
        self._chat_append(self.state.player.name, text)

        if self._client is None:
            self._chat_append("DM", "Offline mode. Use commands like 'pick sword' or 'drop coin'.")
            return

        response = self._client.dm_respond(text)
        self._chat_append("DM", response)

    def _on_execute_command(self) -> None:
        """Execute a command typed into the command field."""
        line = self._cmd_var.get().strip()
        if not line:
            return
        self._cmd_var.set("")
        self._chat_append("CMD", line)

        verb, rest = parse_command(line)
        if not verb:
            return

        if verb == "pick":
            self._cmd_pick(rest)
        elif verb == "drop":
            self._cmd_drop(rest)
        elif verb == "move":
            self._cmd_move(rest)
        elif verb == "save":
            self._on_save()
        elif verb == "load":
            self._on_load()
        elif verb == "help":
            self._cmd_help()
        else:
            self._chat_append("SYS", f"Unknown command '{verb}'. Type 'help'.")

        self._refresh_all()

    def _cmd_help(self) -> None:
        """Show commands."""
        lines = [
            "Commands:",
            "  pick <item>              (catalog items only for now)",
            "  pick <qty> <item>",
            "  drop <item>",
            "  drop <qty> <item>",
            "  move <item> to ground    (same as drop)",
            "  move <item> to bag       (same as pick from ground, stub)",
            "  save                     (opens save dialog)",
            "  load                     (opens load dialog)",
        ]
        for ln in lines:
            self._chat_append("SYS", ln)

    def _cmd_pick(self, rest: str) -> None:
        """Pick an item into inventory (from catalog)."""
        qty, name = parse_quantity_and_name(rest)
        name = normalize_item_name(name)
        if not name:
            self._chat_append("SYS", "Usage: pick <item> or pick <qty> <item>")
            return

        item = item_from_catalog(name, quantity=qty)
        if item is None:
            self._chat_append("SYS", f"Unknown item '{name}'. Add it to tools.default_item_catalog().")
            return

        if not self.state.player.inventory.add(item):
            self._chat_append(
                "SYS",
                f"Too heavy. Need {format_kg(item.total_weight_kg())}, remaining {format_kg(self.state.player.inventory.remaining_kg())}.",
            )
            return

        self._chat_append("SYS", f"Picked up {item.name} x{item.quantity}.")

    def _cmd_drop(self, rest: str) -> None:
        """Drop an item from inventory to ground."""
        qty, name = parse_quantity_and_name(rest)
        name = normalize_item_name(name)
        if not name:
            self._chat_append("SYS", "Usage: drop <item> or drop <qty> <item>")
            return

        removed = self.state.player.inventory.remove_by_name(name, quantity=qty)
        if removed is None:
            self._chat_append("SYS", f"You do not have '{name}'.")
            return

        self.state.ground_items.append(removed)
        self._chat_append("SYS", f"Dropped {removed.name} x{removed.quantity} to ground.")

    def _cmd_move(self, rest: str) -> None:
        """
        Move item between containers (minimal parser for now).

        Examples:
        - move sword to ground
        - move coin to ground
        """
        text = rest.strip().lower()
        if " to " not in text:
            self._chat_append("SYS", "Usage: move <item> to ground|bag")
            return

        left, right = text.split(" to ", 1)
        item_name = normalize_item_name(left)
        target = normalize_item_name(right)

        if target == "ground":
            self._cmd_drop(item_name)
            return

        if target in ("bag", "inventory"):
            # Later: support moving from ground to inventory by name.
            self._chat_append("SYS", "move ... to bag is not implemented yet. Double-click a ground item to pick it up.")
            return

        self._chat_append("SYS", f"Unknown target '{target}'. Use ground or bag.")

    # --------------------------
    # Fast interactions (double click)
    # --------------------------

    def _drop_selected_inventory_item(self) -> None:
        """Drop one unit of the selected inventory item."""
        sel = self._inv_box.curselection()
        if not sel:
            return
        row = self._inv_box.get(sel[0])
        name = row.split(" (", 1)[0].strip()
        name = name.replace(" x", " ").split(" ", 1)[0].strip()
        self._cmd_drop(name)
        self._refresh_all()

    def _pick_selected_ground_item(self) -> None:
        """Pick up one unit of the selected ground item."""
        sel = self._ground_box.curselection()
        if not sel:
            return
        it = self.state.ground_items[sel[0]]
        # remove one from ground and add to inventory
        qty = 1
        if it.quantity > qty:
            it.quantity -= qty
            moved = Item(name=it.name, weight_kg=it.weight_kg, quantity=qty, notes=it.notes)
        else:
            moved = self.state.ground_items.pop(sel[0])

        if not self.state.player.inventory.add(moved):
            # revert
            self.state.ground_items.append(moved)
            self._chat_append(
                "SYS",
                f"Too heavy to pick up. Remaining {format_kg(self.state.player.inventory.remaining_kg())}.",
            )
            self._refresh_all()
            return

        self._chat_append("SYS", f"Picked up {moved.name} x{moved.quantity} from ground.")
        self._refresh_all()

    # --------------------------
    # Save and load
    # --------------------------

    def _on_save(self) -> None:
        """Save game to savegames/<name>.json."""
        name = self.state.player.name.strip() or "Player"
        default_filename = f"{name}.json"
        path = os.path.join(Config.SAVEGAMES_DIR, default_filename)

        answer = simpledialog.askstring("Save", "Save file name (without path):", initialvalue=default_filename, parent=self.root)
        if not answer:
            return

        filename = answer.strip()
        if not filename.lower().endswith(".json"):
            filename += ".json"
        path = os.path.join(Config.SAVEGAMES_DIR, filename)

        try:
            save_game(path, self.state)
            self._hud_status_var.set(f"Saved: {filename}")
        except OSError as exc:
            messagebox.showerror("Save failed", str(exc))

    def _on_load(self) -> None:
        """Load game from savegames folder by filename prompt."""
        answer = simpledialog.askstring("Load", "Load file name from savegames:", parent=self.root)
        if not answer:
            return

        filename = answer.strip()
        if not filename.lower().endswith(".json"):
            filename += ".json"
        path = os.path.join(Config.SAVEGAMES_DIR, filename)

        if not os.path.isfile(path):
            messagebox.showerror("Not found", f"File not found: {filename}")
            return

        try:
            self.state = load_game(path)
            self._hud_status_var.set(f"Loaded: {filename}")
            self._refresh_all()
        except (OSError, ValueError) as exc:
            messagebox.showerror("Load failed", str(exc))