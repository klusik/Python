# Pokusim se vyrobit soubor s nejakymi daty a pak ho otevrit a precist

import random

random.seed()

# Generovani nahodnych dat

while True:
    kolikCisel = int(input("Kolik cisel do souboru generovat? => "))
    if kolikCisel >= 1: break

seznam = []

for _ in range(0, kolikCisel):
    seznam.append(random.randrange(1, 1000))

# Zapis dat do souboru
fSoubor = open("data.kls", "w")

print(len(seznam))

for cislo in seznam:
    fSoubor.writelines(str(cislo)+"\n")

fSoubor.close()

# Vycistime to
seznam = []

# Otevreme soubor pro cteni a zkusime to naplnit
fSoubor = open("data.kls", "r")

while True:
    cislo = fSoubor.readline()
    cislo = cislo[:-1]

    if cislo == '': break
    seznam.append(cislo)

fSoubor.close()

print("Nesetrideny seznam: ")
for cislo in seznam:
    print(str(cislo))