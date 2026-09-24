"""
DnDGame.pyw

Main entry point for the Tkinter DnD assistant app.
Keeps the root module minimal, delegates to src.app.App.

Run:
- Windows: double-click .pyw
- Terminal: python DnDGame.pyw
"""

from __future__ import annotations

import os
import sys


def _ensure_src_on_path() -> None:
    """Ensure ./src is importable when launching from the project root."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(root_dir, "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)


def main() -> None:
    """Program entry point."""
    _ensure_src_on_path()

    from app import App  # pylint: disable=import-error

    app = App()
    app.run()


if __name__ == "__main__":
    main()