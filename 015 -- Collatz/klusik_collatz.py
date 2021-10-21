# Collatz 
#
# If a number is odd, do 3x + 1
# If a number is even, do x/2
#
# Do as long as the result is back to 1
# Track all progress
# Enter the biggest number to test

#imports
import math


def userInput():
    while True:
        number = int(input("Input a number n>1: "))
        if number <= 1: continue
        break

    return number

def isOdd(number):
    if (number % 2) == 0: 
        return True
    else:
        return False

def collatz(maxNumber):

    # create an empty list
    results = []
    print(f"maxNumber = {maxNumber}")

    # Look through all the numbers
    for number in range(1, maxNumber+1):
        
        workingNumber = number      # Actual number
        progress = [number]         # Tracking a progress
        #print(f"Doing number {workingNumber}")
        

        while True:

            if isOdd(workingNumber):
                workingNumber = int(workingNumber / 2)
            else:
                workingNumber = (3 * workingNumber) + 1

            progress.append(workingNumber)

            if workingNumber == 1:
                break

            

        results.append(progress)
        #print(f"Written {len(progress)} items for number {number}.")
        progress = []

    return results


def main():
    
    # User input
    maxNumber = userInput()

    # do magic
    results = collatz(maxNumber)

    # Output
    fileLink = open("output.txt", "w")

    for i in range(0, len(results)):
        fileLink.write(f"{i+1} (length = {len(results[i])}): {results[i]}\n")

    fileLink.close()

if __name__ == "__main__": main()