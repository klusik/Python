minimum = 0
for order in range(10):
    number = int(input("Enter number: "))
    
    if number < minimum:
        minimum = number
print(f"Smallest number is {minimum}.")