# Třídění bubblesort
# Ano, vím, že na to určitě bude knihovna a rychlejší, 
# ale chceme se naučit základy algoritmizace :-D

# config

maxHorniHranice = 1000      # maximální velikost
minSpodniHranice = -1000    # minimální velikost
maxPocetCisel = 10000       # maximální počet čísel

# 1. krok, vytvoříme "pole" (prostě list) náhodných čísel v nějakém rozsahu

import random
random.seed()

# Zadání počtu čísel, která vygenerovat. Od tří do nejvyšší hodnoty výše.
while True:
    mnozstviCisel = int(input(f"Zadej mnozstvi cisel, ktera generovat (3 -- {maxPocetCisel}): "))
    if mnozstviCisel < 3: continue
    if mnozstviCisel > maxPocetCisel: continue
    break

# Zadání spodní hranice, od které se budou generovat čísla
while True:
    spodniHranice = int(input("Zadej spodni hranici velikosti (-1000 -- 1000): "))
    if spodniHranice < -1000: continue
    if spodniHranice > 1000: continue
    break

# Zadání horní hranice, tj. nejvyššího čísla, které se bude generovat.
while True:
    horniHranice = int(input(f"Zadej horni hranici velikosti ({spodniHranice} -- 1000): "))
    if horniHranice < spodniHranice: continue
    if horniHranice > 1000: continue
    break

# Shrnutí toho, co je zadáno a co se bude dít
print(f"Generuji seznam {mnozstviCisel} cisel, "\
    f"kde nejmensi je {spodniHranice} a nejvyssi {horniHranice}.")

# Vytvoření prázdného seznamu
seznamCisel = []

# Plnění seznamu náhodnými čísly
for _ in range(0, mnozstviCisel):

    # Je potřeba zjistit, jaké rozsahy máme -- pokud je spodní a 
    # dolní číslo stejné, je zbytečné volat náhodné volání
    # a prostě seznam zaplníme oním společným číslem

    if horniHranice == spodniHranice:
        seznamCisel.append(int(horniHranice))
    
    # Tady budu plnit náhodnými čísly
    else:
        seznamCisel.append(int(random.randrange(spodniHranice, horniHranice)))

# Výpis nesetříděného seznamu
print("Nas seznam nahodnych cisel: ")
print(seznamCisel)

print("Jdeme tridit, chvilku strpeni...")

# Vlastni trideni bubblesortem
# Princip bubblesortu je jednoduchy, prochazi se neustale pole odzacatku, 
# konec prochazeni nastane v momente, co je pole setridene.
# kdyz se najdou dve sousedni cisla ve spatnem poradi, tedy ze
# prvni cislo bude vetsi nez druhe, prohodi se jejich poradi.
# Tuta metoda je hrozne pomala, ale jednoducha naprogramovat. 
# Priste se podivame na Insertsort a Selectsort, ktere 
# tyhle neduhy trosku odstranuji.

# Počítadlo průchodů
pocetPruchodu = 0

# Megasmyčka -- hlavní řídící blok
while True:
    
    # Každý průchod je zaznamenán
    pocetPruchodu = pocetPruchodu + 1

    # Počítadlo prohození
    pocetProhozeni = 0


    # vlastní prohazování
    for index in range(0, mnozstviCisel-1):        
        if seznamCisel[index] > seznamCisel[index+1]:
            buffer = seznamCisel[index]
            seznamCisel[index] = seznamCisel[index+1]
            seznamCisel[index+1] = buffer
            pocetProhozeni = pocetProhozeni + 1

    # kontrola, jestli je co potřeba prohazovat, případně hotovo.
    if pocetProhozeni == 0:
        break

    

# Výpisy
print("A zde mame hotove setridene pole: ")
print(seznamCisel)
print(f"Na setrideni jsme museli seznam projit nejmene {pocetPruchodu}krat.")