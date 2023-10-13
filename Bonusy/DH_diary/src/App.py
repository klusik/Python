"""
    Main app window
"""

from .Window import Window


class App:
    def __init__(self):
        window = Window()
        window.run()
