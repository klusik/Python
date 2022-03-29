'''
Napiš funkci, která dostane dva seznamy jmen domácích zvířat a vrátí tři seznamy:

    zvířata, která jsou v obou seznamech (bez opakování, tedy sjednocení množin: první ∪ druhá),
    zvířata, která jsou jen v prvním seznamu (bez opakování, tedy rozdíl množin: první - druhá),
    zvířata, která jsou jen ve druhém seznamu (bez opakování, tedy rozdíl množin: druhá - první).
'''

def lists_of_animals(domestic_animals, pests):
    union_list = list(set(domestic_animals) + set(pests))
    only_first = list(set(domestic_animals) - set(pests))
    only_second = list(set(pests) - set(domestic_animals))
    return union_list, only_first, only_second

print(lists_of_animals(['cow', 'chicken', 'goat'], ['roach', 'bat', 'rat']))