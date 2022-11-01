"""
    Seznamy (nebo-li listy)
    
    """
import random

# Definice & deklarace
tuto_je_list = [3, 4, 5, 6, "Dagmar", ["První podvnořenina", "druhá podvnořenina"]]

# Prázdný seznam (různé způsoby)
prazdny = []
prazdny_2 = list()

a = 10

# Výpis všech prvků ze seznamu tak jak jsou
# print(tuto_je_list)

for polozka in tuto_je_list:
    # print(polozka)
    pass # prázdná instrukce, aby blok funkce/cyklu/... nebyl prázdný

# print(tuto_je_list)

# Vypsání konkrétní položky
# V následujícím případu vlezu do 5. prvku hlavního seznamu, ten obsahuje 2 prvky,
# v tom vlezu do 1. prvku a ten obsahuje string
# a tam vlezu do 2. znaku (všechna pořadí od 0)
#print(tuto_je_list[5][1][2])

# Přidávání hodnot do seznamu (:-))

tuto_je_list.append("lahev")

# print(tuto_je_list)

seznam_cisel = []

for _ in range(21):
    seznam_cisel.append(random.randrange(1,20))
    
# Metoda na třídění seznamu

# reverse = True -- od největšího
# reverse = False (nebo neuvedeno) -- od nejnižšího
# seznam_cisel.sort(reverse=False)

print(seznam_cisel)

print(seznam_cisel[:5:-1])

#setrideny = sorted(seznam_cisel)

#print(setrideny)

#print(seznam_cisel)

# Mazání
# .pop()

print(seznam_cisel.pop())
print(seznam_cisel)

del(seznam_cisel[2])

print(seznam_cisel)

seznam_cisel.clear()
print(seznam_cisel)






