"""Utility helpers for running background work from the Tkinter UI."""

import threading
from typing import Callable


class BackgroundTaskRunner:
    """Run background tasks without blocking the Tkinter event loop."""

    def run(self, target_callable: Callable[[], None]) -> None:
        """Start the given callable on a daemon thread."""
        worker_thread = threading.Thread(target=target_callable, daemon=True)
        worker_thread.start()
