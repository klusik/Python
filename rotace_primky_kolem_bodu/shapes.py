"""
    SHAPES

    A graphical program to deal with a shapes.

    Using 'geometry' library.

    Author:     Rudolf Klusal
    Year:       2022
"""

# IMPORTS #
import tkinter
import geometry

# RUNTIME #
if __name__ == "__main__":
    """ Main function """

    # Creating a window

    # Initialize TkInter
    root_window = tkinter.Tk()

    # Canvas
    window_canvas = tkinter.Canvas(root_window, bg="white", width=800, height=600)

    # Stuff on canvas
    window_canvas.create_rectangle(100, 100, 300, 400)

    # Render canvas
    window_canvas.pack()

    # Wait for user input
    root_window.mainloop()