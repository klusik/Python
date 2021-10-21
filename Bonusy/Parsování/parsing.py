# Parsing test

#config
countOfNumbers = 100

# Generate list of numbers
import random
random.seed()

listOfRandomNumbers = []
for _ in range(0, countOfNumbers):
    listOfRandomNumbers.append(random.randrange(1, 10))

# print(listOfRandomNumbers)

# creating a histogram
histogramOfNumbers = []

def findNumberInList(numberToFind):
    for i in range(0, len(histogramOfNumbers)):
        if histogramOfNumbers[i][0] == numberToFind:
            return i
    return(-1)

for i in range(0, len(listOfRandomNumbers)):
    
    indexOfNumberInHistogram = findNumberInList(listOfRandomNumbers[i])
    
    # if not found, create new item in histogram

    if indexOfNumberInHistogram == -1:
        histogramOfNumbers.append([listOfRandomNumbers[i], 1])
    
    # if found, just add 1 to counter (secont argument)
    else:
        histogramOfNumbers[indexOfNumberInHistogram][1] = histogramOfNumbers[indexOfNumberInHistogram][1] + 1

    pass

histogramOfNumbers.sort()

print(histogramOfNumbers)
fFile = open("text.html", "w")
# header
fFile.writelines("<!DOCTYPE html>")
fFile.writelines("<html><head><meta charset='utf-8' /><title>Generovana cisla</title><style type='text/css'>.number</style></head><body>")

# list of numbers (just like that)
fFile.writelines("<h1> List of all numbers </h1>")
for i in range(0, len(listOfRandomNumbers)):
    fFile.writelines(f"<span id='num_{i}' class='number'>{listOfRandomNumbers[i]}</span>")

fFile.writelines("<h1> Histogram of counts </h1>")
for i in range(0, len(histogramOfNumbers)):
    fFile.writelines(f"<span class='number'>{histogramOfNumbers[i][0]} : {histogramOfNumbers[i][1]}x</span>")


# footer
fFile.writelines("</body></html>")
fFile.close()

