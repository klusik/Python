"""
    Do a random walk generator.

    Inputs:
        -   A distance from origin to travel to
        -   Number of dimensions (2 or more) to consider (automatically from input)

    Output:
        -   List of coordinates
        -   File with list of coordinates
"""


# CLASSES #
class Coords:
    def __init__(self,
                 dimensions,  # Number of dimensions (2 or more)
                 distance,  # A distance to travel to
                 ):
        self.dimension = dimensions
        self.distance = distance

    def run(self):
        """ Run the script """

        # 1st step is to determine in which way to go.
        # Because of the dimmension universality, it's possible to go in any way given dimmension allows.
        # For 2D it's only up (0, 1), right (1, 0), left(-1, 0) and down (0, -1).
        # For 3D these values could be (0, 0, 1) or (0, 0, -1) and similar, only one 'one' or 'minus one' placed.
        # This will be used as a differential vector from the origin, which is (0, 0, ..., 0)
        #
        # Random generator must generate two values:
        #   -   1 or -1 for the way
        #   -   index number in the vector which should be changed (for 3D it would be 0--2, for 2D it would be 0--1 etc)
        pass


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
