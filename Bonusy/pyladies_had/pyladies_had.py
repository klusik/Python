"""
    Had z Pyladies
"""

class Had:
    def __init__(self):
        pass

    def __str__(self):
        """ mačkáš mi hada """



def uprav_mapu(mapa: list, seznam_souradnic: list = None) -> list:
    rozmery_mapy = 10

    if not mapa:
        for radek in range(rozmery_mapy):
            mapa.append(10 * ['.'])

    if seznam_souradnic:
        for sloupec, radek in seznam_souradnic:
            mapa[radek][sloupec] = 'X'

    return (mapa)


def nakresli_mapu(mapa: list) -> list:
    for radek, obsah_radku in enumerate(mapa):
        for sloupec, obsah_sloupce in enumerate(obsah_radku):
            print(obsah_sloupce, end=' ')
        print()

    return mapa


mapa = list()

kurzor_x = 5
kurzor_y = 5
mapa = uprav_mapu(mapa, [(kurzor_x, kurzor_y)])

nakresli_mapu(mapa)

while True:
    uzivatel_smer = input("Zadej smer (w, s, a, d): ")
    if uzivatel_smer in ['w', 's', 'a', 'd', 'konec']:
        if uzivatel_smer == 'w':  # hore
            kurzor_y -= 1
        elif uzivatel_smer == 's':  # dole
            kurzor_y += 1
        elif uzivatel_smer == 'a':  # levo
            kurzor_x -= 1
        elif uzivatel_smer == 'd':  # pravo
            kurzor_x += 1
        else:
            break

        mapa = uprav_mapu(mapa, [(kurzor_x, kurzor_y)])

        nakresli_mapu(mapa)
