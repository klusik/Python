"""
    Mapa a filtr
"""
def mapuj_mocninu(vstupni_hodnota):
    return vstupni_hodnota ** 2

def je_sude(vstupni_hodnota):
    return not bool(vstupni_hodnota % 2)

def main():
    vstupni_hodnoty = [x+1 for x in range(20)]
    print("Vstupní hodnoty:\n", vstupni_hodnoty)

    print("Mapa druhých mocnin:\n", list(map(mapuj_mocninu, vstupni_hodnoty)))

    print("Filtr jen sudých:\n", list(filter(je_sude, vstupni_hodnoty)))

    print("Filtr jen lichých:\n", list(filter(lambda sud: not je_sude(sud), vstupni_hodnoty)))



if __name__ == "__main__":
    main()