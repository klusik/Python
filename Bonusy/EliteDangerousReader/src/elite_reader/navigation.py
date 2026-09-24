"""URL validation and navigation policy."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

from .constants import ALLOWED_BASE_DOMAIN, ALLOWED_SCHEMES, HOME_URL


@dataclass(frozen=True, slots=True)
class NavigationDecision:
    """Result of evaluating a candidate top-level URL."""

    allowed: bool
    reason: str


def is_allowed_host(hostname: str | None) -> bool:
    """Return whether a host belongs to the approved Elite Dangerous domain.

    :param hostname: Parsed hostname, with or without case normalization.
    :return: True for ``elitedangerous.com`` and its subdomains.
    """

    normalized = (hostname or "").strip().lower().rstrip(".")
    return normalized == ALLOWED_BASE_DOMAIN or normalized.endswith("." + ALLOWED_BASE_DOMAIN)


def evaluate_navigation(url: str, *, allow_startup_pages: bool = False) -> NavigationDecision:
    """Evaluate a candidate top-level navigation.

    :param url: Absolute URL supplied by WebView2 or the command line.
    :param allow_startup_pages: Allow transient ``about:blank`` startup pages.
    :return: Decision with an audit-friendly reason.
    """

    candidate = str(url or "").strip()
    if allow_startup_pages and candidate in {"", "about:blank"}:
        return NavigationDecision(True, "transient startup page")

    parsed = urlparse(candidate)
    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        return NavigationDecision(False, "only HTTPS navigation is allowed")
    if not is_allowed_host(parsed.hostname):
        return NavigationDecision(False, "host is outside elitedangerous.com")
    if parsed.username or parsed.password:
        return NavigationDecision(False, "credential-bearing URLs are not allowed")
    return NavigationDecision(True, "approved Elite Dangerous URL")


def normalize_start_url(url: str | None) -> str:
    """Validate and normalize a requested startup URL.

    :param url: Optional startup URL from the command line.
    :return: Approved startup URL, defaulting to the update notes index.
    :raises ValueError: If a supplied URL violates the navigation policy.
    """

    candidate = (url or HOME_URL).strip()
    decision = evaluate_navigation(candidate)
    if not decision.allowed:
        raise ValueError(f"Startup URL rejected: {decision.reason}")
    return candidate
