"""
    Ahoj,

    není vůbec od věci si opakovat i základní věci, není prostě možné,
    abychom se po 3 setkáních setkali a nebylo jasné, jak udělat

    šuplíček = input("Něco si přej: ")

    a podobně.

    Tyhle úkoly je BEZPODMÍNEČNĚ nutné umět, jinak nejdeme dál,
    byla by to ztráta času všech.
"""

"""
*   Úkol 1  *

    Vytvoř skriptík, který se zeptá uživatele na nějaké písmenko.
    
    Program toto písmenko uloží "do šuplíčku." 
    
    Program porovná, jestli se písmenko rovná 'a' a pokud ano,
    napíše "jupí, je to áčko," jinak "nu nic, tohle není áčko."
    
    Dagmar, vím, že to zvládneš, ale spíše pro M.
"""

# Úkol 1 -- nejsnazší řešení
pismenko = input("Zadej písmenko: ")
if pismenko == 'a':
    print("Jupí, je to áčko.")
else:
    print("Nu nic, není to áčko.")

# Úkol 1 -- vylepšení
# pismenko už buud počítat, že je zadané z předchozího řešení

if len(pismenko) > 1:
    print("Tohle není samostatné písmenko!")
else:
    if pismenko == 'a':
        print("Jupí, áčko.")
    else:
        print("Nu nic, není áčko.")


"""
*   Úkol 2  *
    
    Vytvoř prográmek, který se zeptá uživatele na číslo.
    
    Toto číslo se uloží do šuplíčku a převede na int() v jednom kroku.
    
    Program zjistí, jestli zadané číslo je větší než 3 a podle toho
    napíše buď "číslo je větší než 3," "číslo je rovné 3" 
    nebo "číslo je menší než 3." 
    
    Vylepšená verze bude kontrolovat, jestli zadaná věc je číslo, 
    ale to už je složitější, bude mi úplně stačit první varianta
    2. úkolu.
"""

# Úkol 2 -- základní verze
zadane_cislo = input("Zadej nějaké celé číslo: ")

"""
# tutu část si odkomentuj, jestli chceš základní řešení

cislo = int(zadane_cislo)
if cislo > 3:
    print(f"Číslo {cislo} je větší než 3.")
elif cislo == 3:
    print(f"Číslo {cislo} je rovné 3.")
else:
    print(f"Číslo {cislo} je menší než 3.")
"""

# Úkol 2 -- vylepšená verze s kontrolou
# Budu počítat s tím, že zadane_cislo máme už

try:
    cislo = int(zadane_cislo)
    if cislo > 3:
        print(f"Číslo {cislo} je větší než 3.")
    elif cislo == 3:
        print(f"Číslo {cislo} je rovné 3.")
    else:
        print(f"Číslo {cislo} je menší než 3.")

except ValueError:
    print("Není číslo.")


