# Given an array of integers, return a new array with each value doubled.
# For example:
# [1, 2, 3] --> [2, 4, 6]
# For the beginner, try to use the map method - it comes in very handy quite a lot so is a good one to know.
# moje poznamka, python sam o sobe nema nic, co by umoznilo rychle vynasobit list konstantou
def maps(a):
    a2 = [(i * 2) for i in a]
    return a2


print(maps([1, 2, 3]))


# ted se pokusim o pristup pomoci funkce map()
def mapa(a):
    f = lambda x: x * 2

    return [
        f(x)
        for x in a
    ]
    # return list(map(f, a))


print(mapa([1, 2, 3]))
