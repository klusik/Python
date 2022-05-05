"""
    Body values

    For losing weight purposes
"""

# IMPORTS #
import easygui
import logging

import xml.etree.ElementTree as xmlElTree


# CLASSES #
class Helper:
    """ Stuff that helps """

    @staticmethod
    def dict_dump(variable,  # variable which is readed
                  indent=0,  # indent of the print
                  indent_symbol=' ',  # symbol of the indent, default ' '
                  ):
        """ Dumps variable in readable way """

        # Assuming the 'variable' is dict and its all items
        # are values or dicts.

        for index, item in enumerate(variable.items()):
            print(f"{str(indent_symbol) * indent}{item[0]}")
            if isinstance(item[1], dict):
                Helper.dict_dump(item[1], indent + 1, ' ')
            else:
                print(f"{str(indent_symbol) * (indent + 1)}{item[1]}")


class Config:
    list_of_bodies_file = "bodies.xml"


class Bodies:
    def __init__(self):
        self.list_of_bodies = self.load_list_of_bodies()

    def get_list_of_bodies(self):
        """ Returns a list of bodies """
        return self.list_of_bodies

    def load_list_of_bodies(self):
        """ Loads a list of previous saved bodies
            Returns: Dict with bodies and their's values
        """

        try:
            with open(Config.list_of_bodies_file, "r") as f_list_of_bodies:
                # The file could be read, cool
                pass

        except FileNotFoundError:
            # No previously found body, create the file
            try:
                root = xmlElTree.Element("bodies")
                body = xmlElTree.SubElement(root, "body", name="John Doe")
                xmlElTree.SubElement(body, "year_of_birth").text = "1984"
                xmlElTree.SubElement(body, "height").text = "180"
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

        # Dict of bodies
        bodies = dict()

        for body in root:
            # For every body in the XMl there will be values
            bodies[body.attrib['name']] = dict()

            for value in body:
                # Every body has values,
                # Key is value.tag, value is value.text from XML
                bodies[body.attrib['name']][value.tag] = value.text

            """
            obj_body = Body(
                year_of_birth=body.attrib['year_of_birth'],
                height=body.attrib['height'],
                ignore=body.attrib['ignore'],
                sex=body.attrib['sex'],
            ) """

        logging.debug(bodies)
        return bodies


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

    Helper.dict_dump(bodies.get_list_of_bodies())


if __name__ == "__main__":
    main()
