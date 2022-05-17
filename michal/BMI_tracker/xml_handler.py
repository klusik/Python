import xml.etree.ElementTree as ET

def parseXML(file):
    tree = ET.parse(file)
    root = tree.getroot()
    weight = root.findall(weight)
    height = root.findall(height)

    print(weight,height)

parseXML(r'C:\UserData\git_ws\myOnlyRealPrivateRepo\michal\BMI_tracker\testXML.xml')