
import random

otazky = ['Kdo?', 'S kým?', 'Co dělali?', 'Kde?', 'Kdy?', 'Proč?']

def sestav_vetu(otazky):
    slovnik = {}
    # zadávání odpovědí
    for otazka in otazky:
        slovnik[otazka] = []
        for i in range(2):
            # dotaz: Proč je nutné to rozsekat na víc řádků? NoneType has not atribute append,
            # přitom to jen uložím do proměnné a už to funguje
            pomocny = slovnik.get(otazka)
            pomocny.append(input(otazka + ' '))
            slovnik[otazka] = pomocny
    # vybírání z odpovědí (sestavení věty)
    veta = ''
    for odpovedi in slovnik.values():
        veta += random.choice(odpovedi) + ' '
    veta += '.'
    return veta

print(sestav_vetu(otazky))