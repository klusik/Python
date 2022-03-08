'''
Dokážeš docílit toho, aby se každý z řetězců 'Plichta.', 'Počítač vyhrál.' a 'Vyhrála jsi!' objevil v programu jen jednou, aniž bys tyhle řetězce musela přiřazovat do proměnných?

Pokud ano, gratuluji! Nasdílej nám tvoje řešení.
'''
# automatizace tahu pocitace
from random import randrange
CML = randrange(2) # CML = Centralni Mozek Lidstva
if CML == 0:
    CML = "kámen"
elif CML == 1:
    CML = 'nůžky'
else:
    CML = 'papír'

hooman = input('kámen, nůžky, nebo papír? ')

print("tah pocitace: " + CML)
# Plichta
if hooman == CML:
    print("plichta")
# Vyhra
elif (hooman == "nůžky" and CML == "papír") or \
    (hooman == "kámen" and CML == "nůžky") or \
    (hooman == "papír" and CML == "kámen"):
    print("Vyhra")

# Prohra
else:
    print("Prohra")