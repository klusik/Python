import math

selectNumber = 0
b = 0

selectNumber = int(input(f'Enter a number:'))
c = math.sqrt(selectNumber)

for i in range(2, math.floor(c)):
    
    a = selectNumber%i

    if a == 0:
        b = 1
        print(f'{selectNumber} is not a prime.')
        break


if b == 0:
    print(f'{selectNumber} is a prime.')

