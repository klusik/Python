"""
    This program returns a list of primes as a prime product
    of given number.

    Author:     Rudolf Klusal 2022
"""

# IMPORTS #
import math
import logging


# CLASSES #
class Config:
    """
        Configuration
    """
    cache_file_name = "primes_cache.kls"

class Primes:
    """
        Caches all found primes to file,
        so next time it won't be necessary
        to compute them again and again
    """

    def __init__(self,
                 number_to_do_product, # This number will be factorized to primes
                 ):

        # Initial check
        self.number_to_do_product = number_to_do_product
        if not self.valid_number():
            raise ValueError


        # Define file name
        self.cache_file_name = Config.cache_file_name
        
        # List of found primes (computed or loaded)
        self.found_primes = list()

        # Pointer to a specific prime
        self.prime_index = None # Initially None, not zero

        # Found factors list
        self.found_factors = list()

        # Loads a cache
        self.load_cache()

    def valid_number(self):
        """ Checks if self.number_to_do_product is valid number """
        return (
            str(self.number_to_do_product).isnumeric() and
            (int(self.number_to_do_product) > 0) and
            ((float(self.number_to_do_product) - int(self.number_to_do_product)) == 0)
            )

    def get_actual_prime(self):
        """ Returns actual prime """
        return self.found_primes[self.prime_index]

    def set_next_prime(self):
        """ Sets the prime_index pointer to next one in the list """
        self.prime_index += 1

        # If the index is in the list
        if self.prime_index < len(self.found_primes):
            # It's okay
            return self.prime_index
        else:
            # Need to generate a new prime
            self.add_next_prime()
            return self.prime_index

    def compute_factors(self):
        """ Compute all factors """

        # Let's go through all the primes found and try to use them as
        # a dividers, modulo-check them and if checked, just divide on
        # and on.
        # If one particular prime not found in the list,
        # it's added and saved in the cache.

        # Floating residue initial
        number_rest = self.number_to_do_product

        # Beginning of the list
        self.prime_index = 0

        while True:
            if len(self.found_primes) == 0:
                # If the list of pre-generated primes
                # is empty, generate at least one prime to begin with
                self.add_next_prime()

            if number_rest == 1:
                # End of the cycle
                break

            # Try the division
            if number_rest % self.get_actual_prime() == 0:
                # It's divisible, so this prime is a factor.
                self.found_factors.append(self.get_actual_prime())

                # Get the rest of the number
                number_rest /= self.get_actual_prime()

                # continue to next cycle with the same prime.
                continue

            else:
                # This prime is not a divider, so just skip to next prime
                self.set_next_prime()


    def get_factors(self):
        """ Returns a list of factors """
        return self.found_factors


    @staticmethod
    def is_prime(number):
        """ Returns True if the number is prime """
        for tested in range(3, math.ceil(math.sqrt(number))+1, 2):
            if number % tested == 0:
                # If divisible by any number,
                # it's not a prime
                return False

        # Never hit the divisible trigger,
        # so it's a prime

        return True

    def add_next_prime(self):
        """
            Adds next prime to list.
            :return: Integer of index of last prime added
        """

        # Last prime
        last_prime = self.get_last_prime()
        if last_prime == None:
            # First two primes would be "2" and "3"
            self.found_primes.append(2)
            self.found_primes.append(3)

        else:
            # If not empty list, generate other
            new_prime_candidate = last_prime + 2
            while True:
                if self.is_prime(new_prime_candidate):
                    self.found_primes.append(new_prime_candidate)
                    return new_prime_candidate
                else:
                    new_prime_candidate += 2


    def get_last_prime(self):
        """
            Returns actual prime from list.
            :return: Integer, actual prime
        """

        # If not prime computed yet, returns None,
        # if computed, return the last one

        if len(self.found_primes):
            return self.found_primes[-1]
        else:
            return None

    def load_cache(self):
        """
            Loads cache from a file if exists
            :return: True if successful, False if not
        """
        try:
            with open(self.cache_file_name, "r") as link_cache_file:
                # Reads the file
                content_cache_file = link_cache_file.read()

                # Going through all numbers and saving them to cache
                for number in str(content_cache_file).split():
                    self.found_primes.append(int(number))

                # Setting the actual index to zero
                self.prime_index = 0

        except FileNotFoundError:
            # Cache doesn't exist, no problem.
            return False
        finally:
            return True

    def save_cache(self):
        """
            Saves cache to file
            :return: True if saved successfully, False if not.
        """
        try:
            with open(self.cache_file_name, "r") as link_cache_file:
                # Reading the last prime added
                last_prime = int(str(link_cache_file.read()).split[-1])
        except FileNotFoundError:
            # Cache doesn't exist yet, nevermind :-)
            pass
        finally:
            # Writing the cache file
            try:
                with open(self.cache_file_name, "a") as link_cache_file:
                    pass
            except Exception as exception:
                print("Writing cache file error.")
                raise(exception)



# RUNTIME #
def main():
    """ Main runtime function """
    try:
        # User input
        user_input = input("Enter a whole positive number to do a prime product: ")
        number_to_do_product = int(user_input)

        # Create a product
        product = Primes(number_to_do_product)

        # Compute a factorization
        product.compute_factors()

        # Displaying a factors
        print(product.get_factors())

    except ValueError:
        print(f"Entered value '{user_input}' is invalid.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()