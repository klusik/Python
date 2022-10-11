"""
    Ukázkový soubor na funkce
"""


def soucet(scitanec_1, scitanec_2=-47):
    soucet_cisel = scitanec_1 + scitanec_2
    return soucet_cisel


def podil(citatel, jmenovatel):
    if jmenovatel != 0:
        return citatel / jmenovatel
    else:
        return None


x_1 = int(input("Zadej prvni cislo: "))
x_2 = int(input("Zadej druhe cislo: "))

soucet_cisel = soucet(x_1)
#soucet_cisel = soucet(scitanec_1=x_1, scitanec_2=x_2)

# Obvod kruhu: o = 2 * pi * r

print (soucet_cisel)

# print(f"Soucet cisel {x_1} a {x_2} je {soucet(x_1, x_2)}. Jejich podil je pak {podil(x_1, x_2)}.")
