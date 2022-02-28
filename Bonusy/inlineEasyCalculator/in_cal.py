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
WINDOW_DIMENSIONS = "450x600"
DISPLAY_HEIGHT = 150
RIGHT_PADDING = 30

SMALL_FONT = ("Arial", 16)
LARGE_FONT = ("Arial", 30)
KEYBOARD_FONT = ("Arial", 30)
DEFAULT_FONT = ("Arial", 20)

DISPLAY_COLOR = "#CCCCCC"
LABEL_COLOR = "#25265C"
BUTTON_COLOR = "#FFFFFF"
OPERATOR_COLOR = "#ABCDEF"


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
        self.total = ""
        self.current = ""

        # FRAMES #

        # Display frame
        self.display_f = self.create_display_frame()
        self.total_label, self.current_label = self.create_display_labels()

        # Keyboard frame

        # Digits
        # It uses coordinates on which the numbers
        # later will be displayed.
        # Layout is standard as on the numerical keyboard
        # on the computer
        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1),
        }
        self.operators = {
            '/': '\u00F7',
            '*': '×',
            '-': '-',
            '+': '+',
        }
        self.buttons_f = self.create_button_frame()

        # Filling the empty spaces with buttons
        for num in range(1, 5):
            self.buttons_f.rowconfigure(num, weight=1)
            self.buttons_f.columnconfigure(num, weight=1)

        self.buttons_f.rowconfigure(0, weight=1)  # Zero on the bottom

        self.create_keyboard()
        self.create_operator_buttons()
        self.create_clear_button()
        self.create_equals_button()

    def update_total_label(self):
        """ Updates the total label number """
        self.total_label.config(text=self.total)

    def update_current_label(self):
        """ Updates the current label number """
        self.current_label.config(text=self.current)

    def add_to_current(self, value):
        """ Updates the expression """
        self.current += str(value)
        self.update_current_label()

    def append_operator(self, operator):
        """ Appends an operator to current """
        self.current += operator
        self.total += self.current
        self.current = ""
        self.update_total_label()
        self.update_current_label()

    def clear(self):
        """ Clears display """
        self.current = self.total = ""
        self.update_total_label()
        self.update_current_label()

    def create_keyboard(self):
        """ Creates buttons """
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_f, text=str(digit),
                               bg=BUTTON_COLOR, fg=LABEL_COLOR, font=KEYBOARD_FONT, borderwidth=0,
                               command=lambda x=digit: self.add_to_current(x))

            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def create_operator_buttons(self):
        """ Creates the button for division, multiplication and so on """
        row = 0
        for operator, symbol in self.operators.items():
            button = tk.Button(self.buttons_f, text=symbol,
                               bg=OPERATOR_COLOR, fg=LABEL_COLOR, font=DEFAULT_FONT, borderwidth=0,
                               command=lambda x=operator: self.append_operator(x))

            button.grid(row=row, column=4, sticky=tk.NSEW)
            row += 1

    def create_clear_button(self):
        """ Creates 'C' button """
        button = tk.Button(self.buttons_f, text='C',
                           bg=OPERATOR_COLOR, fg=LABEL_COLOR, font=DEFAULT_FONT, borderwidth=0,
                           command=self.clear)

        button.grid(row=0, column=1, sticky=tk.NSEW, columnspan=3)

    def create_equals_button(self):
        """ Creates '=' button """
        button = tk.Button(self.buttons_f, text='=',
                           bg=OPERATOR_COLOR, fg=LABEL_COLOR, font=DEFAULT_FONT, borderwidth=0,
                           command=self.evaluate)

        button.grid(row=4, column=3, sticky=tk.NSEW, columnspan=2)

    def create_display_labels(self):
        """ Creates a numbers (current & total) and returns their frames """

        # Number total
        total_label = tk.Label(self.display_f, text=self.total, anchor=tk.E,
                               bg=DISPLAY_COLOR, fg=LABEL_COLOR, padx=RIGHT_PADDING,
                               font=SMALL_FONT)

        total_label.pack(expand=True, fill="both")

        # Number current
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

    def evaluate(self):
        """ Evaluates the result """
        self.total += self.current

        try:
            self.current = str(eval(self.total))
            self.total = ""
        except ZeroDivisionError:
            self.current = "Error (Zero division)"
        finally:
            self.update_current_label()

        self.update_total_label()
        self.update_current_label()

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
