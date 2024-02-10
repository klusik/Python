"""
    Just some TK stuff
"""
# IMPORTS #
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont


# CLASSES #
class App:
    """
    Creates a window app
    """

    def __init__(self):
        self.root = tk.Tk()

        self.create_window()

        self.root.mainloop()

    def create_window(self) -> None:
        """
        Creates a default window
        :return: None
        """

        # Geometry
        self.root.geometry('700x700')
        self.root.title('This is my super duper TK window')
        self.root.aspect(16, 9, 16, 9)

        # Font
        font = tkfont.Font(size=20)

        # Frame
        frame_header = tk.Frame(self.root)
        frame_header.grid(row=0, column=0, sticky='ew')
        frame_header.columnconfigure(0, weight=1)

        label_headings = tk.Label(frame_header, text='This is a big heading', relief='sunken', font=font)
        label_headings.grid(row=0, column=0, columnspan=2, sticky='ew')

        frame_values = tk.Frame(self.root)
        frame_values.grid(row=1, column=0)

        # Grid
        label_1 = tk.Label(frame_values, text='Value 1', font=font)
        label_1.grid(row=0, column=0)
        input_1 = ttk.Combobox(frame_values, font=font)
        input_1.grid(row=1, column=0)

        label_2 = tk.Label(frame_values, text='Value 2', font=font)
        label_2.grid(row=0, column=1)
        input_2 = ttk.Combobox(frame_values, font=font)
        input_2.grid(row=1, column=1)

        self.root.update()
        width = frame_header.winfo_width()
        height = frame_header.winfo_height() + frame_values.winfo_height()
        self.root.geometry(f'{width}x{height}')
        self.root.update()


# RUNTIME #
if __name__ == "__main__":
    app = App()
