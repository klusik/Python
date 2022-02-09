'''
Write a function that accepts a string, and returns true if it is in the form of a phone number.
Assume that any integer from 0-9 in any of the spots will produce a valid phone number.

Only worry about the following format:
(123) 456-7890 (don't forget the space after the close parentheses)

Examples:

"(123) 456-7890"  => true
"(1111)555 2345"  => false
"(098) 123 4567"  => false

'''

""" Author: klusik@klusik.cz """
import logging

logging.basicConfig(level=logging.INFO)



def valid_phone_number(phone_number):
    """ Returns true if valid phone number """

    # Length 14 chars
    if not len(str(phone_number)) == 14:
        logging.info("Length")
        return False

    # String
    if not str(phone_number) == phone_number:
        logging.info("Not a string")
        return False

    # Parentheses
    if not (phone_number[0] == '(' and phone_number[4] == ')'):
        logging.info("Parentheses")
        return False

    # Prefix number
    if not str(phone_number[1:3]).isnumeric():
        logging.info("Prefix")
        return False

    # A space
    if not phone_number[5] == ' ':
        logging.info("Space")
        return False

    # A triplet before dash
    if not str(phone_number[6:8]).isnumeric():
        logging.info("Triplet")
        return False

    # Dash
    if not phone_number[9] == '-':
        logging.info("Dash")
        return False

    # Final number
    if not str(phone_number[10:]).isnumeric():
        logging.info("Final number")
        return False


    # Everything seems ok
    logging.info("OK")
    return True

if __name__ == "__main__":


    number = str(input("Enter the phone number: "))

    if valid_phone_number(number):
        print(f"Cool, {number} is a valid number.")
    else:
        print(f"Nah, {number} is not a valid number.")