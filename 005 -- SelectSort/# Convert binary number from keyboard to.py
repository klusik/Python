# Convert binary number from keyboard to decimal

def numberIsBinary(binaryNumber):
    result = int(binaryNumber)

    while True:

        if result == 1 or result == 0:
            return(True)

        if result%10 == 1 or result%10 == 0:
            result = int(result / 10)
            continue
        else:
            return(False) # it cannot be anything else than 1 or 0

def convertBinToDec(binaryNumber):
    
    listBinaryNumber = list(str(binaryNumber))
    decadicNumber = 0

    for i in range(0, len(listBinaryNumber)):
        position = len(listBinaryNumber) - i - 1
        if listBinaryNumber[i] == '1':
            decadicNumber = decadicNumber + pow(2, position)

    return decadicNumber 

while True:
    binaryNumber = int(input("Number in binary: "))
    if numberIsBinary(binaryNumber): break

print(convertBinToDec(binaryNumber))

