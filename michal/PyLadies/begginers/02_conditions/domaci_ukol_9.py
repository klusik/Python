'''Tento projekt doplňuje program ze srazu. Zkombinuj program z předchozího úkolu (č. 7) s programem kámen-nůžky-papír a nastav tah_pocitace na:

    'kámen', pokud je cislo 0,
    'nůžky', pokud je cislo 1,
    jinak na 'papír'.

Kód ze srazu najdeš i zde(link nize), ale výrazně ho stačí zjednodušit jen na tah_pocitace.
link: https://naucse.python.cz/2021/plzen-podzim-2021/beginners/comparisons/
'''
# automatizace tahu pocitace
from random import randrange
CML = randrange(2) # CML = Centralni Mozek Lidstva
if CML == 0:
    CML = "kámen"
elif CML == 1:
    CML = 'nůžky'
else:
    CML = 'papír'

hooman = input('kámen, nůžky, nebo papír? ')

if hooman == 'kámen':
    if CML == 'kámen':
        print('Plichta.')
    elif CML == 'nůžky':
        print('Vyhrála jsi!')
    elif CML == 'papír':
        print('Počítač vyhrál.')
elif hooman == 'nůžky':
    if CML == 'kámen':
        print('Počítač vyhrál.')
    elif CML == 'nůžky':
        print('Plichta.')
    elif CML == 'papír':
        print('Vyhrála jsi!')
elif hooman == 'papír':
    if CML == 'kámen':
        print('Vyhrála jsi!')
    elif CML == 'nůžky':
        print('Počítač vyhrál.')
    elif CML == 'papír':
        print('Plichta.')
else:
    print('Nerozumím.')