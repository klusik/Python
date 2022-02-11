import random
import math

soucet = 0
x = 10**11
for _ in range(0,x):
    a = random.uniform(0,1)
    b = random.uniform(0,1)

   # print(math.floor(a/b))

    if math.floor(a/b) % 2 == 0:
        soucet += 1

print(soucet/x)

