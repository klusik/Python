"""
    Ukázka na objekty

    Cílem je mít sadu bodů, které mají souřadnice v 3D prostoru
    [x_0, x_1, x_2] (nebo prostě x, y, z)

    Jednotlivé body budou vygenerovány náhodně.

    Panáček bude procházet těmito body v pořadí, ve kterém byly vygenerované.

    Výstupem bude celková trasa, kterou musel urazit mezi prvním a n-tým bodem.

    Všechny proměnné budou v angličtině
"""

# IMPORTS #
import random
import math


# CLASSES #
class Point:
    """ A point object """

    def __init__(self, x_0, x_1, x_2):
        """ Method is called as the object is created automatically """

        self.coordinates = tuple()

        # Sets the coordinates automatically
        self.set_coordinates(x_0, x_1, x_2)

    def set_coordinates(self, x_0, x_1, x_2):
        """ Sets coordinates for given point """
        self.coordinates = (x_0, x_1, x_2)

    def get_coordinates(self):
        """ Retunrs three values """
        return self.coordinates[0], self.coordinates[1], self.coordinates[2]


class Route:
    """ This saves all points to route """
    def __init__(self):
        """ This method is called as the object is created automatically """

        # Create an empty list for route
        self.route = []

        # Adding points. Ask user how many points to generate
        number_of_points = 0
        while number_of_points < 2:
            number_of_points = int(input("Enter the number of points to generate (at least 2): "))

        # Let's generate points
        for _ in range(number_of_points):
            pass

    def get_distance(self, point_1, point_2):
        """ Returns distance to point """
        return math.sqrt(
            point_1.get_coordinates()[0]**2 \
            + point_1.get_coordinates()[1]**2 \
            + point_1.get_coordinates()[2]**2
        )

    def point_exists(self, x_0, x_1, x_2):
        """ Returns True if point with those coords already exists """
        if self.route: # if not empty
            for point in self.route:
                # Go through all the points
                pass
        else:
            return False


# Run main program #
if __name__ == "__main__":
    route = Route()
