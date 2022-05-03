'''
Napiš funkci, která ze seznamu jmen domácích zvířat (zadaný argumentem) 
vrátí ta, která začínají na písmeno k.
'''

def animals(list_of_animals, first_letter):
    '''
    From list of animals return animals starting with given letter

    INPUT
    list_of_animals = given list of animals, list of strings
    first_letter = starting letter, string

    OUTPUT
    result = list of all animals starting with given letter, list of strings
    '''
    result = []
    for animal in list_of_animals:
        if animal.startswith(first_letter):
            result.append(animal)

    return result

anim = ['kiwi', 'cock', 'hen', 'cat', 'kangaroo', 'cow']
# RUNTIME
print(animals(anim, 'k'))
