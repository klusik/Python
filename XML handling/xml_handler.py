# XML handling
#
# Just testing of create some random XML, reading XML and stuff...
#

# IMPORTS #

import xml.etree.ElementTree as ElementTree

# RUNTIME
def main():
    """Main function"""
    root = ElementTree.Element("root")
    something = ElementTree.SubElement(root, "Something")

    ElementTree.SubElement(something, "Aha, takhle", name="description").text = "Tohe je vnitrni hodnota."

    xmlTree = ElementTree.ElementTree(root)
    xmlTree.write("file.xml")
    
if __name__ == "__main__":
    main()
