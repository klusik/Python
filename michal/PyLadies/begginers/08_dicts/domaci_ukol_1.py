'''
Napiš funkci, která vrátí sumu všech klíčů a sumu všech
hodnot ve slovníku, který dostane jako argument. K vyzkoušení
můžeš použít slovník z minulé úlohy. Například:

>>> slovnik = mocniny(4)
>>> soucet_klicu_a_hodnot(slovnik)
(10, 30)
'''

def squares(number):
    d = {}
    for i in range(1,number):
        d[i] = i * i

    sumkeys = sum(d.keys())        
    sumvals = sum(d.values())
    
    return sumkeys, sumvals

print(squares(9))