from __future__ import annotations

import json
from typing import Any
from config import SAVE_PATH
from game_state import GameState

def save_game(gs: GameState) -> None:
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(gs.to_dict(), f, indent=2)

def load_game() -> GameState:
    with open(SAVE_PATH, "r", encoding="utf-8") as f:
        data: Any = json.load(f)
    return GameState.from_dict(data)
