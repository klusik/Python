numbers = [12, 6, 3, 5, 1, 0, 21, 7, 18, -8, -1]

def findMin(indexFrom):
    Min = numbers[indexFrom]
    indexMin = indexFrom

    for index in range(indexFrom+1, len(numbers)):
        if numbers[index] < Min:
            Min = numbers[index]
            indexMin = index

    return indexMin

def swap(index1, index2):
    buffer = numbers[index1]
    numbers[index1] = numbers[index2]
    numbers[index2] = buffer

for index in range(0, len(numbers)-1):
    swap(index, findMin(index))
    
print(numbers)

