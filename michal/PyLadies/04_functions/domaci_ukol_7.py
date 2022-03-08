'''
Napiš funkci která pro zadaný počet N vygeneruje N náhodných čísel, každé 
vygenerované číslo vypíše spolu s informací zda-li je liché či nikoliv. 
Tuto funkci si pojmenuj jednoduše lichost_nahodnych_cisel(pocet).
'''
import random
def lichost_nahodnych_cisel(pocet):
    '''
    Vypis n nahodnych cisel, pro kazde rozhodni, zda je sude.
    # INPUT
    pocet - pocet generovanych cisel, integer
    # OUTPUT
    tisk do konzole nahodne cislo, True/False
    '''
    for i in range(pocet):
        # vygeneruj nahodne cislo
        cislo = random.randrange(100)

        # kdyz je sude
        if cislo%2 == 0:
            print(f'Pseudonahodne cislo {cislo} je sude.')
        # kdyz je liche
        else:
            print(f'Pseudonahodne cislo {cislo} je liche.')

lichost_nahodnych_cisel(10)