"""
    Klick timer :-D

"""

# IMPORTS #
import tkinter
import tkinter.ttk

# CLASSES #
class Pushuper(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

# RUNTIME #

if __name__ == "__main__":
    main_window = Pushuper()

    main_window.master.title("Pushups for MathSessions")
    main_window.master.maxsize(400, 200)
    main_window.master.minsize(400, 200)
    main_window.mainloop()