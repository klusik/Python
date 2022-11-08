"""
    Pokračování o slovnících

"""

seznam = [1, 2, 3, 4, 5]

# Ostraňování ze seznamu nejdříve
posledni = seznam.pop() # Smaže poslední položku ze seznamu a vrátí ji.
nejaky = seznam.pop(1) # Smaže položku na pozici 1 (tedy druha) a vráti ji. (Jako funkční hodnotu)

# print(seznam, posledni, nejaky)

# Odstraňování věcí ze slovníku
uzivatel = {
    "jmeno" : "Petr",
    "prace" : "Pyladies",
    "adresa" : "Praha",
    "cesta" : "na kole",
    "oblibene_cislo": 5,
}

print(uzivatel)

# Samotné odstraňování přes klíč přímo

uzivatel.pop("jmeno") # Odstraní tu s klíčem, který je uveden

uzivatel.popitem() # Odstraní poslední vložený klíč i s hodnotou

uzivatel["prace"] = None    # Klíč 'prace' bude obsahovat hodnotu None, samotný klíč
                            # ale bude dál existovat.
# Vymazání celého slovníku
# uzivatel.clear()

print(uzivatel)
print(uzivatel.items())

# Specifické hodtnoy:

# "ifovatené" na nulu
hodnota = "" # Prázdný řetězec -- tedy je to string (str), ale má délku 0 a nic neobsahuje.
hodnota = 0 # Integer (celé číslo) obsahující 0
hodnota = None # Rezervovaná hodnota, která znamená "prázdné", "není" atd. (prázdná množina)
hodnota = False # Logická hodnota typu bool(), která odpovídá bool(0)

if hodnota:
    """ Sem to nevleze """
else:
    """ Sem jo. """

hodnota = " " # Řetězec obsahující mezeru, délka tedy 1 a je to string jako každý jiný.

print(bool(hodnota))

hodnota = [] # Prázdný seznam
hodnota = {} # Prázdný slovník

