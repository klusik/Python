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
import math


# FUNCTIONS #
def is_prime(number) -> bool:
    """ Returns True if number is prime """

    if number < 2:
        return False

    if not (number % 2):
        return False

    for test in range(3, math.ceil(math.sqrt(number)), 2):
        if not (number % test):
            return False

    return True

def generate_primes_to_number(input_number) ->list:
    """ Generates a list of usable primes to input_number / 2 """
    list_of_primes = [2]

    for number in range(3, math.floor(input_number / 2 +1), 2):
        if not(input_number % number):
            list_of_primes.append(number)

    return list_of_primes

def factorize_number(input_number) -> str:
    """ Generates factorization """

    # Get all primes
    primes = generate_primes_to_number(input_number)

    # Result placeholder
    factorization = ""

    # Counts of divisions
    divisions = dict()

    # Divide the input_number periodically, until possible by every prime,
    # track counts of divisions and generate a string accordingly

    for prime in primes:
        while True:
            if not (input_number % prime):
                # Divisible, add to divisions
                try:
                    # If exist
                    divisions[prime] += 1
                except KeyError:
                    # not exist
                    divisions[prime] = 1

                # Do division
                input_number /= prime
            else:
                # Not divisible, next prime
                break

    # Compile factorization
    for prime in divisions:
        if divisions[prime] == 1:
            factorization += f"({prime})"
        else:
            factorization += f"({prime}**{divisions[prime]})"

    # Return result
    return factorization


def prime_factors(input_number) -> str:
    if not is_prime(input_number):
        return factorize_number(input_number)
    else:
        return (f"({input_number})")


# RUNTIME #
if __name__ == "__main__":

    try:
        number = int(input("Enter the number: "))
        print(prime_factors(number))
    except KeyboardInterrupt:
        print("Bye :-)")
