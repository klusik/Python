# Hledání vždy nových prvočísel v rozkladu od určitého bodu

# imports
import math

# config
countOfNumbers = 20



# Zadana funkce
def thatFunction(number):
    return (2*number + 1)

def isPrime(number):
    
    if number < 2: return(False)

    for i in range(2, int(math.sqrt(number))+1):
        if number % i == 0:
            return(False)

    return(True)

def factorization(number):
    pass

# Vygenerování čísel
numbersList = []
numberCount = 0
numbersList.append(1)

while True:
    newNumber = thatFunction(numbersList[len(numbersList)-1])
    numbersList.append(newNumber)
    numberCount = numberCount + 1
    if numberCount >= countOfNumbers: break


print(numbersList)

# Rozklad všech čísel na prvočísla
for index in numbersList:
    print(f"Number {index} "+str(isPrime(index)))
