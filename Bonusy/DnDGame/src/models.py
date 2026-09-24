"""
models.py

Game state models (player, items, inventory).
These are the authoritative state objects stored in savegames.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Item:
    """A single item instance."""

    name: str
    weight_kg: float
    quantity: int = 1
    notes: str = ""

    def total_weight_kg(self) -> float:
        """Return total weight (weight per piece times quantity)."""
        return float(self.weight_kg) * int(self.quantity)


@dataclass
class Inventory:
    """
    Inventory container with carry limit.

    Note: This is not a grid-based Diablo2 inventory yet.
    For now we keep it list-based; the UI is prepared for future drag/drop.
    """

    max_carry_kg: float
    items: List[Item] = field(default_factory=list)

    def carry_weight_kg(self) -> float:
        """Compute total carried weight."""
        return sum(it.total_weight_kg() for it in self.items)

    def remaining_kg(self) -> float:
        """Return remaining capacity."""
        return self.max_carry_kg - self.carry_weight_kg()

    def can_add(self, item: Item) -> bool:
        """Check whether an item can be added without exceeding capacity."""
        return (self.carry_weight_kg() + item.total_weight_kg()) <= self.max_carry_kg + 1e-9

    def add(self, item: Item) -> bool:
        """
        Add an item. If same name and weight, stacks by quantity.

        Returns True if added, False if capacity exceeded.
        """
        if not self.can_add(item):
            return False

        for existing in self.items:
            if existing.name.lower() == item.name.lower() and abs(existing.weight_kg - item.weight_kg) < 1e-9:
                existing.quantity += item.quantity
                return True

        self.items.append(item)
        return True

    def remove_by_name(self, name: str, quantity: int = 1) -> Optional[Item]:
        """
        Remove quantity of item by name (case-insensitive).
        Returns removed Item (with quantity removed) or None if not found.
        """
        name_norm = name.strip().lower()
        if not name_norm:
            return None

        for idx, existing in enumerate(self.items):
            if existing.name.lower() == name_norm:
                qty = max(1, int(quantity))
                if existing.quantity > qty:
                    existing.quantity -= qty
                    return Item(name=existing.name, weight_kg=existing.weight_kg, quantity=qty, notes=existing.notes)

                removed = self.items.pop(idx)
                return removed

        return None


@dataclass
class Player:
    """Player character profile."""

    name: str
    level: int = 1
    hp_current: int = 10
    hp_max: int = 10
    stats: Dict[str, int] = field(default_factory=lambda: {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10})
    skills: Dict[str, int] = field(default_factory=lambda: {"Perception": 0, "Stealth": 0, "Arcana": 0, "Athletics": 0})
    inventory: Inventory = field(default_factory=lambda: Inventory(max_carry_kg=30.0))


@dataclass
class WorldState:
    """World, location, and narrative summary."""

    location: str = "Unknown"
    time: str = "Unknown"
    summary: str = ""
    plot_points: List[str] = field(default_factory=list)


@dataclass
class GameState:
    """
    Full savegame state.

    This is what you serialize.
    """

    player: Player
    world: WorldState = field(default_factory=WorldState)

    # A simple "ground" container for now (items not carried).
    ground_items: List[Item] = field(default_factory=list)