"""
    Codewars: https://www.codewars.com/kata/54d512e62a5e54c96200019e/train/python

    Description:
        Given a positive number n > 1 find the prime factor decomposition of n. The result will be a string with the following form :

        "(p1**n1)(p2**n2)...(pk**nk)"
        with the p(i) in increasing order and n(i) empty if n(i) is 1.

        Example: n = 86240 should return "(2**5)(5)(7**2)(11)"

    Author: klusik@klusik.cz
"""


# IMPORTS #

# FUNCTIONS #
def prime_factors(input_number):
    pass


# RUNTIME #
if __name__ == "__main__":
    number = int(input("Enter the number: "))

    print(prime_factors(number))
