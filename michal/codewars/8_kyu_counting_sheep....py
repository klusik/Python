# Consider an array of sheep where some sheep may be missing from their place. We need a function that counts the number
# of sheep present in the array (true means present).

# autor zadava pole (list, v pythonu nejsou primo pole) a chce vypocitat, kolik je v nem False hodnot

def count_sheeps(arrayOfSheeps):
    counter = 0
    for i in arrayOfSheeps:
        if i == True:
            counter += 1
    return counter


print(count_sheeps([
    True, True, True, False,
    True, True, True, True,
    True, False, True, False,
    True, False, False, True,
    True, True, True, True,
    False, False, True, True
]))
