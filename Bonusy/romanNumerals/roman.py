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

    # Values for conversion
    conversion_table = [
        ('m', 1000),
        ('cm', 900),
        ('d', 500),
        ('cd', 400),
        ('c', 100),
        ('xc', 90),
        ('l', 50),
        ('xl', 40),
        ('x', 10),
        ('ix', 9),
        ('v', 5),
        ('iv', 4),
        ('i', 1),
    ]

    @staticmethod
    def find_value(character):
        for value in Config.conversion_table:
            if value[0] == character:
                # found
                return value[1]

        return None


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
                    continue  # found
                else:
                    print(f"Not valid roman numeral, a letter {character} in position {index + 1} is not valid.")
                    not_valid = True
            if not_valid:
                exit()



            # Valid roman numeral
            self.roman_number = str(input_number).lower()

            if not self.valid_roman():
                print(f"Not valid (too many repeats of single character) in {self.roman_number}.")
                exit()

            self.is_roman = True
            self.is_integer = False
            print("Number recognized as roman.")

        else:
            # Not integer nor roman
            print("Bad input, mixed decimals with romans.")
            exit()

    def valid_roman(self):
        """ Checks if enterer roman value is valid.
            Returns True if valid, False if invalid
        """
        # Goes through all characters in roman numeral
        # and checks if there is more than 3 same letters
        # consequently

        # counters
        counter = 0
        last_character = str()

        for char_index, roman_character in enumerate(self.roman_number):
            if char_index == 0:
                # first letter
                last_character = roman_character
                continue

            # For not first letter assume there is 'last_character' previously created
            if last_character == roman_character:
                counter += 1
            else:
                counter = 0
                last_character = roman_character

            if counter >= 3:
                # Too many characters
                return False

        return True

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
        #
        # Approach:
        #
        # Let's save all interesting values as list of tuples and subtract
        # one by one until the number is cleared to zero.

        # Make a 'pointer' to the biggest item (the first one)
        conversion_index = 0

        # Local copy of number (we'll destroy it soon :-D )
        number = self.number

        # A place to save output
        output = list()

        # Main loop
        while number:
            # Get the floor of number/max from list
            division = number // Config.conversion_table[conversion_index][1]

            # Save the rest of a division to number
            number %= Config.conversion_table[conversion_index][1]

            # Creating output
            while division:
                # Save a letter (or group of letters)
                output.append(Config.conversion_table[conversion_index][0])

                # next step
                division -= 1

            # Done for this letter, let's skip to another
            conversion_index += 1

        # Returns the joined output
        return ''.join(output).upper()

    def convert_to_integer(self):
        """ Converts number to integer """

        # Method:
        #
        # Going from left to right, every letter is either followed
        # by bigger or lesser number.
        # If it is followed by lesser number, the number we are talking
        # about has to be added to cumulative sum, if the following number
        # is bigger, actual number has to be subtracted from the cumulative sum.
        #
        # Approach:
        #
        # We have Config.conversion_table with values, we need just the
        # "one letter" stuff, easy filtering there.

        # Cumulative sum
        cum_sum = 0

        for index, character in enumerate(self.roman_number):
            # Maximal index
            max_index = len(self.roman_number) - 1

            # Reading and comparing two consequent characters
            character_value = Config.find_value(character)

            # Reading a value of next character only if not last
            if index < max_index:
                next_character_value = Config.find_value(self.roman_number[index + 1])
            else:
                next_character_value = 0  # There is no other one

            if character_value >= next_character_value:
                # Actual number has to be added
                cum_sum += int(character_value)
            else:
                # Actual number has to be subtracted
                cum_sum -= int(character_value)

        # Returns the cumulative sum
        return cum_sum


# RUNTIME #
def main():
    """ Main function """
    input_number = str(input("Enter the input either in decimal (integer) \nor in Roman (case doesn't matter): "))

    number = Number(input_number)

    if number.is_integer:
        print(f"Converted integer {number.number} to roman form is {number.convert_to_roman()}.")

    if number.is_roman:
        print(f"Converted roman {number.roman_number} to integer form is {number.convert_to_integer()}.")


if __name__ == "__main__":
    main()
