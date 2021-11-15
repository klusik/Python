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

    for divisor in range(1, math.floor(math.sqrt(number))+1, 2):
        if number % divisor == 0:
            return False

    return True

def product(listOfNumbers):
    product=1
    for number in listOfNumbers:
        product *= number

    return product

def main():

    # List of primes
    primes = list()
    all_multiplications = list()

    # Add first prime
    primes.append(2)
    all_multiplications.append(2)

    # Defining some limit
    max_prime = 100000

    while(primes[-1] < max_prime):
        # Next prime
        next_prime_candidate = product(all_multiplications) + 1
        print(f"{next_prime_candidate}")
        all_multiplications.append(next_prime_candidate)

        if is_prime(next_prime_candidate):
            primes.append(next_prime_candidate)

        all_multiplications.append(next_prime_candidate)


    print(f"Numbers found as primes (not excesive list):")
    for prime in primes:
        print(f"{prime} ", end="")

    print("")



if __name__ == "__main__":
    main()
