""" Výběr znaků """
def vyber_znaku():
    znak_hrac = 'N'

    while znak_hrac not in 'ox':
        znak_hrac = input("Zadej")

    return znak_hrac

# vyber_znaku()
pole = []

for i in range(5):
    pole.append(["x"] * 5)

print(pole)