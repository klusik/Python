# urci stoleti ze zadaneho letopoctu
# rok 1705 vrati 18 stoleti
# rok 1900 vrati 19 stoleti
# rok 1601 vrati 17 stoleti

# todo naprogramovat to
# jak by to mělo fungovat
# vzhledem k tomu, ze pracuju s letopoctem a z neho chci ziskat stoleti, tak mi staci vydelit zadany letopocet 100
# pokud to vyjde presne (napriklad rok 800 / 100 = 8 a je to zaroven 8 stoleti), tak zapisuji rovnou vysledek
# pokud zbytek bude > 0, tak prictu jedna (napriklad rok 801/100 > 8 a je to 9 stoleti)

def century(year):
    # Finish this :)

    if year % 100 == 0:
        a = int(year / 100)
        return a
    else:
        b = int(year / 100) + 1
        return b


century(1350)
