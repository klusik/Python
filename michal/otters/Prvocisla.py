#Program má hledat prvočísla do zadného čísla nejvýše

import math

while True:
    maxPrime = int(input("Zadej nejvyssi cislo, do ktereho hledat: "))
    if (maxPrime < 2):
        print("Zadej cislo od 2 vyssi, prosim.")
    else:
        break;

# zacneme hledat

primesList = []

def isPrime(testedNumber):
    for divider in range(2, int(math.sqrt(testedNumber)+1)):
        if testedNumber % divider == 0:
            return False # není prvočíslo
    return True #je prvocislo

for testedNumber in range(2, int(maxPrime)+1):
    if isPrime(testedNumber):
        primesList.append(testedNumber)

# výpis uložených čísel
print(f"Celkove nalezeno {len(primesList)} prvocisel.")

if len(primesList) > 0:
    print("Nalezena prvocisla: ")
    for i in range(1, len(primesList)+1):
        print(f"{i}.  {primesList[i-1]}")


