"""
Jednoduchý progámek na součet dvou čísel.
Napiš jednoduchý prográmek, který se uživatele zeptá na dvě celá čísla.
Prográmek vypíše součet tutěch čísel.
"""


def uzivatelsky_vstup() -> tuple[float, float]:
    """ Tato funkce se zeptá uživatele na dvě čísla. """

    try:
        ahoj = float(input("Zadej první číslo: "))
        franto = float(input("Zadej druhé číslo: "))

        # Tuple (1, 2)
        return ahoj, franto

    except KeyboardInterrupt:
        print("Nebylo nic zadáno.")
        raise  # Znovu vytvořím výjimku, takže další běh programu ji umí zachytit.


def soucet(maruska: float, dagmar: float) -> float:
    """ Tato funkce vrátí součet dvou čísel"""
    return round(maruska + dagmar, ndigits=7)


if __name__ == "__main__":
    """ Spustili jsme program """

    # Tady se zeptáme uživatele na vstupní hodnoty
    try:
        cislo_1, cislo_2 = uzivatelsky_vstup()

    except KeyboardInterrupt:
        print("Nic se sčítat nebude, ahoj :-)")
        exit()

    # Tady to chci vypočítat
    vysledek = soucet(cislo_1, cislo_2)

    # Tady to chci vypsat
    print(f"Součet čísel {cislo_1} a {cislo_2} je {vysledek} :-)")
