"""
    Největší ze všech

    Prográmek se bude postupně ptát uživatele na různá celá čísla včetně nuly.
    V momentě, co uživatel napíše 'konec', program se přestane ptát
    na další čísla a vypíše 3 nejvyšší čísla ze zadaných.

    Pokud uživatel zadá žádné, jedno až do tří čísel, tak to buď nevypíše nic (není co),
    anebo všechna tři čísla. Pokud zadá víc než 3 čísla, vypíše to pouze nejvyšší tři čísla.
"""


# CLASSES #
class NumberList:
    def __init__(self):
        # Prepare a list for entered numbers
        self.number_list: list = []

        # Fill up the list
        self.user_input()

    def __str__(self):
        return self.write_numbers()

    def write_numbers(self,
                      limit: int = 0,
                      ) -> str:
        """ Write numbers in the list on the console
        :rtype: None
        :param limit: (Optional) If specified, only 'limit' number of biggest numbers are displayed """
        if not limit:
            return " ".join(map(str, self.number_list))
        else:
            return " ".join(map(str, sorted(self.number_list, reverse=True)[:3]))

    def user_input(self) -> list:
        """ Deals with user input
        :rtype: list
        """
        usr_input: str = ""

        while True:
            if len(self.number_list):
                print(f"Čísla, která jsou zatím v seznamu: {self.write_numbers()}")

            try:
                usr_input = input("Zadej číslo do seznamu: ")
                if usr_input == "konec":
                    return self.number_list

                self.number_list.append(int(usr_input))

            except ValueError:
                print("Zadej celé číslo!")
                continue


# RUNTIME #


def main():
    """ Main routine """
    numbers = NumberList()

    print(f"All numbers in list: {numbers}")
    print(f"Three biggest numbers in the list: {numbers.write_numbers(3)}")


if __name__ == "__main__":
    main()
