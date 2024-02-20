"""
    Zadání 3:

    Vyrobte porgram, který vytvoří nákupní seznam
    s cenou sečtenou podle toho, co si uživatel vymyslí.

    Zadávání bude vypadat např. takto:

    Výpis: Máte k dispozici následující výrobky: mléko, mouka, ... (výpis všech).
    Který výrobek zakoupit?

    uživatel zadá třeba 'mléko'

    program se zeptá: Kolik?

    uživatel zadá třeba 3

    Program si připočte k ceně cenu 3×22 za mléka.

    Na konci prográmek vypíše, kolik Kč bude takový nákup stát.
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

# Tady se budu uživatele ptát na výrobek atd.
celkova_cena = 0
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

        celkova_cena += cena_vyrobku * pocet_uzivatel
    else:
        print("Výrobek není v seznamu, zadejte validní výrobkem!")

print(f"Celková cena výrobků je {celkova_cena} Kč.")

