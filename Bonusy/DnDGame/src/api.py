"""
api.py

OpenAI API wrapper.

Note:
- The actual request format and model selection will be implemented later.
- For now, this is a stub so the GUI can call it in a predictable way.

Design goal:
- Keep API access isolated from UI and game logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class ApiConfig:
    """Runtime API configuration (in-memory unless explicitly stored)."""

    api_key: str
    store_key: bool = False
    model: str = "gpt-5.2-nano"  # placeholder name; you will set the real one later


class OpenAIClient:
    """Thin wrapper around OpenAI API calls (to be implemented)."""

    def __init__(self, cfg: ApiConfig) -> None:
        self._cfg = cfg

    @property
    def config(self) -> ApiConfig:
        """Return current API config."""
        return self._cfg

    def dm_respond(self, prompt: str) -> str:
        """
        Generate DM response for a given prompt.

        For now returns a placeholder. Next step: implement a real call and structured output.
        """
        _ = prompt
        return "DM (stub): API not wired yet. Type commands like 'pick sword' or 'drop coin'."