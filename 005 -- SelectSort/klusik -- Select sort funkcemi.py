# Select sorth with 2 functions -- swap() and minimum()

numbers = [1, 3, -2, -3, -8, 2, 1, 4, 2, -3, 2, 4]

def swap(index1, index2):
    buf = numbers[index1]
    numbers[index1] = numbers[index2]
    numbers[index2] = buf

def minimum(fromIndex):
    minimal = numbers[fromIndex]
    minimalIndex = fromIndex

    for index in range(fromIndex, len(numbers)):
        if numbers[index] < minimal:
            minimal = numbers[index]
            minimalIndex = index

    return minimalIndex


if __name__ == "__main__":
    for index in range(0, len(numbers)):
        swap(index, minimum(index))

    print(numbers)