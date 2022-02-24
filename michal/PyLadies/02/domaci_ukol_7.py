'''
Napiš program, který postupně načte od uživatele dvě čísla a jednoznakový řetězec
– buď '+', '-', '*' nebo '/'. Program provede na číslech příslušnou operaci.

Příklad použití programu:

První číslo: 123
Druhé číslo: 456
Operace: +
123 + 456 = 579
'''

a = float(input("zadejte prvni cislo: "))
b = float(input("zadejte druhe cislo: "))
operand = input('zadejte operaci mezi cisly (+,-,*,/): ')

if operand == '+':
    print(f'Byla vybrana operace soucet. {a} {operand} {b} = ', a+b)
elif operand == "-":
    print(f'Byla vybrana operace rozdil. {a} {operand} {b} = ', a-b)
elif operand == "*":
    print(f'Byla vybrana operace soucin. {a} {operand} {b} = ', a*b)
elif operand == "/":
    print(f'Byla vybrana operace podil. {a} {operand} {b} = ', a/b)
else:
    print(f'Byla vybrana neznama operace. Konzultujte odbornika na linearni algerbu.')