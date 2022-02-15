# Roman numerals converter
# (both ways)
#
# Author:   Rudolf Klusal 2022

# IMPORTS #

# CLASSES #
class Config:
    valid_letters = ['m', 'c', 'd', 'l', 'x', 'v', 'i']
class Number:
    """ Number class """
    def __init__(self, input_number):
        # Determine if it's in Roman or decimal form
        if str(input_number).isnumeric():
            # It's in decimal, checking if 
            # just an integer
            if (float(input_number) - int(input_number)) == 0:
                # Valid integer
                self.number = int(input_number)
                self.is_integer = True
                self.is_roman = False
                print("Number recognized as an integer.")
            else:
                print("Not a valid integer.")
                exit()

        elif str(input_number).isalpha():
            # It's not a numeric
            # Check if consists only valid letters
            not_valid = False
            for index, character in enumerate(str(input_number).lower()):
                if character in Config.valid_letters:
                    continue # found
                else:
                    print(f"Not valid roman numeral, a letter {character} in position {index+1} is not valid.")
                    not_valid = True
            if not_valid:
                exit()

            # Valid roman numeral
            self.roman_number = str(input_number).lower()
            self.is_roman = True
            self.is_integer = False
            print("Number recognized as roman.")

        else:
            # Not integer nor roman
            print("Bad input, mixed decimals with romans.")
            exit()

    def convert_to_roman(self):
        """
        Converts self.number to roman
        :return: string
        """



# RUNTIME #
def main():
    """ Main function """
    input_number = str(input("Enter the input either in decimal (integer) \nor in Roman (case doesn't matter): "))

    number = Number(input_number)

    if number.is_integer:
        print(f"Converted integer {number.number} to roman form is .")
            

if __name__ == "__main__":
    main()