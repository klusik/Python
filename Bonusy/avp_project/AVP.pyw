"""ACARS Virtual Printer entry point.

This module starts the tray application, the local RAW print receiver,
and the Tkinter settings window controller.
"""

import traceback
import tkinter as tk
from tkinter import messagebox

from src.app import ACARSVirtualPrinterApp
from src.constants import APP_NAME


def _show_fatal_error(error):
    """Display a fatal startup error even when launched through pythonw."""
    hidden_root = tk.Tk()
    hidden_root.withdraw()
    messagebox.showerror(
        APP_NAME,
        f"{error}\n\n{traceback.format_exc()}",
        parent=hidden_root,
    )
    hidden_root.destroy()


def main():
    """Start the application."""
    try:
        application = ACARSVirtualPrinterApp()
        application.run()
    except Exception as error:
        _show_fatal_error(error)


if __name__ == "__main__":
    main()
