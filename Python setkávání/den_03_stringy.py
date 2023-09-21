"""
    Opakování stringů
"""

"""
    QUEST 1:
    
    Vytvoř prográmek, který přečte od uživatele text
    (velká/malá, číslice, znaky, všechno) a spočte
    kolikrát se nachází v zadaném textu písmeno 'a' či 'A'. 
    
    Například ve vstupu: "Ale dneska je taky pěkně."
    
    Budou 3 áčka.
"""

# Uživatelský vstup
vstup = input("Zadej krátkou větu: ")

# Výpočet 1. způsobem, tedy sečtu všechny počty 'a' a 'A' a sečtu
# je dohromady

pocet_malych = vstup.count('a')
pocet_velkych = vstup.count('A')

print(f"Počet áček je dohromady {pocet_velkych + pocet_malych}.")

# Výpočet 2. způsobem (udělat to najednou)

pocet_acek = vstup.lower().count('a')

print(f"Počet áček je dohromady {pocet_acek}.")

"""
    QUEST 2:
    
    Uprav QUEST 1 tak, že program spočte všechny samohlásky
    ze zadaného textu (áčka počítat může pořád, tohle bude
    jen rozšíření).
    
    Mezi samohlásky použij list:
    ['a', 'á', 'e', 'ě', 'é', 'i', 
    'í' 'o', 'ó', 'u', 'ú', 'ů', 'y', 'ý']
    
    Výše zmíněný text tedy vrátí "9 samohlásek." (počítám
    od oka, snad počítám správně :-D)
"""

# Seznam samohlásek
samohlasky = [
    'a', 'á', 'e',
    'ě', 'é',
    'i', 'í',
    'o', 'ó',
    'u', 'ú', 'ů',
    'y', 'ý'
]

# 1. metoda

# Vytvořím počítadlo samohlásek a vynuluju ho
pocet_samohlasek = 0

# Projdu všechny samohlásky a postupně posčítávám, kolik jich text
# obsahuje a připočítávám do počítadla.
for samohlaska in samohlasky:
    pocet_samohlasek = pocet_samohlasek + vstup.lower().count(samohlaska)

# Vypíšu výsledek.
print(f"Celkem text obsahuje {pocet_samohlasek} samohlásek.")

# 2. metoda
# Použiju funkci sum(), která sečte prvky pole,
#
print(f"Celkem text obsahuje {sum(vstup.count(znak) for znak in samohlasky)} samohlásek.")

