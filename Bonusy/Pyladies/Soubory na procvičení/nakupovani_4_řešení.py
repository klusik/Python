"""
    Zadání 4: (mírně už pokročilé pro ty, kteří jsou už trošku napřed)

    Vytvořte prográmek z úkolu 3, ale bude si pamatovat nejen celkovou cenu,
    ale kompletně celý nákup, tedy na konci vypíše třeba:

    Budete nakupovat:
    3krát mléko, celkem 3 × 22 = 66 Kč
    1krát mouka, celkem 1 × 25 = 25 Kč
    5krát kaiserka, celkem 5 × 4.5 = 22,5 Kč

    Celková cena nákupu: 113,5 Kč
"""
def vypis_vyrobky():
    """
    Funkce vypíše výrobky, které máme k dispozici
    :return: None
    """
    with open('vyrobky.txt', 'r', encoding='utf-8') as f_vyrobky:
        vyrobky = f_vyrobky.read().split('\n')

    for vyrobek in vyrobky:
        print(f"{vyrobek.split()[0]}: {vyrobek.split()[1]}")

def je_vyrobek_v_seznamu(vyrobek_od_uzivatele):
    """
    Funkce projde soubor a zjistí, jestli zadaný výrobek existuje
    v daném souboru
    :param vyrobek: string s názvem výrobku
    :return: True/False podle toho, jestli obsahuje či nikoliv
    """

    with open('vyrobky.txt', 'r', encoding='utf-8') as f_vyrobky:
        vyrobky = f_vyrobky.read().split('\n')

    for vyrobek in vyrobky:
        if vyrobek.split()[0] == vyrobek_od_uzivatele:
            # Výrobek nalezen, dál nemjusíme hledat
            return True

    # Výrobek se za celou dobu nepodařilo najít
    return False

def zjisti_cenu_vyrobku(vyrobek_uzivatel):
    with open('vyrobky.txt', 'r', encoding='utf-8') as f_vyrobky:
        vyrobky = f_vyrobky.read().split('\n')

    for vyrobek in vyrobky:
        if vyrobek.split()[0] == vyrobek_uzivatel:
            return float(vyrobek.split()[1])

    print("Něco je špatně :-)")

def vycisti_soubor():
    """
    Vyčistí soubor
    """
    with open('seznam.txt', 'w') as f_cisteni:
        f_cisteni.write('')

def uloz_vyrobek_do_souboru(vyrobek, cena, mnozstvi):
    with open('seznam.txt', 'a', encoding='utf-8') as f_seznam:
        f_seznam.write(f"{vyrobek} {cena} {mnozstvi}\n")

def precti_nakupni_seznam():
    try:
        with open('seznam.txt', 'r', encoding='utf-8') as f_seznam:
            seznam = f_seznam.read().split('\n')

        # vyčištění výstupního textu (příprava)
        vystupni_text = ""
        celkova_cena = 0

        for polozka in seznam:
            polozky = polozka.split()

            if len(polozky) == 3:
                vystupni_text += f"{polozky[0]} za {polozky[1]} Kč, počet: {polozky[2]}\n"

                celkova_cena += float(polozky[1]) * float(polozky[2])

        vystupni_text += f"\nCelková cena je {celkova_cena} Kč."

        print(vystupni_text)
        return(vystupni_text)

    except FileNotFoundError as fnf_err:
        print("Nákupní seznam je prázdný :-)")
        return None

# Tady se budu uživatele ptát na výrobek atd.
# Vyčistíme soubor
celkova_cena = 0
vycisti_soubor()
while True:
    # Zeptáme se uživatele na název výrobku
    print(f"Celková cena nákupu je zatím {celkova_cena} Kč.")
    print("K dispizici máme následující výrobky: ")
    vypis_vyrobky()
    vyrobek_uzivatel = input("Jaký výrobek bys chtěl? ")
    # Řeším konec běhu (cyklu)
    if vyrobek_uzivatel == "konec":
        break

    # Řeším výrobky
    if je_vyrobek_v_seznamu(vyrobek_uzivatel):
        # Je v seznamu, můžeme se zeptat na počet výrobků
        pocet_uzivatel = int(input("Kolik tohoto výrobku chceš? "))

        # Připočtu cenu ze souboru vynásobenou počtem výrobků k celkové ceně
        cena_vyrobku = zjisti_cenu_vyrobku(vyrobek_uzivatel)

        # celkova_cena = ceslkova_cena + cena_vyrobku * pocet_uzivatel
        uloz_vyrobek_do_souboru(vyrobek_uzivatel, cena_vyrobku, pocet_uzivatel)
    else:
        print("Výrobek není v seznamu, zadejte validní výrobkem!")

precti_nakupni_seznam()

