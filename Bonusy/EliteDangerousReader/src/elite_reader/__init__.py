"""Elite Dangerous Reader package.

The package provides a narrowly scoped desktop reader for the official Elite
Dangerous website. It uses the installed Microsoft Edge WebView2 runtime through
pywebview and injects a configurable readability layer into approved pages.
"""

from .version import __version__

__all__ = ["__version__"]
