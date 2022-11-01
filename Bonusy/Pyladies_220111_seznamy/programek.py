"""
    Krátké zadání
    

    Vytvořte prográmek, který se bude opakovaně ptát uživatele
    na vstupní hodnotu, která bude celé číslo (int()).
    
    Všechny hodnoty bude ukládat do seznamu a po zadání čísla 256
    se dotazování ukončí.
    
    Program pak všechny hodnoty vypíše s tím, že je očísluje, např.
    
    1. 5
    2. 2
    3. 14
    4. -3
    5. 8
    
    """

# Počáteční nastavení, vytváření proměnných etc.
seznam_cisel = []

# Zadana hodnota musí něco obsahovat a musí existovat,
# jinak by while na 28 (+/-) řádce nemohl udělat porovnání
zadana_hodnota = 0

# Chci, aby cyklus běžel, dokud nezadám číslo 256
while True:
    # Zadání od uživatele
    zadana_hodnota = int(input("Zadej cislo: "))
    
    # Přidání do seznamu
    if zadana_hodnota != 256:
        seznam_cisel.append(zadana_hodnota)
    else:
        break
    
# Výpis pole
for poradi, polozka in enumerate(seznam_cisel):
    print(f"{poradi + 1}. {polozka}")
    
