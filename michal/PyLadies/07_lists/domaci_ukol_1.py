'''
Napiš program, který na konec seznamu zvířat přidá zvíře zadané uživatelem, 
ale pozor jen, pokud tam ještě není. Upravený seznam program vypíše.
'''

def add_missing(animal, list_of_animals):
    '''
    Add missing animal into list

    INPUT
    animal = animail under test, string
    list_of_animals = reference list of animals, list

    OUTPUT
    via print() complete list of animals
    '''
    
    if animal not in list_of_animals:
        list_of_animals.append(animal)
        print(f'animal {animal} added at the end of list of animals')
    else:
        print(f'animal {animal} already present in the list of animals')

    print(f'complete list of animals: {list_of_animals}')

add_missing('anaconda', ['pes', 
                         'kočka', 
                         'králík', 
                         'had', 
                         'hamster', 
                         'fish', 
                         'shrimp', 
                         'snail'])
                         