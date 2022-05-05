"""
    Body values

    For losing weight purposes
"""

# IMPORTS #
import easygui
import logging

from bodies import Bodies
from helper import Helper

import xml.etree.ElementTree as xmlElTree


# CLASSES #




class Body:
    """ Body of the person """

    def __init__(self,
                 year_of_birth=None,  # For determining the age of a person
                 height=None,  # For determining BMI
                 sex=None,  # For determining BMI and ideal weight
                 age=None,  # Age
                 ignore=False,  # If the user is ignored by program (for creating a dummy bodies)
                 ):
        self.year_of_birth = year_of_birth
        self.height = height
        self.sex = sex

        # List for Body values
        self.body_values = []

    def add_body_value(self,
                       weight=None,
                       waist_circumference=None,
                       date_of_measurement=None,
                       ):
        # Create an object with all values necessary
        body_value = BodyValues(
            weight,
            waist_circumference,
            date_of_measurement,
        )

        # Add a body value to the list
        self.body_values.append(body_value)

        # Exit function
        return body_value


class BodyValues:
    """ Values the Body has """

    def __init__(self,
                 weight=None,  # Weight in kg
                 waist_circumference=None,  # Waist circumference in cm
                 date_of_measurement=None,  # Date of measurement (timestamp)
                 ):
        self.weight = weight
        self.waist_circumference = waist_circumference
        self.date_of_measurement = date_of_measurement


# RUNTIME #
def main():
    # Logging setup
    logging.basicConfig(level=logging.INFO)
    # Create a body
    bodies = Bodies()

    print(bodies.get_list_of_bodies())




if __name__ == "__main__":
    main()
