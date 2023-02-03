"""
    Jednoduchý progámek na součet dvou čísel.

    Napiš jednoduchý prográmek, který se uživatele zeptá na dvě celá čísla.
    Prográmek vypíše součet tutěch čísel.

    Tato verze bude objektová.

    Author:     Rudolf Klusal
"""


# CLASES #
class Config:
    """ Config class """

    # Number of numbers to add
    NUMBERS_COUNT = 2


class Number:
    """ Class represents numbers """

    def __init__(self,
                 number=None,  # Number to store
                 count=None,  # Count of number
                 ):

        # If number specified, just use that number. If not, ask user.
        if number:
            self.number = number
        else:
            self.input(count=count)

    def __str__(self):
        """ We can print 'object' now."""
        return str(self.number)

    def __radd__(self, other: 'Number') -> 'Number':
        """ Method uses __add__ method for an object for sum(). """
        return Number(self + other)

    def __add__(self, number_2) -> 'Number':
        """ If I want to simply adding objects as numbers, I must specify how to handle the situation """
        return Number(number=self.number + number_2)

    def input(self,
              count=None,
              ) -> int:
        """ Inputs number from user
        :rtype: int
        :param count: (optional) If specified, the input prompt changes accordinlgy
        :return: integer of the number.
        """
        while True:
            # User input loop
            try:
                if count:
                    # If specified, ask user with count
                    input_string = f"Zadej {count}. číslo: "
                else:
                    # If not, just default prompt
                    input_string = "Zadej číslo: "

                # Save the input, handle the exceptions
                usr_input: int = int(input(input_string))

                self.number = usr_input
                return usr_input

            except ValueError:
                print("This is not allowed, use only whole numbers.")
                continue

            except KeyboardInterrupt:
                print("Ending program.")
                exit(0)


# RUNTIME #
def input_numbers() -> list[Number]:
    """ Handles the input from user
    :rtype: list[Number]
    :return: Returns a list of objects from class Number
    """

    # Create a list for user numbers
    input_list = list()

    # Ask for numbers one by one
    for count in range(Config.NUMBERS_COUNT):
        number = Number(count=count + 1)
        input_list.append(number)

    return input_list


def main():
    """ Main routine """
    input_list: list[Number] = input_numbers()

    print(f"All numbers summed: {sum(input_list)}.")


if __name__ == "__main__":
    main()
