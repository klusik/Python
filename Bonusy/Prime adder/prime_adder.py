"""
    Create a prime adder, which can construct any number from input
    but just only as a sum of unique primes. For example:

    input: 10
    output: [2, 5, 3]

    input: 11
    output: [11]

    input: 20
    output: [2, 5, 13]
"""
# IMPORTS #
import math


# FUNCTIONS #
def is_prime(tested_number: int) -> bool:
    """ Tests if tested_number is a prime.

    @tested_number: integer
    @rtype: bool
    """

    # Filters
    if tested_number < 2:
        return False

    if tested_number == 2:
        return True

    if not tested_number % 2:
        return False

    for prime_iter in range(3, int(math.sqrt(tested_number)) + 1, 2):
        if not tested_number % prime_iter:
            return False

    return True


def sum_of_primes(input_number: int) -> (int, list):
    sum_primes: set = set()

    if not is_prime(input_number):
        tested = 2
        while input_number > 1:
            if is_prime(tested) and input_number % tested == 0:
                sum_primes.add(tested)
                input_number //= tested
            else:
                tested += 1

        if input_number < 0:
            return None, None
        else:
            return sum(sum_primes), sorted(list(sum_primes))
    else:
        return input_number, [input_number]


# RUNTIME #
if __name__ == "__main__":
    print(sum_of_primes(10))
