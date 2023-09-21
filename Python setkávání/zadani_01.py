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


# RUNTIME #
def main():
    # Zadání od uživatele
    user_input = 0
    while True:
        try:
            user_input = int(input("Zadej kladné sudé číslo: "))
        except ValueError:
            print("Zadaný vstup musí být číslo.")

        if user_input > 0 and not (user_input % 2):
            break
        else:
            print("Číslo musí být celé a kladné.")

    # Dělení dvěma
    counter = 0
    while True:
        if not (user_input % 2):
            user_input /= 2
            counter += 1
        else:
            break

    print(f"Celkem obsahujících dvojek: {counter}")

    if user_input == 1:
        print("Číslo je čistě složené z dvojek, super!")


if __name__ == "__main__":
    main()
