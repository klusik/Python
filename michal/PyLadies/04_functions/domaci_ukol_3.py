'''
Napiš funkci, která vypíše do jednoho řádku prvních 11 násobků zvoleného čísla 
(argument funkce). Např.: pro vstup 2 vypíše funkce 
0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20.
'''

def nasobky(n):
    for i in range(11):
        nasobek = n * i
        print(nasobek)

nasobky(2)
