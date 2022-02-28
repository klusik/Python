"""
    Based on 'pyladies'

    Basic inline calculator with +, -, * and /

    () in the Future :-)

    Implements Shunting-yard algorithm: https://en.wikipedia.org/wiki/Shunting-yard_algorithm

    Or maybe not, (we'll see what will be used) :-D

    Author:     klusik 2022
"""

# IMPORTS #
import tkinter as tk

# CONFIG #
WINDOW_DIMENSIONS = "400x600"
DISPLAY_HEIGHT = 150
RIGHT_PADDING = 30

SMALL_FONT = ("Arial", 16)
LARGE_FONT = ("Arial", 30)

DISPLAY_COLOR = "#CCCCCC"
LABEL_COLOR = "#25265C"

# CLASSES #
class Calculator:
    def __init__(self):

        # Specify the window
        self.window = tk.Tk()

        # Specify the size of the window
        self.window.geometry(WINDOW_DIMENSIONS)
        self.window.resizable(False, False)
        self.window.title("Awesome klusculator")

        # Default display values
        self.total = "0"
        self.current = "0"

        # Frames
        self.display_f = self.create_display_frame()

        self.total_label, self.current_label = self.create_display_labels()

        self.buttons_f = self.create_button_frame()

    def create_display_labels(self):
        total_label = tk.Label(self.display_f, text=self.total, anchor=tk.E,
                               bg=DISPLAY_COLOR, fg=LABEL_COLOR, padx=RIGHT_PADDING,
                               font=SMALL_FONT)

        total_label.pack(expand=True, fill="both")

        current_label = tk.Label(self.display_f, text=self.current, anchor=tk.E,
                               bg=DISPLAY_COLOR, fg=LABEL_COLOR, padx=RIGHT_PADDING,
                               font=LARGE_FONT)

        current_label.pack(expand=True, fill="both")

        return total_label, current_label


    def create_display_frame(self):
        """ Creates a frame for a display numbers """
        frame = tk.Frame(self.window, height=DISPLAY_HEIGHT, bg=DISPLAY_COLOR)
        frame.pack(expand=True, fill="both")

        return frame

    def create_button_frame(self):
        """ Creates a frame for keyboard """
        frame = tk.Frame(self.window, height=400)
        frame.pack(expand=True, fill="both")

        return frame

    def run(self):
        self.window.mainloop()


# RUNTIME #
def main():
    # Creating a window
    calculator = Calculator()

    # Loops the loop
    calculator.run()

if __name__ == "__main__":
    main()