""" Podivný podíl
    
    Chci funkci, která vrátí podíl dvou zadaných čísel (přijme je jako argumenty)
    a vrátí mi jejich podíl, pokud to jde (nechci dělit nulou), ale pokud je podíl
    tutěch dvou čísel větší 10, už to stejně vrátí 10.
    
    Např. pro čísla 100 a 5 to vrátí 10. Pro čísla 5 a 2 to vrátí 2.5.
    
    
    Rychlé zadání na závěr: Funkce, která přijme dva argumenty, první vypíše, druhý vrátí.
    
    """

def podivny_podil(citatel, jmenovatel):
    if jmenovatel == 0:
        return False

    podil = citatel / jmenovatel

    if podil > 10:
        return 10
    else:
        return podil


citatel = int(input("Zadej čitatele: "))
jmenovatel = int(input("Zadej jmenovatele: "))

print("Výsledek podivného podílu je", podivny_podil(citatel, jmenovatel))
