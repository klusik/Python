numbers = [12, 6, 3, 5, 1, 0, 21, 7, 18]

while True:
    counter = 0
    for i in range(0, len(numbers)-1):
        if numbers[i]<numbers[i+1]:
            buffer = numbers[i]
            numbers[i] = numbers[i+1]
            numbers[i+1] = buffer
            counter = counter + 1
    if counter == 0:
        break
print(numbers)


    
    


