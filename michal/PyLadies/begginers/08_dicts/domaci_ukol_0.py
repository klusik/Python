'''
Napiš funkci, která pro argumentem zadané číslo n vytvoří a vrátí slovník, 
kde jako klíče budou čísla od jedné do n a jako hodnoty k nim jejich 
druhé mocniny. Například:

>>> mocniny(4)
{1: 1, 2: 4, 3: 9, 4: 16}

'''

def squares(number):
    d = {}
    for i in range(1,number):
        d[i] = i * i
        
    return d

print(squares(9))