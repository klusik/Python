"""
    Learning with TKInter
"""

# IMPORTS
import tkinter as tk

# CLASSES
class App:
    def __init__(self):
        self.window = tk.Tk()

    def run(self):
        self.window.mainloop()

# RUNTIME
def main():
    app = App()

    app.run()

if __name__ == "__main__":
    main()