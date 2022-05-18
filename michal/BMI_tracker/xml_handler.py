import xml.etree.ElementTree as ET

def testujPraciSxml(file):
    
    tree = ET.parse(file) # tohle to najde
    root = tree.getroot() # tohle to najde
    
    # weight = root.findall('weight')
    # height = root.findall('height')

    for userID in root:
        # projde pouze prvni uroven child
        # takze vrati pouze user id
        #print(userID.tag, userID.attrib)
        pass
    for entryID in userID:
        #print(entryID.tag, entryID.attrib)
        pass

    userID = 0
    entryID = 0
    weight = 0
    height = 0
    chest = 0
    belly = 0
    bottom = 0

    # takhle prochazim strom bez cyklu
    print(root[userID][entryID][weight].tag)
testujPraciSxml(r'C:\UserData\git_ws\myOnlyRealPrivateRepo\michal\BMI_tracker\testXML.xml')