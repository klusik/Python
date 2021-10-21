numbers = [12, 6, 3, 5, 1, 0, 21, 7, 18]

def findLowestNumber(numbers):

    lowestNumberIndex = 0
    lowestNumber = numbers[0]

    for i in range(0, len(numbers)):
        if numbers[i] < lowestNumber:
            lowestNumber = numbers[i]
            lowestNumberIndex = i
    return [lowestNumber, lowestNumberIndex]

lowestNumber = findLowestNumber(numbers)

print(f'{lowestNumber[0]} is the lowest number')
print(f'Its position is {lowestNumber[1]}')

highestNumberIndex = 0
highestNumber = numbers[0]

for i in range(0, len(numbers)):
    if numbers[i] > highestNumber:
        highestNumber = numbers[i]
        highestNumberIndex = i

print(f'{highestNumber} is the highest number')
print(f'Its position is {highestNumberIndex+1}')      
    
    


