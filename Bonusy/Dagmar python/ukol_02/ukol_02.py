"""
    Přečti větu zadanou z klávesnice a spočti počet slov.

    Prográmek se uživatele zeptá na nějakou větu, může obsahovat čárky,
    tečky, různé věci. Zpočátku tyhle znaky neřeš, prostě uživatel
    zadá třeba "toto je veta a kdo je vic" -- prográmek vrátí, že to má 7 slov.

    Postupně pak budeme přidávat další funkcionality
"""
# IMPORTS #
import re


# CLASSES #
class Sentence:
    """ Contains sentence to work with """

    def __init__(self,
                 usr_input: str):
        self.usr_input = usr_input
        self.string_output = usr_input

    def __str__(self):
        """ Printable version """
        word_count = self.word_count()

        # String output (formatted)
        output_string = f"Věta '{self.usr_input}' obsahuje {self.word_count()} "

        # Czech grammar depends on number of words
        if word_count == 1:
            output_string += "slovo."
        elif 2 <= word_count <= 4:
            output_string += "slova."
        elif word_count >= 5:
            output_string += "slov."

        # Finally return the whole string
        return output_string

    def clean_string(self) -> None:
        """ Clears string from 'non-letters'
        :rtype: None
        """
        # Remove everything not a-z, A-Z or 0-9 or space
        self.string_output = re.sub('[^ a-zA-Z0-9]+', '', self.string_output)

    def word_count(self) -> int:
        """ Returns word count
        :rtype: int
        """

        # First prepare a string (clean it)
        self.clean_string()

        return len(self.string_output.split())


# RUNTIME #
def clear_input():
    """ Deals with user's input """
    usr_string: str = ""

    try:
        usr_string = input("Zadejte nějakou větu: ")
    except KeyboardInterrupt:
        print("Ukončuji zadávání.")
        exit(0)

    # Check of string length
    if not len(usr_string):
        print("Zadán prázdný řetězec, takže 0 slov :-)")
        exit(0)

    # If not empty or user didn't stop inputing, return string from user.
    return usr_string


def main():
    """ Main routine """

    # Variables
    usr_string: str = ""  # String for user input

    # User input
    usr_string = clear_input()

    # Create an object for the setnence
    sentence = Sentence(usr_string)

    print(sentence)


if __name__ == "__main__":
    main()
