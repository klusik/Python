def vyber_znaku():
    znak_hrac = '?'
    while znak_hrac != 'o' and znak_hrac != 'x':
        znak_hrac = input('hrajes o nebo x?')
    return znak_hrac


def vyhodnotit(znak, pole):
    return znak * 3 in pole
    if znak * 3 in pole:
        return 1
    elif '-' in pole:
        return 0
    else:
        return -1


def tah_hrace(znak, pole):
    while True:
        tah = int(input('zadej cislo pozice pro tah:'))
        if tah >= 0 and tah <= 19 and pole[tah] == '-':
            pole[tah] = znak
            return pole


def tah_pocitace(znak, pole):
    from random import randrange
    while True:
        tah = randrange(0, 20)
        if pole[tah] == '-':
            pole[tah] = znak
            return pole


def piskvorky():
    hraci_pole = ['-'] * 20
    znak_hrac = vyber_znaku()
    if znak_hrac == 'o':
        znak_pocitac = 'x'
    else:
        znak_pocitac = 'o'

    cislo_tahu = 0
    while True:
        hraci_pole = tah_hrace(znak_hrac, hraci_pole)
        cislo_tahu = cislo_tahu + 1
        print(str(cislo_tahu) + '. kolo', ' '.join(hraci_pole))
        vysledek = vyhodnotit(znak_hrac, ''.join(hraci_pole))
        if vysledek == 1:
            print('hrac zvitezil')
            break
        elif vysledek == -1:
            print('remiza')
            break
        hraci_pole = tah_pocitace(znak_pocitac, hraci_pole)
        cislo_tahu = cislo_tahu + 1
        print(str(cislo_tahu) + '. kolo', ' '.join(hraci_pole))
        vysledek = vyhodnotit(znak_pocitac, ''.join(hraci_pole))
        if vysledek == 1:
            print('pocitac zvitezil')
            break
        elif vysledek == -1:
            print('remiza')
            break


piskvorky()
