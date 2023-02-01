"""
    Jednoduchý progámek na součet dvou čísel.

    Napiš jednoduchý prográmek, který se uživatele zeptá na dvě celá čísla.
    Prográmek vypíše součet tutěch čísel.

    Author:     Rudolf Klusal
"""


# RUNTIME #
def user_input() -> (int, int):
    """ Deal with user input 
    :rtype: (int, int)
    """

    # Values for storing two user inputs
    usr_val_1: int = 0
    usr_val_2: int = 0

    while True:
        # User input of two numbers
        try:
            # First number from user
            usr_val_1 = int(input("Zadej první číslo: "))
        except ValueError:
            print("Musí být celé číslo!")
            continue
        except KeyboardInterrupt:
            print("Ukončuji zadávání!")
            exit(0)

        # First number successfully stored
        break

    while True:
        try:
            # Second number from user
            usr_val_2 = int(input("Zadej druhé číslo: "))
        except ValueError:
            print("I druhé číslo musí být celé číslo!")
            continue
        except KeyboardInterrupt:
            print("Ukončuji zadávání po druhém čísle!")
            exit(0)

        # Both numbers successfully added
        break

    return usr_val_1, usr_val_2


def add_numbers(val_1: int, val_2: int) -> int:
    """ Adds two numbers together
    :rtype: int
    :param val_1: First number from user
    :param val_2: Second number from user
    :return: integer, adds val_1 and val_2
    """
    return val_1 + val_2


def main():
    """ Main routine """

    # Values from user
    val_1, val_2 = user_input()

    # Number addition
    print(f"Součet čísel {val_1} a {val_2} je {add_numbers(val_1, val_2)}.")


if __name__ == "__main__":
    main()
