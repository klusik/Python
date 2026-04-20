# Legacy baseline copied from the original implementation for benchmarking.

import math


def userInput():
    while True:
        number = int(input("Input a number n>1: "))
        if number <= 1:
            continue
        break

    return number


def isOdd(number):
    if (number % 2) == 0:
        return True
    else:
        return False


def collatz(maxNumber):
    results = []
    print(f"maxNumber = {maxNumber}")

    for number in range(1, maxNumber + 1):
        workingNumber = number
        progress = [number]

        while True:
            if isOdd(workingNumber):
                workingNumber = int(workingNumber / 2)
            else:
                workingNumber = (3 * workingNumber) + 1

            progress.append(workingNumber)

            if workingNumber == 1:
                break

        results.append(progress)
        progress = []

    return results


def main():
    maxNumber = userInput()
    results = collatz(maxNumber)

    fileLink = open("output.txt", "w")

    for i in range(0, len(results)):
        fileLink.write(f"{i + 1} (length = {len(results[i])}): {results[i]}\n")

    fileLink.close()


if __name__ == "__main__":
    main()
