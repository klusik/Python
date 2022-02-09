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
def click(event):
    print(f"Clicked at {event.x}:{event.y}")

def main():
    """ Main function """

    # Creating some geometry
    square = geometry.Rectangle(
        geometry.Point(100, 100),
        geometry.Point(200, 200))

    # Creating a window

    # Initialize TkInter
    root_window = tkinter.Tk()

    # Canvas
    window_canvas = tkinter.Canvas(root_window, bg="white", width=800, height=600)

    # Stuff on canvas
    window_canvas.create_rectangle(
        square.point_0.x,
        square.point_0.y,
        square.point_1.x,
        square.point_1.y)

    # Mouse events
    window_canvas.bind("<Button-1>", click)

    # Render canvas
    window_canvas.pack()

    # Wait for user input
    root_window.mainloop()

if __name__ == "__main__":
    main()
