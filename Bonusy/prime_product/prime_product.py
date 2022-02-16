"""
    This program returns a list of primes as a prime product
    of given number.

    Author:     Rudolf Klusal 2022
"""

# IMPORTS #

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

    def __init__(self):
        # Define file name
        self.cache_file_name = Config.cache_file_name
        
        # List of found primes (computed or loaded)
        self.found_primes = list()

        # Pointer to a specific prime
        self.prime_index = None # Initially None, not zero

        # Loads a cache
        self.load_cache()

    def add_next_prime(self):
        """
            Adds next prime to list.
            :return: Integer of index of last prime added
        """

    def get_prime(self):
        """
            Returns actual prime from list.
            :return: Integer, actual prime
        """

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


class Product:
    """
        Handles the primes factorization
    """

# RUNTIME #
def main():
    """ Main runtime function """

if __name__ == "__main__":
    main()