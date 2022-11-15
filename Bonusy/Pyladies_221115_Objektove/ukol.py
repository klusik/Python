"""
    Objektově

    Vytvořte třídu, která bude obsahovat seznam hodnot.

    Třída bude obsahovat metodu, třeba pridej(hodnota)

    Třída bude obsahovat metodu na smazání seznamu,
    třeba smaz_seznam().

    Vytvořte si objekt, na základě této třídy.

    V cyklu (while) vytvořte zadávání hodnot,
    které se bude ptát uživatele na číslo, které
    je třeba přidat do seznamu. Bude se zadávat, dokud se nezadá
    třeba nula (nebo tak něco).

    Pak bude třída obsahovat metodu na vypsání seznamu (nějak hezky,
    očíslovaně atd.)

    Po zadání všech čísel (od uživatele) se zavolá vypisovací metoda na výpis.
"""

class Hodnoty:
    """ Tuta třída bude obsahovat hodnoty a metody k tomu určené """
    seznam = []

    def pridej_hodnotu(self, hodnota):
        """ Přidá hodnotu do seznamu """
        self.seznam.append(hodnota)

    def smaz_seznam(self):
        """ Smaže celý seznam """
        self.seznam.clear()

    def vypis_hodnoty(self):
        """ Vypise hezky hodnoty pod sebe a očíslovaně """

        if self.seznam:
            for poradi, hodnota in enumerate(self.seznam):
                print(f"{poradi + 1}. {hodnota}")
        else:
            print("Tento seznam je prázdný.")
# Zde vytvoříme seznam hodnot na základě třídy Hodnoty() (vytváříme objekt)
seznam_hodnot = Hodnoty()
dalsi_seznam = Hodnoty()
a_jeste_jeden = Hodnoty()


while True:
    """ Tohle je smyčka, která to celé obsluhuje """
    # Zeptáme se uživatele na hodnotu
    hodnota = int(input("Zadej hodnotu: "))

    if hodnota == 0:
        # Ukončení po zadání nuly
        break
    else:
        # Pokud zadal cokoliv jiného než nulu
        seznam_hodnot.pridej_hodnotu(hodnota)


# Až doběhne zadávání, vypíšeme
seznam_hodnot.vypis_hodnoty()

# Smažeme všechny hodnoty
seznam_hodnot.smaz_seznam()
seznam_hodnot.vypis_hodnoty()

