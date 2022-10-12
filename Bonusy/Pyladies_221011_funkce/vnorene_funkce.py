"""
    Funkce se dají i vnořovat, tedy v rámci jedné funkce může být definována i další funkce.

    Osobně to nedoporučuju dělat, pokud velmi dobře nevíte, proč toho využít.

    Níže trošku vycucaný příklad
"""

def vypocti(cislo1=0, cislo2=1, operator='+'):
    """ Funkce přijme 3 parametry """
    def secti(cislo1, cislo2):
        """ Vnitřní funkce sečti sečte parametry a vrátí součet """
        return cislo1 + cislo2

    def odecti(cislo1, cislo2):
        """ Vnitřní funkce odečte od sebe parametry a vrátí rozdíl """
        return cislo1 - cislo2

    def vydel(cislo1, cislo2):
        """ Vnitrni funkce vydělí parametry a vrátí podíl """
        return cislo1 / cislo2

    def vynasob(cislo1, cislo2):
        """ Vnitřní funkce vrátí součin dvou čísel z parametru """
        return cislo1 * cislo2

    # Zde logika k operátoru
    if operator == '+':
        # Funkce vypocti() vrátí součet
        return secti(cislo1, cislo2)
    elif operator == '-':
        # Funkce vypocti() vrátí rozdíl
        return odecti(cislo1, cislo2)
    elif operator == '*':
        # Funkce vypocti() vrátí součin
        return vynasob(cislo1, cislo2)
    elif operator == '/':
        # Pokud není jmenovatel nulový, funkce vypocti()
        # vrátí podíl
        if cislo2 == 0:
            return False
        return vydel(cislo1, cislo2)


# A zde se zeptáme uživatele
cislo1 = int(input("Zadej první číslo: "))
operator = input("Zadej operator: ")
cislo2 = int(input("Zadej druhé číslo: "))

# Samotný výpočet
vysledek = vypocti(cislo1, cislo2, operator)

# Výpis výsledku
print(cislo1, operator, cislo2, '=', vysledek)