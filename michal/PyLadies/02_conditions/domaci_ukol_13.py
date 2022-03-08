'''
Na srazu jsme měli program, který píše různé nesmysly podle uživatelem zadaného věku.

Zkus napsat program, který píše hlášky podle
zadané rychlosti chůze, 
váhy ulovené ryby, 
počtu tykadel, 
teploty vody 
nebo třeba vzdálenosti od rovníku. 
'''

rychlost_chuze = float(input("zadejte rychlost chuze: "))
vaha_ryby = float(input("zadejte vahu_ryby: "))
pocet_tykadel = float(input("zadejte pocet paru tykadel (0, 1, 2): "))
teplota_vody = float(input("zadejte teplotu vody: "))
vzdalenost_rovnik = float(input("zadejte vasi vzdalenost od rovniku: "))

if rychlost_chuze > 6:
    print("rychlost chuze je vyssi nez 6km/h, pravdepodobne bezite")
else:
    print("vase chuze je pomalejsi nez 6km/h, pridejte, nebo vas dohoni Rusove")

if vaha_ryby > 60:
    print(f"vaha ryby prekracuje 60kg. Gratuluji ke kapitalnimu ulovku")
elif vaha_ryby > 100:
    print(f'opravdu ta ryba vazi {vaha_ryby}??? To je z Pripyati?')
else:
    print("gratuluji, premohl jste nemou tvar. Dnes bude hodokvas")

if pocet_tykadel not in range(3):
    print("prave jste prozil blizke setkani tretiho druhu s mimozemskou formou zivota")

if teplota_vody < -273.15:
    print('setkal jste se s teplotou nizsi, nez je absolutni nula. kontaktuje akademii ved CR, dekuji')
elif teplota_vody == -273.15:
    print('pri teto teplote je mozny pouze elementarni pohyb castic.')
elif teplota_vody > -273.15 and teplota_vody < 0:
    print('pevne skupenstvi vody')
elif teplota_vody >= 0 and teplota_vody <= 100:
    print('kapalne skupenstvi vody')
elif teplota_vody > 100 and teplota_vody < 2000:
    print('plynne skupenstvi vody')
elif teplota_vody >= 2000:
    print('z vody se stalo plazma')

if vzdalenost_rovnik != 0:
    print("nachazite se prilis blizko invazi na Ukrajinu")