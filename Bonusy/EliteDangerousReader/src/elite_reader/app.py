"""Application lifecycle and WebView2 integration."""

from __future__ import annotations

import logging
from typing import Any

import webview

from .api import ReaderApi
from .config import SettingsStore
from .constants import (
    APP_NAME,
    HOME_URL,
    WINDOW_BACKGROUND_COLOR,
    WINDOW_HEIGHT,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_WIDTH,
)
from .native_guard import NativeNavigationGuard
from .navigation import evaluate_navigation, normalize_start_url
from .paths import user_webview_directory
from .theme import build_injection_script
from .version import __version__


class EliteReaderApplication:
    """Own the desktop window, navigation policy, and page customization."""

    def __init__(
        self,
        *,
        start_url: str | None,
        debug: bool,
        store: SettingsStore,
        logger: logging.Logger,
    ) -> None:
        """Initialize the application without starting the GUI loop.

        :param start_url: Optional approved initial URL.
        :param debug: Enable WebView2 development tools and verbose diagnostics.
        :param store: Persistent settings store.
        :param logger: Application logger.
        """

        self._start_url = normalize_start_url(start_url)
        self._debug = debug
        self._store = store
        self._logger = logger
        self._api = ReaderApi(store, logger)
        self._window: Any | None = None
        self._native_guard: NativeNavigationGuard | None = None
        self._last_allowed_url = self._start_url

    def run(self) -> None:
        """Create the reader window and enter the pywebview GUI loop."""

        self._configure_webview_security_settings()
        self._window = webview.create_window(
            title=f"{APP_NAME} {__version__}",
            url=self._start_url,
            js_api=self._api,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            min_size=(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT),
            resizable=True,
            text_select=True,
            zoomable=True,
            background_color=WINDOW_BACKGROUND_COLOR,
            confirm_close=False,
        )
        self._native_guard = NativeNavigationGuard(self._window, self._logger)
        self._window.events.before_show += self._on_before_show
        self._window.events.loaded += self._on_loaded

        self._logger.info("Starting %s at %s", APP_NAME, self._start_url)
        webview.start(
            gui="edgechromium",
            debug=self._debug,
            private_mode=False,
            storage_path=str(user_webview_directory()),
        )

    def _configure_webview_security_settings(self) -> None:
        """Disable features unnecessary for this single-purpose reader."""

        webview.settings["ALLOW_DOWNLOADS"] = False
        webview.settings["ALLOW_FILE_URLS"] = False
        webview.settings["OPEN_EXTERNAL_LINKS_IN_BROWSER"] = False
        webview.settings["REMOTE_DEBUGGING_PORT"] = None
        webview.settings["OPEN_DEVTOOLS_IN_DEBUG"] = self._debug

    def _on_before_show(self) -> None:
        """Install the native navigation guard before the window is displayed."""

        if self._native_guard is not None:
            self._native_guard.install()

    def _on_loaded(self) -> None:
        """Validate the loaded URL and inject the reader interface."""

        if self._window is None:
            return

        current_url = str(self._window.get_current_url() or "")
        decision = evaluate_navigation(current_url)
        if not decision.allowed:
            self._logger.warning(
                "Post-load guard rejected %s: %s",
                current_url,
                decision.reason,
            )
            self._window.load_url(self._last_allowed_url or HOME_URL)
            return

        self._last_allowed_url = current_url
        try:
            settings = self._store.load()
            script = build_injection_script(settings)
            self._window.run_js(script)
            self._logger.debug("Reader interface injected into %s", current_url)
        except Exception:
            self._logger.exception("Failed to inject reader interface")
