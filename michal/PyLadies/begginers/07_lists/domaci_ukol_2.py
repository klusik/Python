'''
Napiš funkci, která dostane dva seznamy jmen domácích zvířat a vrátí tři seznamy:

    zvířata, která jsou v obou seznamech (bez opakování, tedy sjednocení množin: první ∪ druhá),
    zvířata, která jsou jen v prvním seznamu (bez opakování, tedy rozdíl množin: první - druhá),
    zvířata, která jsou jen ve druhém seznamu (bez opakování, tedy rozdíl množin: druhá - první).
'''

# This is the way I would like to solve the task:
def lists_of_animals(domestic_animals, pests):
    union_list = list(set(domestic_animals) | set(pests))
    only_first = list(set(domestic_animals) - set(pests))
    only_second = list(set(pests) - set(domestic_animals))
    return union_list, only_first, only_second

# RUNTIME
print(lists_of_animals(['cow', 'chicken', 'goat'], ['roach', 'bat', 'rat']))

# This is the solution you want to see as per my opinion
def animalists(domestic_animals, pests):
    result_union = [] # domestic_animals + pests
    result_first = [] # domestic_animals - pests
    result_second = [] # pests - domestic_animals
    for animal in domestic_animals:
        result_union.append(animal)
        # domestic_animals - pests
        if animal not in pests:
            result_first.append(animal)

    for pest in pests:
        result_union.append(pest)
        # pests - domestic_animals
        if pest not in domestic_animals:
            result_second.append(pest)

    return result_union, result_first, result_second

domestic_animals = ['chicken', 'rat', 'cow']
pests = ['rat', 'bat', 'centipede']

# RUNTIME
print(animalists(domestic_animals, pests))