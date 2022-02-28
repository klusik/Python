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


# CLASSES #
class Calculator:
    def __init__(self):

        # Specify the window
        self.window = tk.Tk()

        # Specify the size of the window
        self.window.geometry("400x600")
        self.window.resizable(False, False)
        self.window.title("Awesome klusculator")

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