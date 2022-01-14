# XML handling
#
# Just testing of create some random XML, reading XML and stuff...
#

# IMPORTS #
import os
import glob
import xml.etree.ElementTree as ElementTree

# FUNCTIONS #
def readAllFiles():
    path = "../**"
    structure = glob.glob(path, recursive=True)
    return structure

# RUNTIME
def main():
    """Main function"""
    root = ElementTree.Element("root")
    something = ElementTree.SubElement(root, "something")

    ElementTree.SubElement(something, "innerSomething", name="description").text = "Tohe je vnitrni hodnota."

    ElementTree.indent(root)
    xmlTree = ElementTree.ElementTree(root)
    xmlTree.write("file.xml")

    fileStructure = readAllFiles()
    print(f"Found {len(fileStructure)} files.")
    for file in fileStructure:
        print(file)

if __name__ == "__main__":
    main()
