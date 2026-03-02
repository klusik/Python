"""
tools.py

Utilities: parsing commands, formatting, safe IO, item database.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from typing import Dict, Optional, Tuple

from models import GameState, Inventory, Item, Player, WorldState


def format_kg(value: float) -> str:
    """Format kg with sensible precision."""
    if abs(value) < 10:
        return f"{value:.2f} kg"
    return f"{value:.1f} kg"


def normalize_item_name(text: str) -> str:
    """Normalize user-entered item names."""
    return " ".join(text.strip().split())


def parse_command(line: str) -> Tuple[str, str]:
    """
    Parse command line into (verb, rest).

    Examples:
    - "pick sword" -> ("pick", "sword")
    - "drop 2 coin" -> ("drop", "2 coin")
    """
    raw = line.strip()
    if not raw:
        return "", ""
    parts = raw.split(maxsplit=1)
    verb = parts[0].lower().strip()
    rest = parts[1].strip() if len(parts) > 1 else ""
    return verb, rest


def parse_quantity_and_name(rest: str) -> Tuple[int, str]:
    """
    Parse optional leading integer quantity.

    "2 coin" -> (2, "coin")
    "coin" -> (1, "coin")
    """
    text = rest.strip()
    if not text:
        return 1, ""
    parts = text.split(maxsplit=1)
    if parts and parts[0].isdigit():
        qty = max(1, int(parts[0]))
        name = parts[1].strip() if len(parts) > 1 else ""
        return qty, name
    return 1, text


def default_item_catalog() -> Dict[str, float]:
    """
    Basic realistic-ish weight catalog.

    You will likely replace this with a proper database and item instances.
    """
    return {
        "sword": 2.0,
        "dagger": 0.5,
        "shield": 6.0,
        "leather armor": 10.0,
        "chainmail": 20.0,
        "coin": 0.005,  # 5 g
        "torch": 0.3,
        "rope": 3.0,
        "ration": 0.5,
        "potion": 0.2,
    }


def item_from_catalog(name: str, quantity: int = 1) -> Optional[Item]:
    """Create an Item from catalog if known, else None."""
    name_norm = normalize_item_name(name).lower()
    catalog = default_item_catalog()
    if name_norm not in catalog:
        return None
    return Item(name=name_norm, weight_kg=float(catalog[name_norm]), quantity=int(quantity))


def gamestate_to_dict(state: GameState) -> Dict:
    """Convert GameState to JSON-serializable dict."""
    return asdict(state)


def gamestate_from_dict(data: Dict) -> GameState:
    """Build GameState from dict produced by gamestate_to_dict()."""
    inv_data = data.get("player", {}).get("inventory", {})
    inv = Inventory(
        max_carry_kg=float(inv_data.get("max_carry_kg", 30.0)),
        items=[Item(**it) for it in inv_data.get("items", [])],
    )

    p_data = data.get("player", {})
    player = Player(
        name=str(p_data.get("name", "Player")),
        level=int(p_data.get("level", 1)),
        hp_current=int(p_data.get("hp_current", 10)),
        hp_max=int(p_data.get("hp_max", 10)),
        stats=dict(p_data.get("stats", {})),
        skills=dict(p_data.get("skills", {})),
        inventory=inv,
    )

    w_data = data.get("world", {})
    world = WorldState(
        location=str(w_data.get("location", "Unknown")),
        time=str(w_data.get("time", "Unknown")),
        summary=str(w_data.get("summary", "")),
        plot_points=list(w_data.get("plot_points", [])),
    )

    ground_items = [Item(**it) for it in data.get("ground_items", [])]
    return GameState(player=player, world=world, ground_items=ground_items)


def save_game(path: str, state: GameState) -> None:
    """Save a game state to JSON."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    payload = gamestate_to_dict(state)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def load_game(path: str) -> GameState:
    """Load a game state from JSON."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return gamestate_from_dict(data)