"""
    Based on Pyladies task:

    Task: Napište program, který vyřeší následující úlohu:
    Na dlouhé chodbě je n dveří, všechny jsou na začátku zavřené.
    Při prvním průchodu otočíme (tzn. zavřeme pokud byly
    otevřené/otevřeme pokud byly zavřené) všechny dveře,
    při druhém průchodu otočíme pouze každé druhé dveře,
    při třetím průchodu každé třetí atd. až do 100 průchodů,
    kdy otočíme pouze poslední dveře. Které dveře zůstanou na konci otevřené?
    Vypište jejich pořadová čísla.
"""

def main():
    number_of_doors = int(input("Enter the number of doors: "))

    doors = [0] * number_of_doors

    # switching
    for switch in range(number_of_doors):
        actual = 0
        while actual < number_of_doors:
            doors[actual] = 1 if doors[actual] == 0 else 0
            actual += 1

    print(doors)


if __name__ == "__main__":
    main()