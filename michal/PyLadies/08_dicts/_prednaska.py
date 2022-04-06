'''
Topic: dicts
this file is intended as a lecture record 
date: 05.04.2022 (DD.MM.YYYY)
prednasejici: jakub cervinka
'''

# jak se referencuje hodnota z dictu
pocet_kroku_dct = {

    'pondeli': 100,
    'utery': 2586,
    'streda': 8465,
    'ctvrtek': 8464,
    'patek': 6864,
    'sobota': 30,
    'nedele': 15
}

print(pocet_kroku_dct['nedele'])

# lze zanorovat
test = {
    1: 'ferrari',
    2: ['honda', 'yammaha']
}

print(test[1])
print(test[2][1])

# jako klic, na zacatecnickem levelu, lze pouzit cislo nebo slovo

# jak zadat nova data do slovniku
test['nova_polozka'] = ['schumi', 'marquez', 'rossi']

# mazani ze slovniku
del test['nova_polozka'][0]

print(test)

# lze zanorovat slovnik do slovniku

znamky = {
    'pepicek': {
        'matematika':[],
        'cestina':[],
        'informatika':[]
    },
    'maruska': {
        'matematika':[],
        'cestina':[],
        'gender studies':[]
    }
}

znamky['pepicek']['cestina'].append(3)
print(znamky)

# slovnik je iterable
for i in pocet_kroku_dct.items(): # nebo .keys(), nebo .values()
    print(i)

# unpacking
for den, kroky in pocet_kroku_dct.items():
    print(f'{den} jsem usel {kroky * 0.8} metru')

print(f'celkem jsem usel {sum(pocet_kroku_dct.values())}')

pocet_kroku_dct['pondeli'] += 150

# metoda update
prvni = {
    'a' : 1,
    'b': 2,
    'c': 3,
}

druhy = {
    #'a': 10,
    'b': 20,
    'c': 30,
    'd': 40
}

prvni.update(druhy)
print(prvni)

# home work spoiler alert
cisla = {}

for n in range(10):
    cisla[n] = n * n

print(cisla)

# PrettyPrint!!!
import pprint
pprint.pprint(cisla)

pprint.pprint(znamky)

# metoda .get()
print(znamky.get('ondra', 'neni v seznamu'))
print(znamky.get('pepicek', 'neni v seznamu'))

print(pocet_kroku_dct.get('pondeli', 0)) # pokud neni key v dict, vrati 0

# metoda .pop()
pondeli = pocet_kroku_dct.pop('pondeli')
print(pondeli)
pprint.pprint(pocet_kroku_dct)
# print(pocet_kroku_dct['pondeli']) # tohle da key error

# maly testik
print('pondeli' in pocet_kroku_dct)

# metoda popitem odstrani nahodny prvek z dictu. nema prakticke pouziti
# pokud nepisete metodu sadisticky dozorce...