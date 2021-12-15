# write algorithm that takes an array and moves all of the zeroes to the end
# preserving the order of the other elements

# imports
import random

def reconfigurator(policko):
    nullcounter = 0
    # removing zeroes from the position and counting volume of zeroes
    for i in policko:
        if i == 0:
            policko.remove(0)
            nullcounter += 1
    
    # adding zeroes to the end of the list
    for i in range(nullcounter):
        policko.append(0)

    return policko, nullcounter

# generate random list of integers
start = 0
stop = 3
count = 10
lRan = [random.randint(start,stop) for i in range(count)]
print(lRan)
print(reconfigurator([lRan]))