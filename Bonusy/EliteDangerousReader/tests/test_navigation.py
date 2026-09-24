"""Tests for the top-level navigation policy."""

from elite_reader.navigation import evaluate_navigation, normalize_start_url


def test_main_domain_is_allowed() -> None:
    """The official HTTPS host is accepted."""

    assert evaluate_navigation("https://www.elitedangerous.com/update-notes").allowed


def test_subdomain_is_allowed() -> None:
    """Approved subdomains remain usable if the site introduces them."""

    assert evaluate_navigation("https://news.elitedangerous.com/path").allowed


def test_similar_domain_is_rejected() -> None:
    """Suffix confusion must not permit attacker-controlled hosts."""

    assert not evaluate_navigation("https://elitedangerous.com.example.org/").allowed
    assert not evaluate_navigation("https://notelitedangerous.com/").allowed


def test_non_https_scheme_is_rejected() -> None:
    """The reader does not allow HTTP, file, or custom schemes."""

    assert not evaluate_navigation("http://www.elitedangerous.com/").allowed
    assert not evaluate_navigation("file:///C:/temp/page.html").allowed


def test_invalid_start_url_raises() -> None:
    """A rejected command-line URL fails before the window is created."""

    try:
        normalize_start_url("https://example.com/")
    except ValueError as exc:
        assert "rejected" in str(exc).lower()
    else:
        raise AssertionError("Expected ValueError")
