# Bisekce
#
# Nejprve pouze odmocnina za dvou, pozdeji obecna odmocnina z obecneho cisla


# zelená část

# zadávání hodnot

lowerLimit = 1
higherLimit = 2
deltaX = 0.000001
deltaY = 0.000001
n = 2
z = 2
defaultLimitSearch = [-10000, 10000]


def myFunction(x):
    result = 1

    for i in range(0, n):
        result = result * x

    result = result - z

    return result

def getLimits():
    if n%2 == 0:
        defaultLimitSearch[0] = 0

    for i in range(defaultLimitSearch[0], defaultLimitSearch[1]):
        if (myFunction(i) < 0 and myFunction(i+1) >= 0) or (myFunction(i) > 0 and myFunction(i+1) <= 0): 
            return [i, i+1]


while True:
    
    # ptaní se uživatele

    # lowerLimit = int(input("Zadej spodni limit vypoctu (kladne cislo): "))
    # higherLimit = int(input("Zadej vrchni limit vypoctu (kladne cislo): "))


    
    deltaY = float(input("Zadej presnost vypoctu (napr. 0.01): "))
    n = int(input("Kolikata odmocnina z cisla: "))
    z = float(input("Z jakeho cisla odmocnovat: "))

    limits = getLimits()

    lowerLimit = limits[0]
    higherLimit = limits[1]

    if (lowerLimit >= higherLimit):
        continue

    if (deltaY <= 0):
        continue

    if n <= 1:
        continue

    if z <= 0:
        continue


    if myFunction(lowerLimit) < 0:
        if myFunction(higherLimit) > 0:
            # v poradku
            break

    if myFunction(lowerLimit) > 0:
        if myFunction(higherLimit) < 0:
            # v poradku
            break

    if myFunction(lowerLimit) == 0:
        # trefil jsem se
        break

    if myFunction(higherLimit) == 0:
        # trefil jsem se
        break


    # pokud to neprojde alespon jednou podminkou, neco je spatne a musim se uzivatele ptat na nove hodnoty
    

# modrá část
iter = 0

while True:
    iter = iter + 1
    # pulka intervalu

    halfInterval = (higherLimit + lowerLimit) / 2
    print(f"{iter}. krok: sL: {lowerLimit}, hL: {higherLimit}, halfInterval: {halfInterval}")

    # Zjistim, jestli je funkcni hodnota v intervalu kladna ci zaporna

    if myFunction(halfInterval) > 0:
        # hybu hornim limitem
        higherLimit = halfInterval

    if myFunction(halfInterval) < 0:
        # huby spodnim limitem
        lowerLimit = halfInterval

    if myFunction(halfInterval) == 0:
        # trefa
        break

    # kontrola na presnost delta X
    if (higherLimit - lowerLimit) < deltaX:
        break

    # kontrola na presnost delta Y
    if (myFunction(higherLimit) - myFunction(lowerLimit)) < deltaY:
        break

print(f"Nalezli jsme cislo {(lowerLimit)}.")
