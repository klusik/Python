""" Ahoj, zase budu označovat #RK# to, co komentuju """

# Celá funkční hra
from random import randrange

pocet_znaku = 20


def nova_hra():
    return pocet_znaku * "-"


def vyhodnot(pole):
    pole = pole.lower()

    if "xxx" in pole:
        return 'x'
    elif "ooo" in pole:
        return 'o'
    elif '-' not in pole:
        return '!'
    else:
        return '-'


def tah(pole, cislo_policka, symbol):
    pole = pole.lower()
    pole = list(pole)
    pole[cislo_policka] = symbol

    return ''.join(pole)


def tah_je_validni(pole, index):
    try:
        index = int(index)
    except ValueError:
        print("Zadejte číslo")
        return False

    if index < 0 or index >= pocet_znaku:
        print("Políčko neexistuje")
        return False

    if pole[index] != '-':
        print("Políčko je již obsazené")
        return False

    return True


def tah_hrace(pole):
    while True:

        index = input("Tah hráče na pozici: ")
        if tah_je_validni(pole, index):
            break

    index = int(index)

    return tah(pole, index, 'X')


def tah_pocitace(pole):
    while True:

        index = randrange(pocet_znaku)
        if tah_je_validni(pole, index):
            break

    print("Tah počítače:")

    return tah(pole, index, 'O')


def vypis_stav(pole, stav):
    if stav == 'x':
        print("Hráč vyhrál!")
    elif stav == 'o':
        print("Počítač vyhrál!")
    elif stav == '!':
        print("Remíza!")

    print(pole)


def piskvorky1d():
    pole = nova_hra()

    while vyhodnot(pole) == '-':

        pole = tah_hrace(pole)
        stav = vyhodnot(pole)
        vypis_stav(pole, stav)

        if stav != '-':
            break

        pole = tah_pocitace(pole)
        stav = vyhodnot(pole)
        vypis_stav(pole, stav)

    print("Konec hry!")


piskvorky1d()