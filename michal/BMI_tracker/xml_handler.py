import xml.etree.ElementTree as ET

def testujPraciSxml(file):
    # vytvor objekt xml souboru
    tree = ET.parse(file) # tohle to najde
    # vytvor objekt s obsahem souboru (strukura)
    root = tree.getroot() # tohle to najde

    userID = 0
    entryID = 0
    weight = 0
    height = 0
    chest = 0
    belly = 0
    bottom = 0

    # takhle prochazim strom bez cyklu
    print(root[userID][entryID][weight].tag)
    print(root[userID][entryID][weight].text)

    # nacti hodnoty tagu
    for userID in root:
        # projde pouze prvni uroven child
        # takze vrati pouze user id
        print(userID.tag, userID.attrib)
        
    for entryID in userID:
        print(entryID.tag, entryID.attrib)
        
    # zapis dat do xml souboru
    print(root[0][0][0].text)
    root[0][0][0].text = str(90) # i kdyz je to cislo, musim zapsat string
    print(root[0][0][0].text)

    tree.write(r'C:\UserData\git_ws\myOnlyRealPrivateRepo\michal\BMI_tracker\testXML.xml')

testujPraciSxml(r'C:\UserData\git_ws\myOnlyRealPrivateRepo\michal\BMI_tracker\testXML.xml')