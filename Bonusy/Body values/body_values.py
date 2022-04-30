"""
    Body values

    For losing weight purposes
"""

# IMPORTS #
import easygui
import logging

import xml.etree.ElementTree as xmlElTree


# CLASSES #
class Config:
    list_of_bodies_file = "bodies.xml"


class Body:
    """ Body of the person """

    def __init__(self,
                 year_of_birth=None,  # For determining the age of a person
                 height=None,  # For determining BMI
                 sex=None,  # For determining BMI and ideal weight
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

    def list_of_bodies(self):
        """ Loads a list of previous saved bodies """
        try:
            with open(Config.list_of_bodies_file, "r") as f_list_of_bodies:
                # The file could be read, cool
                pass

        except FileNotFoundError:
            # No previously found body, create the file
            try:
               root = xmlElTree.Element("bodies")
               body = xmlElTree.SubElement(root, "Default")
               xmlElTree.SubElement(body, "age").text = "30"
               xmlElTree.SubElement(body, "height").text = "180"
               xmlElTree.SubElement(body, "name").text = "John Doe"
               xmlElTree.SubElement(body, "ignore").text = "True"

               tree = xmlElTree.ElementTree(root)
               tree.write(Config.list_of_bodies_file)

               logging.info("Test")

            except PermissionError:
                # If bodies file couldn't be created
                logging.error(f"File {Config.list_of_bodies_file} couldn't be created, exiting process.")
                exit(1)

        # File exists and it's openable, xml parse it
        root = xmlElTree.parse(Config.list_of_bodies_file).getroot()

        # List of bodies
        print(root)


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
    body = Body()

    body.list_of_bodies()


if __name__ == "__main__":
    main()
