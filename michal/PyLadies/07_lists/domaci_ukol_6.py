'''
Had byl pyšný na to, že je v abecedě první. Dokud nepřiletěla "andulka".

Abys hada uklidnila, vytvoř funkci, která zvířata seřadí podle abecedy, 
ale bude ignorovat první písmeno t.j. vrátí:

"had",
"pes",
"andulka",
"kočka",
"králík".

Postup:

    Máš seznam hodnot, které chceš seřadit podle nějakého klíče. 
    Klíč se dá z každé hodnoty vypočítat.
    Vytvoř seznam dvojic (klíč, hodnota).
    Seřaď tento seznam dvojic 
'''

def sort_animals(list_of_animals):
    '''
    Sort list of animals based on second letter

    INPUT
    list_of_animals = list of animals to be sorted, list of strings

    OUTPUT
    sorted list of animals = sorted list of animals, list of strings
    '''
    return sorted(list_of_animals, key=lambda animal: animal[1])

anim_list = ['had', 'hamster', 'cow', 'turkey', 'mamal']
# RUNTIME
print(sort_animals(anim_list))

# source for lambda function:
# https://docs.python.org/3/howto/sorting.html