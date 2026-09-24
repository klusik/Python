"""
    Zadání 5: Velmi pokročilé

    Vytvořte prográmek, který načte výrobky ze souboru a jejich ceny.

    Program se zeptá uživatele na počet kusů výrobku, který chce nakoupit
    a cenové rozmezí (miminální cena, maximální cena, stačí int() hodnoty).

    Prográmek poté vytvoří nákupní seznam, který bude obsahovat daný počet výrobků
    a celková cena bude v rozmezí zadaných hodnot.

    Pokud takový nákup nepůjde vytvořit, program vypíše, že takový nákup nelze vytvořit
    a nabídne uživateli, že může znovu zadat pravidla.

    Výsledný výstup pak bude vypadat třeba takto:

        PC: Kolik kusů výrobků nakoupit?
        U:  10
        PC: Jaká je minimální cena nákupu?
        U:  100
        PC: Jaká je maximální cena nákupu?
        U: 150

        Nákup bude obsahovat:
        6 × kaiserka po 4.5, celkem 27 Kč
        4 × mléko po 22, celkem 88 Kč

        Celková cena nákupu 115 Kč.
"""

def nacti_seznam():
    """
    Přečte soubor a vytvoří datovou strukturu
    @return: slovník seřazených výrobků
    """
    with open('vyrobky.txt', 'r', encoding='utf-8') as f_vyrobky:
        vyrobky = f_vyrobky.read().split('\n')


    slovnik_vystup = dict()

    for vyrobek in vyrobky:
        vyrobek_jmeno, vyrobek_cena = vyrobek.split()
        slovnik_vystup[vyrobek_jmeno] = vyrobek_cena


    return dict(sorted(slovnik_vystup.items(), key = lambda item: item[1], reverse=True))

def cena_nakupniho_seznamu(nakupni_seznam):
    """
    Vypočítá celkovou cenu seznamu
    @param nakupni_seznam: nákupní seznam
    @return: float s cenou nákupního seznamu
    """

    return float(sum(nakupni_seznam.values()))

def main():
    while True:
        # Zadání dat od uživatele
        pocet = int(input("Zadej počet výrobků: "))
        cena_min = int(input("Zadej minimální cenu: "))
        cena_max = int(input("Zadej maximální cenu: "))

        if pocet > 0 and (1 <= cena_min < cena_max):
            # Načtu seřazený slovník výrobků
            vyrobky = nacti_seznam()

            # Procházím nejdražší výrobky a snažím se vyrobit nákup tak, abych se trefil mezi rozsahy ceny.
            # Pokud se mi podaří trefit nejdražšími výrobky do ceny, program je hotov.
            # Pokud cenu "přetáhnu," pak uberu poslední nejdražší výrboek z nákupního seznamu
            # a zkusím přidat levnější.
            # Pokud se ani toto nepodaří, uberu i ten levnější a přidám ještě levnější etc.

            nakupni_seznam = dict()

            while True:
                # Vnitřní smyčka řešící fitnutí výrobků do ceny
                if len(vyrobky):
                    # Máme-li ještě nějaké výrobky
                    if cena_nakupniho_seznamu(nakupni_seznam) > cena_max:
                        # přehnali jsme hodnotu
                        # je třeba ze seznamu odstranit poslední přidanou položku
                        nakupni_seznam.pop()

                        # nadále budeme ignorovat drahý výrobek, odstraníme ho
                        vyrobky.pop(0)  # odstranění nejdražšího výrobku z výrobků
                        continue  # vnitřní smyčka běží dál
                    else:
                        # Výrobkem jsme nepřesáhli max_cenu
                        if cena_min <= cena_nakupniho_seznamu(nakupni_seznam) <= cena_max:
                            # trefili jsme se
                            break
                        else:
                            # máme málo, přidáme další položku do seznamu
                            if list(vyrobky.keys())[0] in nakupni_seznam:
                                # výrobek už jsme použili, jen zvýšíme jeho počet
                                nakupni_seznam[list(vyrobky.keys())[0]] += 1
                            else:
                                # výrobek v nákupním seznmau ještě nemáme
                                nakupni_seznam[list(vyrobky.keys())[0]] = 1
                else:
                    # Nemáme výrobky
                    break


            # Kontrola, jestli máme něco v nákupním seznamu
            if len(nakupni_seznam):
                print("Nákupní seznam vypadá takto: ")
                print(nakupni_seznam)
            else:
                print("Nepodařilo se sestavit vhodný nákupní seznam.")





if __name__ == "__main__":
    main()