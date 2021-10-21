# Compute sum from 1 to n of sin(1/n) for given "n"

import math

n=0

while n<=1:
    n=int(input("Zadej 'n,' (n >= 2):  "))

sum = 0
for i in range(1, n+1):
    sum = sum + math.sin(1/i)
    
    if i <= 100 or i%1000 == 0:
        print(f"Mezisoucet {i}. krok: {sum}")

