# Select sort
# by Klusik

import random
random.seed()



# Definice & deklarace funkce, která zjistí nejmenší prvek
def nejmensiCislo(hledatOd, seznam):
    
    # nastavime, ze prvni cislo je nejmensi
    nejmensi = seznam[hledatOd]

    # prohledám seznam čísel od počátku (nebudu řešit to, co už je setříděný)
    posledniVyskytIndex = hledatOd
    for index in range(hledatOd, len(seznam)):
        if nejmensi > seznam[index]:
            nejmensi = seznam[index]
            posledniVyskytIndex = index


    # Vrátím hodnotu a její pozici
    return [nejmensi, posledniVyskytIndex]



# Zadání hodnot
while True:
    pocetCisel = int(input("Zadej pocet cisel (3 -- 10000): "))
    if pocetCisel < 3: continue
    if pocetCisel > 10000: continue
    break


# Naplnění pole náhodnými prvky
seznamCisel = []
for _ in range(0, pocetCisel):
    seznamCisel.append(random.randrange(1,100))


print("Nesetridene pole: ")
print(seznamCisel)

# Vlastni trideni

setridenoOd = 0 # Jeste nic neni setrideno
while True:

    # Nejdrive najdeme nejmensi cislo a jeho polohu
    nejmensi = nejmensiCislo(setridenoOd, seznamCisel)

    # prohodíme nejmenší číslo z nalezené pozice s prvnim nesetridenym
    # a nastavime, ze odtud uz je setrideno
    
    # Prohazování
    buffer = seznamCisel[setridenoOd]
    seznamCisel[setridenoOd] = seznamCisel[nejmensi[1]]
    seznamCisel[nejmensi[1]] = buffer

    # Posuneme ukazovátko toho, co už je setříděno (nehrab mi do toho)
    setridenoOd = setridenoOd + 1

    # Když jsme na konci, jsme hotovi
    if setridenoOd == len(seznamCisel):
        break

print("Setridena cisla: ")
print(seznamCisel)