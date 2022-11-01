"""
    Zjistěte chybu v tutom prográmku

    Zadání:

"""


def funkce(l_values=None):
    l_values = []
    l_values.append("vnitrek funkce")
    print(f"Uvnitř funkce, seznam vypadá takhle: \t{l_values}")


list_of_words = ['ahoj', 'pocitac', 'pes']

funkce(list_of_words)

print(f"Mimo funkci, seznam vypadá takhle: \t\t{list_of_words}")
