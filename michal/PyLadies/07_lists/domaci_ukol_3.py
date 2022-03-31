'''
Napiš funkci, která ze seznamu jmen domácích zvířat (zadaný argumentem) vrátí
ta, která jsou kratší než 5 písmen.
'''

def short_animals(list_of_animals):
    result = []
    for animal in list_of_animals:
        if len(animal) < 5:
            result.append(animal)

    return result

shorts = ['centipede', 'anaconda', 'ant', 'duck', 'hawk']

print(short_animals(shorts))
