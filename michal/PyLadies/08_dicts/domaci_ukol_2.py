'''
Napiš funkci, která vypíše obsah slovníku (klíče a k nim 
náležící hodnoty) na jednotlivé řádky.

Funkci, která něco vypisuje, je vhodné pojmenovat speciálně,
zde třeba vypis_slovnik, aby bylo jasné, že jen vypisuje
a nic nevrací. K vyzkoušení můžeš zase použít slovník
z minulé úlohy. Například:

>>> slovnik = mocniny(4)
>>> vypis_slovnik(slovník)
Klíč 1, hodnota 1
Klíč 2, hodnota 4
Klíč 3, hodnota 9
Klíč 4, hodnota 16
'''
def squares(number):
    d = {}
    for i in range(1,number):
        d[i] = i * i
        
    return d

def dictprint(d):
    for 

d = squares(5)    
dictprint(d)
