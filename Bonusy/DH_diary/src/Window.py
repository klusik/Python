"""
    Window class
"""

import tkinter as tk
from tkinter import Menu, Text, Toplevel


class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Dračí hlídka Diary")

        # Setup menu
        self._setup_menu()

        # Display panel
        self.display_panel = Text(self.root, wrap=tk.WORD)
        self.display_panel.pack(expand=True, fill=tk.BOTH)

    def _setup_menu(self):
        # Create Menu
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)

        # File menu options
        self.file_menu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # Edit menu options
        self.edit_menu = Menu(self.menu)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Add Journal Entry", command=self._add_journal_entry)
        self.edit_menu.add_command(label="Edit Items", command=self._edit_items)
        # ... Add other options as needed

    def _add_journal_entry(self):
        # Logic to add a journal entry
        top = Toplevel(self.root)
        top.title("Add Journal Entry")
        tk.Label(top, text="This is where you add a journal entry").pack()

    def _edit_items(self):
        # Logic to edit items
        top = Toplevel(self.root)
        top.title("Edit Items")
        tk.Label(top, text="This is where you edit items").pack()

    # ... Add other methods as needed

    def run(self):
        self.root.mainloop()
