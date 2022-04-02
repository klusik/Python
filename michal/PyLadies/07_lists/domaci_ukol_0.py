'''
Udělej si seznam domácích zvířat. Budeš ho potřebovat v dalších úlohách. 
Domácí zvířata známe tato: "pes", "kočka", "králík", "had", můžeš přidat 
nějaké svoje oblíbené, žádné ale neubírej.

Napiš funkci, která přebere seznam a slovo a zjistí, jestli je to slovo v 
seznamu domácích zvířat.

„Zjistí“ znamená, že funkce vrátí True nebo False.
'''

def animal_detector(animal, list_of_animals):
    '''
    Check if given animal is in given list of animals

    INPUTS
    animal = animal under test, string
    list_of_animals = reference list against which test is being held, list

    OUTPUTS
    True/False = True if found, bool
    '''

    if animal in list_of_animals:
        return True
    else:
        return False
animal_list = ['pes', 
                'kočka', 
                'králík', 
                'had', 
                'hamster', 
                'fish', 
                'shrimp', 
                'snail']
# RUNTIME
print(animal_detector('horse', animal_list))
