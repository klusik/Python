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
    location_x = 0
    location_y = 0    # 0, 0 is the top left corner, cursor variable
    direction = [1, 0]  # x diff, y diff

    while True:
        # Test if it's possible to go in direction way
        #
        # If the location on the direction's way is out of the grid, change direction
        # If the location + 2 on the direction's way is used (1), change direction.
        #
        # Stop cycle if there's nowhere to go 'legally'

        # Location and out of grid situation
        if location_x + direction[0] == size:
            # x out of bonds on the right, need to switch direction to down
            direction = [0, 1]
        if location_x == 0 and direction[0] == 1:
            # x out of bonds on the left, need to switch direction to up
            direction = [0, -1]
        if location_y + direction[1] == size:
            # y out of bonds on the bottom, need to switch to left
            direction = [-1, 0]

        # Used space direction switch
        if direction == [1, 0]:
            if grid[location_y][location_x + direction[0] + 1] == 1:
                # there's a previous spiral on the right, switch down
                direction = [0, 1]
        if direction == [-1, 0]:
            if grid[location_y][location_x + direction[0] - 1] == 1:
                # there's a previous spiral on the left, switch up
                direction = [0, -1]
        if direction == [0, 1]:
            if grid[location_y + direction[1] + 1][location_x] == 1:
                # there's a previous spiral on the bottom, switch to left
                direction = [-1, 0]
        if direction == [0, -1]:
            if grid[location_y + direction[1] -1][location_x] == 1:
                # there's a previous spiral on the top, switch to right
                direction = [1, 0]

        # Placing the 1 on the grid
        grid[location_y][location_x] = 1

        # Moving to next coords
        location_x += direction[0]
        location_y += direction[1]

        # Checking, if end of cycle
        if grid[location_y, location_x] == 1:
            # nowhere else to go, break
            break


    return grid

if __name__ == "__main__":
    size = 10
    for row in spiralize(size):
        print(row)
