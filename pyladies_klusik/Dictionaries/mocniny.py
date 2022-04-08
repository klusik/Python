def mocniny(n):
    vysledek = {}
    for cislo in range(n + 1):
        vysledek[cislo] = (cislo * cislo)
    return vysledek


print(mocniny(4))