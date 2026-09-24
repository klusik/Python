"""
    Registration plates recognizer

    Author: klusik@klusik.cz (2023, 2024)
"""

# IMPORTS #
from src.Tools import Tools
from src.Window import MainWindow


class App:
    def __init__(self):
        self.main_window = MainWindow()

    def run(self):
        self.main_window.run()


if __name__ == "__main__":
    app = App()
    app.run()
