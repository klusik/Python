'''
Topic: Functions
this file is intended as a lecture record 
date: 8.3.2022 (DD.MM.YYYY)
prednasejici: jakub cervinka
'''

# na zacatku opakovani
# hint 1 - pojmenovavejte si promenne popisne

'''
opakovani prikladu
X X X X X X
X         X
X         X
X         X
X         X
X X X X X X
'''

# podminky jsou 'sheer beauty'

from tkinter.tix import CheckList


pocet_radku = 5
pocet_sloupcu = 5

for cislo_radku in range(pocet_radku):
    for cislo_sloupce in range(pocet_sloupcu):
        # pokud jsem uvnitr, napisu mezeru
        if 0 < cislo_radku < pocet_radku -1 \
            and 0 < cislo_sloupce < pocet_sloupcu -1:
            print(' ', end='')
        # jinak jsem na okrji, pisu 'X'
        else:
            print('X', end='')
    print()

# DEBUGovani

'''
beh programu se zastavi na zvolenem breakpointu
v zavislosti na editoru se ma zobrazit prehled promennych
breakpointu muze byt vic
nezajimavy kod mezi breakpointy se preskoci pomoci continue
step over je nasledujici krok
step in a step out je spojeno s funkcema
to si ukazeme za chvili
stay tuned :)
'''

# jdeme na funkce

'''
teoreticky uvod
'''
# chci napsat fci na urceni poctu znaku

veta = 'ahoj svete'
pocet_znaku = 0
for c in veta:
    pocet_znaku += 1
print(f'pocet znaku je {pocet_znaku}')

# taky existuje funkce len

print(f'pocet znaku s pouzitim len je : {len(veta)}')

jmeno = 'michal'
celkovy_pocet = len(veta) + len(jmeno)
print(f'celkovy pocet znaku {celkovy_pocet}')

# HROZNE DULEZITE NA MULTILINE STRINGY!!!!!!!!!!!!!!!!!!!!!
from textwrap import dedent

# napiseme si vlastni funkci!!!
def vypocti_obsah(delka, sirka):
    docstring = dedent('''
                tohle
                    je string 
                na vic radek
                ''')
    print(docstring)
    obsah = delka * sirka
    return obsah

rozloha_prvni_parcely = vypocti_obsah(100,50)
rozloha_druhe_parcely = vypocti_obsah(60,40)

print(
    f'rozloha prvni parcely je: {rozloha_prvni_parcely}\n'
    f'rozloha druhe parcely je: {rozloha_druhe_parcely}'
    )

# zpet k DEBUGovani
'''
setp in vleze do funkce tam, kde je volana
step over by proste vzal vystup z funkce jako dany
step out z funkce vyleze predcasne
'''

# vida, tak na zaklade toho meho dotazu vyse jsem narazili na docstring

def urci_znamku(name, score):
    '''
    vypis znamku podle score
    vrat znamku jako int
    '''
    if score < 40:
        print(f'{name} neprosel')
        znamka = 4
    elif score >= 40 and score < 60:
        print(f'{name} ma trojku')
        znamka = 3
    elif score >= 60 and score < 80:
        print(f'{name} dosahl na dvojku')
        znamka = 2
    elif score >= 80 and score < 98:
        print(f'{name} dosahl hodnoceni vyborne')
        znamka = 1
    elif score >= 98 and score <= 100:
        print(f'{name} dosahl na vyznamenani')
        znamka = 1
    else:
        print(f'{name} ma neplatne hodnoceni')
urci_znamku('Michal Ukrutny', 88)

# nove zadani: napiste funkci, ktera nakresli n-uhelnik
# IMPORTS
import turtle
def nuhelnik(n):

    for i in range(n):
        turtle.forward(500/n)
        turtle.left(360/n)
    # turtle.exitonclick()

nuhelnik(8)

# nove zadani: posun se doprava o n
def right_shift(shift_length):
    turtle.penup()
    turtle.forward(shift_length)
    turtle.pendown()
# turtle.exitonclick()
for pocet_uhlu in range(5, 9):
    nuhelnik(pocet_uhlu)
    right_shift(100)

turtle.exitonclick()