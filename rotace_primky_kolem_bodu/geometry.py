"""
    Rotate an abscisse around a point
    abscisse je usecka, vole
        voe vim, ne :-D 

    Author:     Rudolf Klusal
    Year:       2022

"""

# IMPORTS #
import math


# CLASSES #
class Point:
    """ Point class """
    def __init__(self,
                 x, # X coordinate of a point
                 y, # Y coordinate of a point
                    ):
        """ Init """
        self.x = x
        self.y = y
        

class Abscisse:
    """ Abscisse class """
    def __init__(self,
                 point_1,  # a touple with x coordinates
                 point_2,  # a touple with y coordinates
                 ):
        """ Init method """
        self.point_1 = dict()
        self.point_2 = dict()

        # setting
        self.point_1['x'] = point_1[0]
        self.point_1['y'] = point_1[1]

        self.point_2['x'] = point_2[0]
        self.point_2['y'] = point_2[1]

    def set_new_coords(self,
                       point_1,
                       point_2,
                       ):
        """ Sets new coordinates """


    def get_length(self):
        """ Returns a length of an abscisse """
        return math.sqrt((self.point_1['x'] - self.point_2['x']) ** 2 + (self.point_1['y'] - self.point_2['y']) ** 2)

    def rotate(self,
               angle,  # an angle of rotation in degrees
               point_of_rotation,  # rotate around this point
               ):
        """ Rotate an abscisse around a point with given angle.
            Returns 2 points after rotation."""

        def rotate_point(point, point_of_rotation, angle):
            """ Rotates a point around an angle and point"""

            # Rotation is done as follows:
            # p'x = cos(theta) * (px-ox) - sin(theta) * (py-oy) + ox
            # p'y = sin(theta) * (px-ox) + cos(theta) * (py-oy) + oy

            new_x = math.cos(math.radians(angle)) \
                    * (point['x'] - point_of_rotation['x']) - math.sin(math.radians(angle)) \
                    * (point['y'] - point_of_rotation['y']) \
                    + point_of_rotation['x']
            new_y = math.sin(math.radians(angle)) \
                    * (point['x'] - point_of_rotation['x']) + math.cos(math.radians(angle)) \
                    * (point['y'] - point_of_rotation['y']) \
                    + point_of_rotation['y']

            return (new_x, new_y)

        point_1_rotated = rotate_point(self.point_1, point_of_rotation, angle)
        point_2_rotated = rotate_point(self.point_2, point_of_rotation, angle)

        return point_1_rotated, point_2_rotated

    def rotate_self(self,
                    angle, # Angle of rotation
                    point, # Point around
                    ):
        """ Rotates an abscisse around a point and saves new points as abscisse points """
        pass

    def rotate_around_center(self,
                             angle, # Angle of rotation
                             ):
        """ Rotates an abscisse around it's center point """

    def get_center_point(self):
        """ Returns a center point of an abscisse """

    def get_points(self):
        """ Get two points of abscisse """
        pass

    def is_point_on_abscisse(self,
                             point, # A point on which we can decide if it's on or it's not on self abscisse
                             ):
        pass


# RUNTIME #
def main():
    print("Points of an abscisse:")
    x1 = float(input("Enter the X coordinate of the 1st point: "))
    y1 = float(input("Enter the Y coordinate of the 1st point: "))
    x2 = float(input("Enter the X coordinate of the 2nd point: "))
    y2 = float(input("Enter the Y coordinate of the 2nd point: "))

    print("Rotation point:")
    x_rot = float(input("Enter the X coordinate of the point of rotation: "))
    y_rot = float(input("Enter the Y coordinate of the point of rotation: "))
    angle_rot = float(input("Enter the angle in degrees: "))

    abscisse = Abscisse((x1, y1), (x2, y2))

    print(f"Length of an abscisse is: {abscisse.get_length()}")

    print(abscisse.rotate(angle_rot, {'x' : x_rot, 'y' : y_rot}))


if __name__ == "__main__":
    main()
