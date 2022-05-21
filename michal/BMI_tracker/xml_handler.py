import xml.etree.ElementTree as ET
'''
Pred samotnou implementaci xml handleru musim udelat uvahu, jak chci s xml
soubory vlastne pracovat, co vsechno chci naprogramovat. XML soubor bude
slouzit jako uchovatel uzivatelskych dat.

uzivatelska data:
vaha, vyska, obvod hrudi, bricha a pasu, poznamka

metadata:
user id, entry id

Uzivatel muze
 1) vytvorit novy soubor s user daty
    - def createProfile(userName)
        vytvori strukturu souboru s default values
 2) nemam chut resit jakakoliv prava
 3) zobrazit user data
    def showData(userName)
        nacte soubor a zobrazi vsechny zaznamy pro vybraneho uzivatele
        v tabulce, ktera bude soucasti GUI.
 4) zadat user data
    def enterData()
        funkce se pta na userName, userData(vaha, vyska, obvod hrudi,
        bricha, poznamka)
 5) zmenit user data
    def alterData(entryID, userID)
        funkce se musi zeptat na atribut, ktery chce uzivatel menit,
        ten overit na pritomnost, zeptat se na novou hodnotu a zapsat ji
 6) smazat user data
    def eraseData(entryID, userID)
        funkce bude umoznovat smazani konkretnich zaznamu, nejnizsi uroven
        bude entryID
 7) exportovat user data ve forme pdf
    def exportPDF()
        funkce pripravi vystup do tvaru, ktery bude umet modul vytvarejici
        soubory PDF (zajit nevim ktery to bude)
'''


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