A = [
    [1,3,5],
    [2,6,3],
    [8,5,4]
]
b = [82,101,123]
n = len(b)

# První fáze
for i in range(n-1):
    m = abs(A[i][i])
    l = i
    for j in range(i+1,n):
        if abs(A[j][i]) > m:
            l = j
    if l != i:
        A[i], A[l] = A[l], A[i]
        b[i], b[l] = b[l], b[i]
    for j in range(i+1,n):
        c = A[j][i] / A[i][i]
        for k in range(i,n):
            A[j][k] -= c * A[i][k]
        b[j] -= c * b[i]

for row in A:
    print(*row)
print(b)

# Druhá fáze
for i in range(n-1,-1,-1):
    b[i] /= A[i][i]
    A[i][i] = 1
    for j in range(i):
        c = A[j][i]
        A[j][i] = 0
        b[j] -= c * b[i]

for row in A:
    print(*row)
print(b)