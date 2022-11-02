ble = "ahoj, tohle je všechno malými"

for znak in range(len(ble)):
    print(f"{ble[0:znak]}{ble[znak].upper()}{ble[znak+1:]}")