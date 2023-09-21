"""
* CO DĚLAT NA NAŠICH SOUKROMÝCH PYTHON SETKÁNÍCH *

==========
Setkání 1.
==========

Program:
    -	Číselné proměnné (int, float) a řetězce
    -	Výpis proměnných
    -	Vstup od uživatele

Ukázková zadání:
    Z1.
    -	Požádej uživatele o vstup: Zadej sudé kladné číslo
    -	Program bude kontrolovat validitu vstupu,
        dokud uživatel nezadá kladné sudé číslo
    -	Program toto číslo bude dělit dvěma tak dlouho, dokud to půjde.
    -	Nakonec vypíše, kolikrát se mu to povedlo (proto je třeba sudé číslo, aby to bylo alespoň jednou).
    -	Pokud číslo bude složeno pouze z násobků dvojek,
        program vypíše hlášku: Zadali jste mocninu dvou, super!
"""


# CLASSES #
class Divider:
    def __init__(self):
        # Variables
        self.number = 0
        self.counter = 0

        self.pow_2 = False

        # Prompt user
        self.user_input()

        # Compute divisions
        self.make_divisions()

    def __str__(self):
        return (
            f"Počet dělení dvojkou: {self.counter}, "
            f"číslo je mocnina dvojky."
            if self.pow_2
            else f"Počet dělení dvojkou: {self.counter}, číslo není mocninou dvojky"
        )

    def user_input(self):
        while True:
            try:
                user_input = int(input("Zadej sudé kladné číslo: "))
            except ValueError:
                print("Je třeba zadat číslo.")
                continue

            if user_input > 0 and not user_input % 2:
                self.number = user_input
                return self.number
            else:
                print("Číslo musí být kladné a sudé.")
                continue

    def make_divisions(self):
        while True:
            if not self.number % 2:
                self.counter += 1
                self.number /= 2
            elif self.number == 1:
                self.pow_2 = True
                return self.counter
            else:
                return self.counter


# RUNTIME #
if __name__ == "__main__":
    divider = Divider()

    print(divider)
