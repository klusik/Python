#
# CW: https://www.codewars.com/kata/58fea5baf3dff03a6e000102
#
# Task
# Given an integer n, lying in range [0; 1_000_000], calculate the number of digits in n! (factorial of n).
#
# Example
# For n = 0, the output should be 1 because 0! = 1 has 1 digit;
# For n = 4, the output should be 2 because 4! = 24 has 2 digits;
# For n = 10, the output should be 7 because 10! = 3628800 has 7 digits.
#

import numpy

def main():
    # User input
    try:
        numberInput = int((input("Input the 'n' value for n!: ")))
    except ValueError:
        print("That's not a good value, is it?")
        return False

    if numberInput < 0:
        print("Number less than zero, bye.")
        return False




if __name__ == "__main__":
    main()