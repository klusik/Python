"""
Funkce mám dělané malinko jinak a samy o sobě by
nefungovaly, dávám sem tedy celý prográmek.
Snad to není moc kódu najednou.
"""

from math import floor
from random import randrange


# vytvoření tabulky se samými tečkami na základě poslané velikosti
def vytvor_mapu(rozmery):
    return [['.' for i in range(rozmery["sirka"])] for j in range(rozmery["vyska"])]


def nacist_rozmery(min_rozmery):
    print("Min. rozměry pole (š x v) - " + str(min_rozmery["sirka"]) + "x" + str(min_rozmery["vyska"]))
    rozmery = {"sirka": "", "vyska": ""}

    # načítaní šířky tabulky
    while True:
        sirka = int(input("Zadejte šířku tabulky:"))
        rozmery["sirka"] = sirka
        if sirka >= min_rozmery["sirka"]: break
        print("Nesprávný vstup")

    # náčítání výšky tabulky
    while True:
        vyska = int(input("Zadejte výšku tabulky:"))
        rozmery["vyska"] = vyska
        if vyska >= min_rozmery["vyska"]: break
        print("Nesprávný vstup")

    return rozmery


def nakresli_mapu(rozmery_mapy, souradnice_hada, seznam_ovoce):
    # vytvoření prázdné tabulky
    tabulka = vytvor_mapu(rozmery_mapy)

    # vykreslení hada - hlavu znakem 'O', zbytek těla znakem 'x'
    for had in souradnice_hada:
        if had == souradnice_hada[-1]:
            tabulka[had[1]][had[0]] = "O"
        else:
            tabulka[had[1]][had[0]] = "x"

    # vykreslení ovoce
    for ovoce in seznam_ovoce:
        tabulka[ovoce[1]][ovoce[0]] = "?"

    # vypsání hotové tabulky do konzole
    for radka in tabulka:
        for bunka in radka:
            print(bunka, end=' ')
        print("")


def ovoce(rozmery_mapy, souradnice_hada, seznam_ovoce):
    while True:

        generuj_znovu = False
        pozice_ovoce = (
            randrange(rozmery_mapy["sirka"]),
            randrange(rozmery_mapy["vyska"])
        )

        # pokud se ovoce vygenerovalo v těle hada, generuj znovu
        for had in souradnice_hada:
            if had == pozice_ovoce:
                generuj_znovu = True
                break

        # pokud se ovoce vygenerovalo v jiném ovoci, generuj znovu
        for existujici_ovoce in seznam_ovoce:
            if existujici_ovoce == pozice_ovoce:
                generuj_znovu = True
                break

        # vyskočení z nekonečné smyčky pokud se ovoce vygenerovalo na validní pozici
        if not generuj_znovu:
            return pozice_ovoce


def pohyb(rozmery_mapy, souradnice_hada, seznam_ovoce):
    while True:

        # načítání uživ. inputu
        smer = input("Zadej směr pohybu ('s', 'j', 'v', 'z'):")

        # dle zadaného směru vypočítání nové pozice hlavy hada na základě jeho poslední pozice
        if (smer == 's'):
            pohyb_na = (souradnice_hada[-1][0], souradnice_hada[-1][1] - 1)
        elif smer == "j":
            pohyb_na = (souradnice_hada[-1][0], souradnice_hada[-1][1] + 1)
        elif smer == "v":
            pohyb_na = (souradnice_hada[-1][0] + 1, souradnice_hada[-1][1])
        elif smer == "z":
            pohyb_na = (souradnice_hada[-1][0] - 1, souradnice_hada[-1][1])
        else:
            print("Špatný směr")
            continue

        # pokud had vyjede z mapy - game over
        if pohyb_na[0] < 0 or pohyb_na[0] >= rozmery_mapy["sirka"] or pohyb_na[1] < 0 or pohyb_na[1] >= rozmery_mapy[
            "vyska"]:
            raise ValueError('Game over, vyjel jsi z mapy!')

        # pokud had narazí do svého těla - game over
        for telo in souradnice_hada:
            if telo == pohyb_na:
                raise ValueError('Game over, snědl jsi se!')

        # pokud je nová pozice hlavy hada shodná s pozicí některého z ovocí, odebere se to dané ovoce ze seznamu
        ovoce_snezeno = False
        for ovoce in seznam_ovoce:
            if ovoce == pohyb_na:
                ovoce_snezeno = True
                seznam_ovoce.remove(ovoce)
                break

        # přidání nové pozice hlavy hada do souradnic hada
        souradnice_hada.append(pohyb_na)

        # pokud nebylo snezeno ovoce, umazani ocasu hada
        if not ovoce_snezeno:
            souradnice_hada = souradnice_hada[1:]

        # navraceni novych souradnic hada a seznamu ovoce
        return souradnice_hada, seznam_ovoce


# navraceni informace zda had zabírá celou tablku
def vyhra(rozmery_mapy, souradnice_hada):
    pocet_policek = rozmery_mapy["sirka"] * rozmery_mapy["vyska"]
    volna_policka = pocet_policek - len(souradnice_hada)

    return volna_policka <= 0


def had():
    kolo = 0
    min_rozmery = {"sirka": 2, "vyska": 5}
    # nacitani rozmeru tabulky od uzivatele
    rozmery_mapy = nacist_rozmery(min_rozmery)

    # startovní pozice hlavy hada je cca. uprostred tabulky a začíná s délkou 3 políčka směrem dolů
    start_x = floor(rozmery_mapy["sirka"] / 2)
    start_y = floor(rozmery_mapy["vyska"] / 2)
    souradnice_hada = [(start_x, start_y + 2), (start_x, start_y + 1), (start_x, start_y)]

    # vygenerování startovního ovoce
    seznam_ovoce = [ovoce(rozmery_mapy, souradnice_hada, [])]
    kolo = 0

    # smycka bezici do doby dokud had nezabere celou tabulku
    while not vyhra(rozmery_mapy, souradnice_hada):

        print("----------------------------------------")
        print("Kolo", kolo)

        kolo += 1

        # nove ovoce se pridava kazde 30. kolo a nebo pokud na mape zadne neni
        if (not seznam_ovoce) or not kolo % 30:
            seznam_ovoce.append(ovoce(rozmery_mapy, souradnice_hada, seznam_ovoce))

        # vykresleni tabulky do konzole
        nakresli_mapu(rozmery_mapy, souradnice_hada, seznam_ovoce)

        # prijeti novych udaju o pozici hada a ovoce
        souradnice_hada, seznam_ovoce = pohyb(rozmery_mapy, souradnice_hada, seznam_ovoce)

    # vypis v pripade vyhry hrace
    print("----------------------------------------")
    nakresli_mapu(rozmery_mapy, souradnice_hada, seznam_ovoce)
    print("Výhra!")


# volani hlavni smycky hry
had()
