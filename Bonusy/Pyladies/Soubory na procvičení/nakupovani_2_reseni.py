"""
    Zadání 2:

    Vyrobte prográmek, který spočte cenu nákupu,
    pokud bych zakoupil všechny výrobky a od každého jeden kus (posčítejte cenu)
"""

# 1. krok: Načteme zase všechny výrobky a ceny (použijeme předchozí program)
# Vysvětlení kódu v 1. příkladu nakupovani_1_reseni.py

with open('vyrobky.txt', 'r', encoding='utf-8') as f_vyrobky:
    zbozi = f_vyrobky.read()

zbozi_radky = zbozi.split('\n')

# Nastavení našeho počitadla na cenu
celkova_cena = 0

for radek in zbozi_radky:
    cena = radek.split()[1]
    celkova_cena += float(cena) # Cena je string, je třeba ji přehodit na číslo, navíc desetinné v případě haléřů

# Vypíšeme celkoovou cenu
print(f"Celková cena je {celkova_cena} Kč.")


