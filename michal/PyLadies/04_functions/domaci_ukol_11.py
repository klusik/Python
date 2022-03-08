'''
Změň funkci ano_nebo_ne tak, aby se místo ano se dalo použít i a, místo ne i n
a aby se nebral ohled na velikost písmen a mezery před/za odpovědí.

Textům jako možná nebo no tak určitě by počítač dál neměl rozumět.
'''

def ano_nebo_ne(otazka):
    """Vrátí True nebo False podle odpovědi uživatele"""
    while True:
        odpoved = input(otazka).lower()
        odpoved = odpoved.replace(' ', '')
        if odpoved == 'ano' or odpoved == 'a':
            return True
        elif odpoved == 'ne' or odpoved == 'n':
            return False
        # bez pridani else s break se mi zda, ze jde o nekonecnou smycku, dokud
        # user neodpovi dle zadani
        else:
            print('Nerozumím! Odpověz "ano" nebo "ne".')
            break

print(ano_nebo_ne('mas rad klobasy?'))