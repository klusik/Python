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

    return grid

if __name__ == "__main__":
    size = 10
    for row in spiralize(size):
        print(row)
