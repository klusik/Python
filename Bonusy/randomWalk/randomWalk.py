"""
    Do a random walk generator.

    Inputs:
        -   A distance from origin to travel to
        -   Number of dimensions (2 or more) to consider (automatically from input)

    Output:
        -   List of coordinates
        -   File with list of coordinates
"""
# IMPORTS #
import random
import math

# CLASSES #
class Coords:
    def __init__(self,
                 dimensions,  # Number of dimensions (2 or more)
                 distance,  # A distance to travel to
                 ):
        self.dimension = dimensions
        self.distance = distance

        # The while gameboard is a list of tuples
        self.gameboard = list()

        # Create an origin (0, 0, ..., 0)
        origin = tuple([0] * self.dimension)

        # Add 1st coordinate to the list
        self.gameboard.append(origin)

    def run(self):
        """ Run the script """

        # The main is to determine in which way to go.
        #
        # Because of the dimmension universality, it's possible to go in any way given dimmension allows.
        # For 2D it's only up (0, 1), right (1, 0), left(-1, 0) and down (0, -1).
        # For 3D these values could be (0, 0, 1) or (0, 0, -1) and similar, only one 'one' or 'minus one' placed.
        # This will be used as a differential vector from the origin, which is (0, 0, ..., 0)
        #
        # Random generator must generate two values:
        #   -   1 or -1 for the way
        #   -   index number in the vector which should be changed
        #       (for 3D it would be 0--2, for 2D it would be 0--1 etc)

        while self.in_range():
            # Generate 1 or -1
            way_to_go = random.sample([-1, 1], 1)

            # Populate an empty vector with a way to go randomly
            diff_vector = [0] * self.dimension
            random_dimension = random.randrange(0, self.dimension, 1)
            diff_vector[random_dimension] = way_to_go[0]

            # Compute a new coordinate
            last_coord = self.gameboard[-1]
            new_coord = tuple(map(lambda x, y: x + y, last_coord, tuple(diff_vector)))

            # Append to the list of coordinates the new coordinate
            self.gameboard.append(new_coord)

    def compute_distance(self,
                         ref_location = None):
        square_sum = 0
        if ref_location:
            location = ref_location
        else:
            location = self.gameboard[-1]

        for value in location:
            # Go through all numbers in the last coord
            square_sum += value ** 2

        return math.sqrt(square_sum)

    def in_range(self):
        """ Returns True if in distance range """
        return self.compute_distance() < self.distance

    def display_result(self):
        for index, coord in enumerate(self.gameboard):
            print(f"{index+1}:\t {coord} \t {self.compute_distance(coord)}")



# RUNTIME #
if __name__ == "__main__":

    # Input value
    input_distance = 0

    # Dimension
    input_dimension = 0

    # Input coordinates
    while input_distance <= 1:
        input_distance = float(input("Enter a distance to travel to: "))

    # Input dimension
    while input_dimension < 2:
        input_dimension = int(input("Enter a dimmension (whole positive number >= 2): "))

    # Game plane
    coords = Coords(
        dimensions=input_dimension,
        distance=input_distance,
    )

    # Run
    coords.run()

    # Display output
    coords.display_result()
