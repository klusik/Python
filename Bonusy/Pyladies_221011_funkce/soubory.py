""" soubory """


soubor = open('soubory.py', 'r')

print(soubor.read())
soubor.close()

try:
    with open('soubory.py', 'r') as soubor:
        print(soubor.read())
except FileNotFoundError:
    print("PSantne nazev souboru")