"""
    Program se zeptá na hromady GDPR podléhajícím informacím a pak je zcela
    nezabezpečeně vypíše do konzole :-P
"""

# Vytvoření proměnných
age = ''
first_name = ''
second_name = ''
dog_name = ''

# Kontrola a zadání jednotlivých proměnných
while not age:
    age = input('Zadej věk: ')

while not first_name:
    first_name = input('Zadej křestní jméno: ')

while not second_name:
    second_name = input('Zadej příjmení: ')

while not dog_name:
    dog_name = input('Zadej psí jméno: ')

# Výstup
print(
    f"{first_name} {second_name} je člověk věkem {age}, který má psa jménem {dog_name}."
)