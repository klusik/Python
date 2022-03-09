"""
    Generate a square with given lenght of size

    Author: klusik@klusik.cz
"""
# CLASSES #
class Rectangle:
    def __init__(self, size, symbol = "#"):
        self.size = size
        self.symbol = symbol

    def draw_rectangle(self):
        """ Draws a ascii rectangle """

        # Problem in 3 parts: top, middle and bottom

        # TOP
        for _ in range(self.size):
            print(self.symbol, end="")
        print("")

        # MIDDLE
        count_of_spaces = self.size - 2
        for row in range(count_of_spaces):
            # This draws rows

            # First symbol
            print(self.symbol, end="")

            # Middle spaces
            for _ in range(count_of_spaces):
                print(" ", end="")

            # Last symbol
            print(self.symbol)

        # BOTTOM
        for _ in range(self.size):
            print(self.symbol, end="")
        print("")

# RUNTIME #
if __name__ == "__main__":
    try:
        # User input -- size of rectangle
        size = abs(int(input("Give the size: ")))
    except ValueError:
        print("F. you :-D ")
    except Exception as exception:
        print("Something different happened.")
        print(exception.with_traceback())


    # Create the rectangle
    rectangle = Rectangle(size)

    rectangle.draw_rectangle()



