p = 1
for n in range(40):
    p *= (365-n)/365
    print(n+1, 1-p)