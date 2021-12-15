#
# Write an algorithm that takes an array
# and moves all of the zeros to the end,
# preserving the order of the other elements.
#

# IMPORTS
import random

# CONFIG
digitsCount = 10
maxNumber = 4
minNumber = 0

# PROGRAM
def main():
    listOfNumbers = list()

    for index in range(digitsCount):
        listOfNumbers.append(random.randrange(minNumber, maxNumber+1))

    print("Original list: ")
    print(listOfNumbers)

    zeroCount = 0
    for digit in listOfNumbers:
        if digit == 0:
            zeroCount += 1

    if zeroCount == 0:
        print("List doesn't contain any zero.")
    else:
        print(f"List contains {zeroCount} zeros.")
        
if __name__ == "__main__":
    main()