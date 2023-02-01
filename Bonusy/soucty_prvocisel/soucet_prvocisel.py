"""
    Uživatel zadá číslo

    Program najde všechny možné součty prvočísel, které k danému číslu vedou
"""
# IMPORTS #
import math


# RUNTIME #
def is_prime(number: int) -> bool:
    for iter in range(3, int(math.sqrt(number)+1), 2):
        if not (number % iter):
            return False
    return True


def generate_primes_to(max_number: int) -> list:
    """ Generates all numbers up to max_number """

    list_primes: list = list()

    list_primes.append(2)

    for number in range(3, max_number + 1, 2):
        if is_prime(number):
            list_primes.append(number)

    return list_primes


if __name__ == "__main__":
    user_number: int = 0
    while user_number < 2:
        user_number = int(input("Enter the number (2 and more): "))

    list_primes: list = generate_primes_to(user_number)

    print(list_primes)
