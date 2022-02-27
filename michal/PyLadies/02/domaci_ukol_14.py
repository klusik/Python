'''
A teď trochu kreativity. Napiš program, který po zadání správného hesla vypíše nějakou tajnou informaci.

Vhodné tajemství je třeba: Dnes koukáme na Harryho Pottera.
'''

heslo = "Putin"

volba = input("zkuste uhandnout heslo. bez napovedy... Vase volba: ")

if heslo == volba:
    print("Python ma vysokou energetickou narocnost")
else:
    print("Nepovedlo se, zkus to znovu")
