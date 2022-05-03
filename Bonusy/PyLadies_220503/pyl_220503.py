""" Výběr znaků """
def vyber_znaku():
    znak_hrac = 'N'

    while znak_hrac not in 'ox':
        znak_hrac = input("Zadej")

    return znak_hrac

vyber_znaku()