a = 2

for a in range(1, 10):
    print(a.to_bytes(2, "big"), a)
    print(a.__add__(5))
    print(a.__bool__())