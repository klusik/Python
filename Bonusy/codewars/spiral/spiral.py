"""
    CW:         https://www.codewars.com/kata/534e01fbbb17187c7e0000c6/train/python
    Author:     klusik@klusik.cz
"""

def spiralize(size):
    """The goal is to create a grid with a spiral,
    begining with location (0 0)."""

    # Making a grid of size {size}
    grid = []

    # Initialize grid
    for row in range(size):
        grid.append([0]*size)

    ## Going through the grid & filling it up :-)

    # Initial location
    location = [0, 0]   # 0, 0 is the top left corner
    direction = [1, 0]  # x diff, y diff

    while True:
        # Test if it's possible to go in direction way
        #
        # If the location on the direction's way is out of the grid, change direction
        # If the location + 2 on the direction's way is used (1), change direction.
        #
        # Stop cycle if there's nowhere to go 'legally'

    return grid

if __name__ == "__main__":
    size = 10
    for row in spiralize(size):
        print(row)
