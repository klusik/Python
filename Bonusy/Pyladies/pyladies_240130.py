# Pyladies 30. 1. 2024 (Cykly)

seznam_jmen = ["Marie", "Hana", "Dominika"]
neco = "Filip"

# Cyklus FOR
# Omezený počet opakování, který známe dopředu.
# Průchody seznamů, slovníků, souborů, ...

"""
    Šablona FOR
    
    for promenna in seznam:
        neco dělej

"""
for jmeno in seznam_jmen:
    # print(jmeno)
    pass
    
# Celý seznam
# print(seznam_jmen)

# Konkrétní položka
# print(seznam_jmen[1])

# Zadání
# Vezmi nějaký seznam slov, jmen, cokoliv tě napadne
# a vytiskni postupně všechna tato slova s tím, že mezi nimi budou MEZERY.
# Pro vstup ["hana", "jana", "petra"] to vypíše "hana jana petra".

"""
nova_jmena = ["Hana", "Jana", "Dominika", "Lucie", "Daida", "Lea"]
for jmeno in nova_jmena:
    print(jmeno, end=" ")
"""

"""
for cislo in range(10):
    print(cislo, end="  ")
"""    
# print(range(35))
    
"""    
for cislo in range(10, 30):
    print(cislo, end=" ")
print()
   
"""
"""
    Zadání:
    
    Zeptáme se uživatele na nějaké číslo, uživatel odpoví třeba 5.
    
    Program pak 5krát vypíše slovo "ahoj" a oddělí ho mezerami
    na jeden řádek.
    """
"""    
pocet_opakovani = int(input("Zadej počet opakování: "))
for poradi in range(1, pocet_opakovani+1):
    print(f"{poradi}. Ahoj")
else:
    print()
"""

# Uprav program tak, aby vypisoval pořadí výpisu, takže:
# 1. Ahoj
# 2. Ahoj
# 3. Ahoj
# Už to nebude na jednom řádku, dáte pryč end=""

"""
seznamek = ["Audi", "BMW", "Skoda", "Honda"]
for znacka_auta in seznamek:
    print(f"Auto: {znacka_auta} je znacka auta, ktera znamena {znacka_auta}.")
"""    
    
""" Cyklus WHILE:

    while (vyraz):
        dělej to, dokud vyraz platí.
        
        """

"""
pocitadlo = 0
while pocitadlo <= 100: # kontroluju, jestli je počítadlo menší než 100
    print("Ahoj, já jsem nekonečný, nemyslím Daniel. ")    # Vypíšu
    pocitadlo = pocitadlo + 1 # nezapoemenu počítat, jinak by to bylo nekonečné
"""

"""
for pocitadlo in range(100):
    print("...")
    """

"""
    Napište pomocí cyklu while prográmek, kterýu
    se zeptá uživatele na číslo mezi 1 a 10
    a pokud uživatel zadá něco většího než 10 nebo menšího než 1,
    program řekne "musíš zadat něco 1--10" a znovu se ho zeptá.
    
    Bude se uživatele ptát tak dlouho, dokud uživatel netrefí něco
    mezi 1 a 10.
    """
"""
pocitadlo_pokusu = 1
while True:
    vstup_uzivatele = int(input("Zadej cislo v rozmezí 1 -- 10: "))
    
    if 1 <= vstup_uzivatele <= 10:
        print(f"Super, povedlo se ti na {pocitadlo_pokusu}. pokus!")
        break
    else:
        pocitadlo_pokusu += 1
        # toto odpovídá pocitadlo_pokusu = pocitadlo_pokusu + 1
"""
# Náhodné číslo

# print(randrange(100)) # Náhodné číslo

# myslene_cislo = randrange(1, 10) # Generuje čísla mezi 1 až 10 (včetně)

"""
    Zadání HÁDACÍ HRA:
    
    V cyklu se probgram bude uživatele ptát na náhodné číslo,
    které si před cyklem počítač vylosuje v rozsahu 1--10.
    
    Uživatel bude hádat toto číslo, pokud se trefí, cyklus končí,
    pokud se netrefí, program vypíše "seš moc nízko" nebo "seš moc vysoko"
    podle toho, jestli nadswtřelil či podstřelil.
    """
from random import randrange # Musíme vědět, co je randrange()
myslene_cislo = randrange(1, 10) # počítač si myslí čísla 1--10

pokus = 1
while True:
    hadani = int(input("Jaké číslo v rozmezí 1--10 si počítač myslí? "))
    
    if hadani == myslene_cislo:
        # Jupí, trefa
        print(f"Super, trefa na {pokus} pokus!")
        break
    elif hadani < myslene_cislo:
        print("Podstřeleno")
    else:
        print("Nadstřeleno")
        
    pokus += 1
