# IMPORTS #
import logging
import xml.etree.ElementTree as xmlElTree
from config import Config

# CLASSES #
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

if __name__ == "__main__":
    pass
