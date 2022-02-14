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
def do_computation(input_string):
    """ Returns a number, reads a string """

    # This function tries to read all numbers and 'plus' or 'minus'
    # substrings, ignores all other stuff.
    # It should be okay for 'pl us' and so on.

def main():
    """ Main function """

    input_string = str(input("Enter the string: "))

    try:
        print(f"{input_string} = {do_computation(input_string)}.")
    except Exception as exception:
        print("Error occured :-(")
        raise exception

if __name__ == "__main__":
    main()