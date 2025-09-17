"""
    As Michal did that, so do I

    # In this kata, you will do addition and subtraction on a given string. The return value must be also a string.
    # Note: the input will not be empty.
    # Examples
    # "1plus2plus3plus4"  --> "10"
    # "1plus2plus3minus4" -->  "2"

    Author: klusik@klusik.cz
"""

# RUNTIME #
def parse_input(input_string):
    """Returns a number, reads a string"""
    if len(input_string) == 0:
        return False

    def is_digit(char):
        return str(char).isnumeric()

    def is_sign_char(char):
        return str(char).lower() in ('p', 'm')

    def process_number(digits_list, sum_list):
        if digits_list:
            sum_list.append(int("".join(digits_list)))
            digits_list.clear()

    plus = False
    minus = False
    current_number_digits = []
    running_sum = []

    for character in input_string:
        if not (plus or minus):
            # Not in a sign state
            if is_digit(character):
                current_number_digits.append(character)
                plus = False
                minus = False
            elif is_sign_char(character):
                # Identify if it's a plus or minus
                if str(character).lower() == 'p':
                    plus = True
                    minus = False
                elif str(character).lower() == 'm':
                    minus = True
                    plus = False
                # Process existing number before switching sign state
                process_number(current_number_digits, running_sum)
            # else ignore other characters
        else:
            # Handle cases where sign has been indicated
            # (Add your logic here if needed, currently not handled in original code)
            pass

    # Process any remaining number at the end
    process_number(current_number_digits, running_sum)

    # Assuming the function should return sum or final number
    return sum(running_sum) if running_sum else False

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