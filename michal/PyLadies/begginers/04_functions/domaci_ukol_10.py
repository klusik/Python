'''
Změň program Kámen, Nůžky, Papír tak, aby opakoval hru dokud uživatel nezadá konec.
'''

def rps():
    '''
    Hraj hru kamen/nuzky/papir. Zeptej se uzivatele na volbu, generuj tah
    pocitace, vyhodnot vysledek.
    vyhra: nuzky > papir, papir > kamen, kamen > nuzky

    # INPUT
    hooman - volba kamen/nuzky/papir, string

    # OUTPUT
    tisk do konzole
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

    print("tah pocitace: " + CML)
    # Plichta
    if hooman == CML:
        print("plichta")
    # Vyhra
    elif (hooman == "nůžky" and CML == "papír") or \
        (hooman == "kámen" and CML == "nůžky") or \
        (hooman == "papír" and CML == "kámen"):
        print("Vyhra")

    # Prohra
    else:
        print("Prohra")

while True:
    rps()
    pokracovat = input('Prejete si hrat znovu? vlozte p - pokracovat'
                        'nebo k - konec: ')
    if pokracovat == 'p':
        continue
    elif pokracovat == 'k':
        break
    else:
        print(f'nerozumim vasi volbe {pokracovat}. Ukoncuji program.')
        break