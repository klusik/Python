"""
    Zadání 1:

    Vyrobte program, který přečte všechny výrobky ze souboru 'vyrobky.txt'
    a zobrazí všechny výrobky a jejich ceny ve formátu např.:

        mléko: 22 Kč
"""

# 1. krok, načteme všechno ze souboru
with open('vyrobky.txt', 'r', encoding='utf-8') as f_vyrobky:
    zbozi = f_vyrobky.read()

# 2. krok, ve stringu 'zbozi' máme úplně všechny výrobky, musíme je
# trošku rozsekat. Využijeme toho, že v souboru vyrobky.txt jsou
# jednotlivé výrobky odděleny "enterem," prostě novým řádkem.
# To už víme, že je symbol '\n', podle něho tedy rozdělíme zboží
# na jednotlivé řádky.

zbozi_radky = zbozi.split('\n')

# 3. krok, forem projdeme jednotlivé řádky a ve vstupním souboru vidíme,
# že je vždy výrobek a jeho cena oddělena mezerou, rozdělíme tedy řádek
# podle mezery
for radek in zbozi_radky:
    # Vlastní rozdělení podle mezery
    vyrobek = radek.split()[0]
    cena = radek.split()[1]

    # Vypíšeme výstup
    print(f"{vyrobek}: {cena} Kč")

