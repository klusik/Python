"""
    Search for primes using 'construction' approach
"""

# IMPORTS
import math
import time

# FUNCTIONS
def is_prime(number):
    if number == 1:
        return False

    if number == 2:
        return True

    for divisor in range(3, math.floor(math.sqrt(number)), 2):
        if number % divisor == 0:
            return False

    return True


def main():

    # List of primes
    primes = list()


if __name__ == "__main__":
    main()
