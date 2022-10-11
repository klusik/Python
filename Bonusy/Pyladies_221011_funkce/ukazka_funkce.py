"""
    Ukázkový soubor na funkce
"""


def soucet(scitanec_1, scitanec_2):
    return (scitanec_1 + scitanec_2)


def podil(citatel, jmenovatel):
    if jmenovatel:
        return citatel / jmenovatel
    else:
        return None


x_1 = int(input("Zadej prvni cislo: "))
x_2 = int(input("Zadej druhe cislo: "))

print(f"Soucet cisel {x_1} a {x_2} je {soucet(x_1, x_2)}. Jejich podil je pak {podil(x_1, x_2)}.")
