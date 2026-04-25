"""Windowed launcher for the YouTube Downloader application."""

from src.runtime_environment import configure_runtime_environment
from src.startup_error import StartupError


def main() -> None:
    """Start the Tkinter application without opening a console window."""
    configure_runtime_environment()

    try:
        from src.app import App
    except ModuleNotFoundError as exc:
        if exc.name == "_tkinter":
            StartupError().show(
                "Tkinter Is Missing",
                "This Python installation was built without Tkinter support.\n\n"
                "Install a Python build that includes Tkinter, then run the app again.\n\n"
                "On Homebrew Python, try installing the matching python-tk package. "
                "For example: brew install python-tk@3.14",
            )
            return

        raise

    app: App = App()
    app.run()


if __name__ == "__main__":
    main()
