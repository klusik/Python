'''
Změn funkci z předchozího úkolu tak, aby funkce měla tři argumenty – číslo, 
počet vypisovaných násobků, znak pro oddělení vypsaných násobků.
'''

def nasobky(n,nasobek, delimiter):
    ''' Vrat n nasobek zadaneho cisla, vysledky oddel delimiterem
    # INPUT
    n - cislo, ktere bude nasobeno, integer
    nasobek - kolikrat bude nasobeno n, integer
    delimiter - oddelovaci znak, string

    # OUTPUT
    tisk do konzole
    '''
    for cislo in range(nasobek):
        vysledek = cislo * nasobek
        print(vysledek, end = str(delimiter)+'\n')

nasobky(2, 8, 'xFF')