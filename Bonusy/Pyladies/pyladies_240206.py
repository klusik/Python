"""
    Funkce 6. 2. 2024
    
"""

# Krátký program, který se zeptá uživatele  na nějaký vstup
# a program vypíše, kolik znaků ten vstup obshuje, např. pro "ahoj" bude výstup 4.

"""
vstup = input("Zadej vstup: ")
delka_vstupu = len(vstup)

print(f"Délka vstupu je {delka_vstupu} znaků.")
"""

"""
# Definice funkce
def scitaci_funkce(parametr_1, parametr_2):
    soucet = parametr_1 + parametr_2
    return soucet

def odcitani(parametr_1, parametr_2):
    # Funkce odečte parametr_1 - parametr_2 a VYPÍŠE HO, nic nevrací
    rozdil = parametr_1 - parametr_2
    print(f"Rozdil je {rozdil}.")

cislo_1 = int(input("Zadej 1. číslo: "))
cislo_2 = int(input("Zadej 2. číslo: "))

soucet = scitaci_funkce(cislo_1, cislo_2)
print(f"Součet čísel {cislo_1} + {cislo_2} = {soucet}.")

odcitani(cislo_1, cislo_2)
"""

# Zadání: Chci napsat funkci, která vydělí dvě čísla, ale pokud druhé číslo
# bude 0 (nula), funkce vypíše "tohle nemůžu udělat."
# Funkce tento výsledek vypíše i vrátí, ale pokud bude chybový stav, vrátí to slovo "nelze"

"""
def deleni(prvni, druhy):
    if druhy == 0:
        print("Tohle nejde.")
        return("nelze")
    else:
        podil = prvni / druhy
        print(podil)
        return(podil)
    
cislo_1 = int(input("Zadej 1. číslo: "))
cislo_2 = int(input("Zadej 2. číslo: "))

podil = deleni(cislo_1, cislo_2)
print(f"Funkce vrátila {podil}.")
"""
"""
hodnota = 2
log_funkce = hodnota == 1

print(log_funkce)
print(2 == 2)
"""
"""
hodnota = print("Ahoj.")
print(hodnota)
"""
# Zadání: Vytvoř funkci, do které vstoupí 3 proměnné
# a funkce vrátí objem kvádru, který je definovaný těmito třemi hodnotami.
# objem je vždy kladné číslo, dejte pozor, aby se vždy vrátilo kladné číslo.
# Zadání 2: Vytvoř funkci, která vezme tři čísla, z předchozího zadání
# a vypíše jejich aritmetický průměr.

"""
from math import pi # 3.1416...

def objem_kvadru(a, b, c):
    objem = a * b * c
    
    # když do funkce abs() vstoupí kladné číslo, vystoupí kladné, pokud záporné,
    # vystoupí kladné. Funkce abs() vždy vrací nezáporný výsledek (x >= 0)
    return abs(objem)
"""
def aritmeticky_prumer(a, b, c):
    return (a + b + c) / 3

cislo_1 = int(input("Zadej 1. číslo: "))
cislo_2 = int(input("Zadej 2. číslo: "))
cislo_3 = int(input("Zadej 3. číslo: "))


# Ještě jedno zadání:
# Uživatel zadá poloměr koule a funkce vrátí objem koule (vždy kladný, použijte abs funkci)
# Pro připomenutí: V = 4/3 * pi * (r ** 3)
# Jako vstup do funkce na objem můžete použít výstupu z funkce
# pro aritmetický průměr výše.
# pi se načte z math knihovny jako:

from math import pi

def koule(polomer, pi):
    return abs(4/3 * pi * (polomer ** 3))

objem_koule = koule(aritmeticky_prumer(cislo_1, cislo_2, cislo_3), pi)
print(f"Využijeme čísel z průměru, objem takové koule je {objem_koule}.")

