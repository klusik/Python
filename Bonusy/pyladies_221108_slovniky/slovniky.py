"""
    Slovníky (Dictionaries)

    Lekce 8. 11. 2022

    Pyladies
"""

seznam = ['a', 343, 3.14]

for polozka in seznam:
    print(polozka)

seznam_jako_slovnik = {
    0 : 'a',
    1 : 343,
    2 : 3.14,
}

for klic_polozky, polozka in seznam_jako_slovnik.items():
    print(f"Klic {klic_polozky} obsahuje hodnotu {polozka}")

# Python 3.6, možná 3.7

# Rozložení
ntice = ('ahoj', 'dveře')

promenna1 = 6
promennaa2 = "6"

# Velké Python Fuj
"""
for promenna in len(list_promennych):
    print(list_promennych[promenna])
"""
# Nefuj verze
"""
for promenna in list_hodnot:
    print(promenna)
"""

prmenna1, promenna2 = ntice

# hodnoty, klice, uzivatele, hernipole = hraj()
# vysleky = hraj()
# hodnoty = vysledky[0]
# klice = vysledky[1]
# ...


print(prmenna1, promenna2)

uzivatel = list()
print("Prazdny seznam", uzivatel)

uzivatel = [
    "klusik",
    "heslo",
    "pyladies@klusik.cz"
]
uzivatel2 = ["petra", "heslo2", "Pod Záhorskem 33/22, Praha",]

uzivatel_slovnik_ktery_neni_prazdny = {
    "jmeno" : "klusik",
    "heslo" : "heslo",
    "email" : "email klusika",
}

uzivatel_slovnik_ktery_neni_prazdny["adesa"] = "Taky má adresu"
uzivatel_slovnik_ktery_neni_prazdny["jmeno"] = "Rudolf"

uzivatel2_slovnik = {
    "jmeno" : "petra",
    "heslo" : "heslo petry",
    "adresa" : "Policejní 6, Usti n. L."
}

# Vrací list klíčů
print(uzivatel2_slovnik.keys())

# Vrací list hodnot
print(uzivatel2_slovnik.values())

print(uzivatel2_slovnik.items())
# Vypíšu položku ze slovníku
print(uzivatel2_slovnik["adresa"])

try:
    print(uzivatel_slovnik_ktery_neni_prazdny["adresa"])
except KeyError:
    print("Uživatel nemá adresu.")

uzivatel.append("Něco dalšího")

# Přidávání hodnot do slovníku
uzivatel_slovnik_ktery_neni_prazdny = dict()

uzivatel_slovnik_ktery_neni_prazdny["jmeno"] = "klusik"
uzivatel_slovnik_ktery_neni_prazdny["heslo"] = "heslo"
uzivatel_slovnik_ktery_neni_prazdny["email"] = "pyladies@klusik.cz"

print(f"Uživatel {uzivatel_slovnik_ktery_neni_prazdny['jmeno']} ma email {uzivatel_slovnik_ktery_neni_prazdny['email']}.")

print(uzivatel)

# Odstraňování položek ze slovníku
