# bez pouziti cyklu
# napis metodu copy, ktera pouziva jako vstupni parametery:
# array = seznam prvku
# start = zacatek vyberu
# stop = konec vyberu
# place = pozice
# metoda ze zadaneho array vykopiruje prvky mezi start a stop
# a vlozi je na pozici place
# vykopirovane prvky nahrazuji puvodni, velikost listu se tedy nemeni
# nahrazeni prvku dosahnu tak, ze odstranim vsechny zprvky z array od pozice do delka vkladaneho retezce

def copy(array, start, stop, place):
    # your code here [do not change the array in place and do not use loops!]
    # step1: get the abbreviated list
    print('array at start', array)
    b = array[start:stop]
    print('b', b)

    # step2: delete n members from array
    # step2.1: transfer negative limits to positive
    negative_start = ~start
    negative_stop = ~stop
    negative_place = ~place
    print(negative_place)
    # step2.2: define start stop limits
    if start < 0 or stop < 0 or place < 0:
        pass
    else:
        pass


print(copy([1, 2, 3, 4, 5], 0, 2, -2))
