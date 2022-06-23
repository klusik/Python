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
                 dimensions,    # Number of dimensions (2 or more)
                 distance,      # A distance to travel to
                ):
        self.dimension = dimensions
        self.distance = distance

    def run(self):
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
