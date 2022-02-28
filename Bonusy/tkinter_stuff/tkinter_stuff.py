"""
    Learning with TKInter
"""

# IMPORTS
import tkinter as tk

# CONFIG
FRAME_BG = "#ABCDEF"
W_DIMENSIONS = "600x600"

# CLASSES
class App:
    def __init__(self):
        # Window
        self.window = tk.Tk()
        self.window.geometry(W_DIMENSIONS)
        self.window.title("Test TK")
        
        # Frame
        self.frame = tk.Frame(self.window, bg=FRAME_BG)

        self.frame.pack(expand=True, fill="both")
        self.frame.update()

    def run(self):
        self.window.mainloop()

# RUNTIME
def main():
    app = App()

    app.run()

if __name__ == "__main__":
    main()