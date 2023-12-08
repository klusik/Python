"""
    TK window
"""

import tkinter as tk
from tkinter import filedialog
import os


class MainWindow:
    """
    Main application window class for the Registration Plates Recognizer.

    This class creates and manages the main GUI window using Tkinter. It includes
    a button for browsing directories and an embossed text field to display the
    selected directory path.
    """

    def __init__(self):
        """
        Initializes the main window.
        """
        self.root = tk.Tk()
        self.selected_path = tk.StringVar(value=os.getcwd())  # Default path is the current working directory
        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the user interface components of the main window.
        """
        self.root.title("Registration Plates Recognizer")
        self.root.geometry("1200x100")  # width x height

        # Not resizable
        self.root.resizable(False, False)

        # Create a frame to hold the text field and the browse button
        directory_frame = tk.Frame(self.root)
        directory_frame.pack(pady=20)

        # Embossed text field
        path_display = tk.Entry(directory_frame, textvariable=self.selected_path, relief="sunken", state='readonly',
                                width=150)
        path_display.grid(row=0, column=0, padx=(10, 0), pady=10, sticky='we')

        # Browse button
        browse_button = tk.Button(directory_frame, text="Browse", command=self.browse_directory)
        browse_button.grid(row=0, column=1, padx=(5, 10), pady=10)

    def browse_directory(self):
        """
        Opens a file dialog to browse for a directory and updates the path display.
        """
        directory = filedialog.askdirectory()
        if directory:  # Update only if a directory is selected
            self.selected_path.set(directory)

    def run(self):
        """
        Runs the main loop of the Tkinter window.
        """
        self.root.mainloop()
