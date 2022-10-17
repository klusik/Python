"""
    Klick timer :-D

"""

# IMPORTS #
import tkinter
import tkinter.ttk

# CLASSES #
class Pushuper():
    def __init__(self, master=None):
        main_window = tkinter.Tk()

        main_window.title("Pushups for MathSessions")
        main_window.maxsize(400, 200)
        main_window.minsize(400, 200)

        # Setting up a labels
        
        main_window.mainloop()
# RUNTIME #

if __name__ == "__main__":
    app = Pushuper()
