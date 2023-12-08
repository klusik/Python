"""
    TK window
"""

import tkinter as tk


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Registration Plates Recognizer")
        self.root.geometry("800x600")  # width x height

    def run(self):
        self.root.mainloop()
