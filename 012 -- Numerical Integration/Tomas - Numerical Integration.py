
a = 0
b = 3
result = 0

def x2(x):
    return x*x

division = int(input("Enter the division: "))

delta = abs(a - b)/division
x = delta

for n in range(1, division+1):
    result = result + delta*x2(x)
    x = x+delta
    print(x)
    
print(result)
