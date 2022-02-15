# Roman numerals converter
# (both ways)
#
# Author:   Rudolf Klusal 2022

# IMPORTS #

# CLASSES #
class Config:
    """ Just values and config """

    # list of valid letters
    valid_letters = ['m', 'c', 'd', 'l', 'x', 'v', 'i']

    # Letter values for conversion
    letter_values = {
        'm':1000,
        'c':100,
        'x':10,
        'i':1,
        'd':500,
        'l':50,
        'v':5,
    }


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

        # Method:
        #
        # Subsequently try to subtract the largest possible value from
        # the number. If possible, do it and save the letter used.
        # If the remainin value after subtraction is not less than
        # 100 from 1000 or 10 from 100 and so on, it must use subtract
        # form of roman numeral, for example 900 is not writen as DCCCC, but CM.
        # 800 is writen as DCCC. So the limit is 3 on the right side and 1
        # on the left side around the main roman numeral.



# RUNTIME #
def main():
    """ Main function """
    input_number = str(input("Enter the input either in decimal (integer) \nor in Roman (case doesn't matter): "))

    number = Number(input_number)

    if number.is_integer:
        print(f"Converted integer {number.number} to roman form is .")
            

if __name__ == "__main__":
    main()