def pocet_znaku():
    with open('prvni.txt', mode='r', encoding='utf-8-sig') as prvni_soubor:
        obsah_souboru = prvni_soubor.read().strip().replace(" ", "")

    return len(obsah_souboru)


def pocet_radku():
    pocet = 0
    with open('prvni.txt', mode='r', encoding='utf-8-sig') as prvni_soubor:
        for i in prvni_soubor:
            pocet = pocet + 1
    return pocet


with open('vysledek.txt', mode='a', encoding='utf-8') as vysledek:
    vysledek.write(f'Počet znaků v souboru je: {pocet_znaku()}\n')
    vysledek.write(f'Počet řádků v souboru je: {pocet_radku()}\n')