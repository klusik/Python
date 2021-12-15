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

    # Creating a list
    for index in range(digitsCount):
        listOfNumbers.append(random.randrange(minNumber, maxNumber+1))

    # Displaying an original list
    print("Original list: ")
    print(listOfNumbers)

    # Counting zeroes and removing them.
    zeroCount = 0
    for digitIndex, digit in enumerate(listOfNumbers):
        if digit == 0:
            zeroCount += 1


    # Displaying a number of zeroes
    if zeroCount == 0:
        print("List doesn't contain any zero.")
    else:
        print(f"List contains {zeroCount} zeros.")

    # Removing zeros
    for _ in range(zeroCount):
        listOfNumbers.remove(0)

    # Adding zeroes to the end
    if zeroCount > 0:
        for _ in range(zeroCount):
            listOfNumbers.append(0)

    # Displaying final list
    print("After zero moving: ")
    print(listOfNumbers)

if __name__ == "__main__":
    main()