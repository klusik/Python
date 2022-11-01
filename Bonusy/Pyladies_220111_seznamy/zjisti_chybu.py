"""
    Zjistěte chybu v tutom prográmku

    Zadání:

"""


def funkce(l_values=[]):
    for value in l_values:
        print(value, end="")


for value in range(5):
    print(f"Pro {value}: ", end="")
    funkce([value, value + 1, value + 2])
    print()

funkce()
