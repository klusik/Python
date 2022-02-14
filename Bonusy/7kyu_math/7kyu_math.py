"""
    As Michal did that, so do I

    # In this kata, you will do addition and subtraction on a given string. The return value must be also a string.
    # Note: the input will not be empty.
    # Examples
    # "1plus2plus3plus4"  --> "10"
    # "1plus2plus3minus4" -->  "2"

    Author:     klusik@klusik.cz
"""

# RUNTIME #
def parse_input(input_string):
    """ Returns a number, reads a string """

    # This function tries to read all numbers and 'plus' or 'minus'
    # substrings, ignores all other stuff.
    # It should be okay for 'pl us' and so on.

    # Empty input
    if len(input_string) == 0:
        return False

    # Not empty input
    plus = False            # Plus trigger
    minus = False           # Minus trigger
    number = list()         # List of detected numbers (build up numbers)
    running_sum = list()    # List of previously found numbers and operations

    for index, character in enumerate(input_string):
        if not (plus and minus):
            # Basic branch -- no sign of sign detected yet

            # Is a character character or a digit?
            if str(character).isnumeric():
                # It's a number
                number.append(character)

                # reset plus or minus
                plus = False
                minus = False

            if str(character).isalpha():
                # Begining of 'plus' or 'minus' (maybe)
                if str(character).lower() == 'p':
                    plus = True
                    minus = False

                if str(character).lower() == 'm':
                    minus = True
                    plus = False

                # Handling previous numbers
                if len(number) > 0:
                    # Not empty list of digits
                    running_sum.append(int("".join(number)))

                    # Place for a new number
                    number.clear()

            # Next character
            continue


        # In the case of plus or minus

def main():
    """ Main function """

    input_string = str(input("Enter the string: "))

    try:
        print(f"{input_string} = {parse_input(input_string)}.")
    except Exception as exception:
        print("Error occured :-(")
        raise exception

if __name__ == "__main__":
    main()