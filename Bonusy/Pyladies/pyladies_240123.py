# Chci vypsat čislo 5
#
# Tady bych chtěl pomocí funkce print() vypsat číslici 5,
# nechci však aby to psalo nějaké chyby.
# print(5)

# Chci vypsat součet čísel 5 + 7 (nápověda: 12)
# print(5 + 7)

# Co se stane, když budu chgtítg sečíst řetězec: "ahoj" a k tomu 5?
# print("ahoj", 5)

# Chci řešit prioritu operátorů
# print((1 + 2) * 6)

# Výstup: Čtverec se stranou 10 má plochu 100.
# print("Čtverec se stranou", 10, "má plochu", 10**2)

# PROMĚNNÁ
# strana = 5e06 # znamená 5 x 10 na šestou
# print("Čtverec se stranou", strana, "má plochu", strana ** 2)

# neco = input("Zadej stranu čtverce, celé číslo: ")
# neco_cislo = int(neco)

# print("Čtverec se stranou", neco, "má obsah", neco_cislo ** 2)
# print("ahoj" * neco_cislo)

# Uživatel zadá dvě celá čísla (dva inputy za sebou)
# Program spočítá plochu trojúhelníka, který je definovaný
# jednou stranou a výškou (to jsou ty dvě hodnoty)
# Plocha trojúhelníka: strana * výška_na_stranu / 2

# Zeptám se uživatele na dvě hodnoty
strana_trojuhelniku = int(input("Zadej stranu trojuhelniku: "))
vyska_strany = int(input("Zadej výšku na tuto stranu: "))

# Kontroly výpočtu:
if strana_trojuhelniku > 0 and vyska_strany > 0:
    if strana_trojuhelniku <= 100 and vyska_strany <= 100:
        # Spočtu plochu
        plocha = strana_trojuhelniku * vyska_strany / 2
        
        print("Trojúhelník se stranou", # začátek výpisu
              strana_trojuhelniku, # narvu tam první stranu
              "a výškou",
              vyska_strany, # do výpočtu narvu výšku
              "má plochu",
              plocha) # Vypíšu výsledek
    else:
        print("Hodnoty jsou moc velké.")
else:
    print("Strana i výška musí být kladné číslo.")
        



# Vypíšu plochu




# Co nechceme:
# Nulové strany
# záporné strany
# stranu a výšku chceme ne větší než 100

# hodnota = 5

"""
if hodnota < 10:
    print("Hodnota je menší než 10.")
    print("Moc hezky jsi to zadal.")
else:
    print("Zkus zadat menší číslo.")
"""    
# porkacovat tady
