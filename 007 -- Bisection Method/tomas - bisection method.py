a = 1
b = 2
tolerance = 0.01
iteration = 0
n = 0
z = 0

def myFunction(x):
    result = 1

    for i in range(0,n):
        result = result*x
        
    result = result - z
        
    return result

while True:
    a = int(input("Enter the lower limit: "))
    b = int(input("Enter the higher limit: "))
    tolerance = float(input("Enter the tolerance: "))
    n = int(input("Enter the nth root: "))
    z = float(input("Enter the base: "))

    if a >= b:
        continue

    if tolerance <= 0:
        continue

    if myFunction(a) < 0 and myFunction(b) > 0:
        # all right
        break

    if myFunction(a) > 0 and myFunction(b) < 0:
        # all right
        break

while True:
    iteration = iteration + 1
    c = (b + a) / 2

    print(f"{iteration}.step LowerLimit: {a}, HigherLimit: {b}")

    if myFunction(c) > 0:
        b = c

    if myFunction(c) < 0:
        a = c
    
    if myFunction(b) - myFunction(a) > tolerance:
        continue
    
    else: break
    
print(f"The result is {a}.")
