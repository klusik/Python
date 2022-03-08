'''
Nejprve si napiš funkci, která rozhodne jestli zadané číslo je liché. Funkci
si vhodně pojmenuj. Pokud nevíš jak zjistíš, že dané číslo je liché, zkus se 
podívat na operátor modulo % a zamysli se, jak by se dal použít pro vyřešení 
úkolu.
'''
def not_even(n):
    '''
    Rozhodni, zda je zadane cislo liche
    # INPUT
    n - cele cislo, integer
    # OUTPUT
    True/False - bool
    '''

    if n%2 == 0:
        return True
    else:
        return False
    
print(not_even(5))
