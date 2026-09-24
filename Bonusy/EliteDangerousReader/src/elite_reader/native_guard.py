"""Best-effort native Microsoft Edge WebView2 navigation enforcement."""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from .navigation import evaluate_navigation


class NativeNavigationGuard:
    """Cancel top-level WebView2 navigation outside the approved domain.

    pywebview intentionally presents a cross-platform abstraction and does not
    expose a cancellable navigation event. On Windows, the underlying WebView2
    control is available through ``window.native.webview``. This class attaches
    directly to its .NET events while retaining a post-load fallback in the main
    application for compatibility.
    """

    def __init__(self, window: Any, logger: logging.Logger) -> None:
        """Initialize the guard.

        :param window: pywebview Window instance.
        :param logger: Application logger.
        """

        self._window = window
        self._logger = logger
        self._control: Any | None = None
        self._core: Any | None = None
        self._installed = False
        self._handlers: list[Callable[..., Any]] = []

    def install(self) -> None:
        """Attach native handlers when the Edge WebView2 control is available."""

        if self._installed:
            return

        try:
            native = self._window.native
            control = native.webview
            self._control = control
            control.NavigationStarting += self._on_navigation_starting
            control.CoreWebView2InitializationCompleted += self._on_core_initialized
            self._handlers.extend([self._on_navigation_starting, self._on_core_initialized])
            self._installed = True
            self._logger.info("Native WebView2 navigation guard installed")

            core = getattr(control, "CoreWebView2", None)
            if core is not None:
                self._attach_core_handlers(core)
        except Exception as exc:
            self._logger.warning(
                "Native navigation guard unavailable; using fallback guard: %s",
                exc,
            )

    def _on_navigation_starting(self, _sender: Any, args: Any) -> None:
        """Cancel disallowed top-level navigation before content is loaded."""

        try:
            url = str(args.Uri)
            decision = evaluate_navigation(url, allow_startup_pages=True)
            if decision.allowed:
                return
            args.Cancel = True
            self._logger.warning("Blocked navigation to %s: %s", url, decision.reason)
        except Exception as exc:
            self._logger.exception("Navigation guard failed closed: %s", exc)
            try:
                args.Cancel = True
            except Exception:
                return

    def _on_core_initialized(self, sender: Any, args: Any) -> None:
        """Attach handlers that require an initialized CoreWebView2 instance."""

        try:
            if not bool(args.IsSuccess):
                self._logger.error("WebView2 core initialization failed")
                return
            self._attach_core_handlers(sender.CoreWebView2)
        except Exception as exc:
            self._logger.warning("Could not attach CoreWebView2 handlers: %s", exc)

    def _attach_core_handlers(self, core: Any) -> None:
        """Install the new-window guard exactly once.

        :param core: Initialized CoreWebView2 .NET object.
        """

        if self._core is core:
            return
        self._core = core

        try:
            browser = getattr(self._window.native, "browser", None)
            pywebview_handler = getattr(browser, "on_new_window_request", None)
            if pywebview_handler is not None:
                core.NewWindowRequested -= pywebview_handler
        except Exception:
            self._logger.debug(
                "pywebview new-window handler could not be removed",
                exc_info=True,
            )

        core.NewWindowRequested += self._on_new_window_requested
        self._handlers.append(self._on_new_window_requested)
        self._logger.debug("CoreWebView2 new-window guard attached")

    def _on_new_window_requested(self, _sender: Any, args: Any) -> None:
        """Open approved new-window links in the current reader window."""

        try:
            url = str(args.Uri)
            args.Handled = True
            decision = evaluate_navigation(url)
            if decision.allowed:
                self._logger.info("Redirecting approved new-window link: %s", url)
                self._window.load_url(url)
            else:
                self._logger.warning(
                    "Blocked new-window navigation to %s: %s",
                    url,
                    decision.reason,
                )
        except Exception as exc:
            self._logger.exception("New-window guard failure: %s", exc)
            try:
                args.Handled = True
            except Exception:
                return
