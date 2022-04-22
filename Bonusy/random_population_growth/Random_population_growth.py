"""
    The goal is to simulate a unbounded population growth
    with added randomness.

    There will be some constants (user input):

        -- probability of birth of every two M/F for another person
        -- min age of concieving (all the same)
        -- max age of concieving (all the same)
        -- max age (all the same), after this age random death occurs
        -- max number of iterations

"""

# IMPORTS #
import random

# CLASSES #
class Defaults:
    """ Default constants and stuff """

    # Probability of birth
    # If two persons want to have a child, this is the probabilty
    # of concieving a child
    probability_of_birth = 0.5

    # Minimal age of concieving a child
    # Both of parents must have at least this age to be able to have a child
    min_age_of_concieving = 20

    # Maximal age of concieving a child
    # Both of parents must have this age or lower.
    max_age_of_concieving = 30

    # Initial population
    # Initial population of the simulation
    initial_population = 1000

    # Initial population sex distribution
    # How much M over F
    # 1 means all M, 0 means all F
    initial_sex_distribution = 0.5

    # Simulation length
    maximal_number_of_iterations = 100


class Person:
    def __init__(self):
        pass

    def __repr__(self):
        pass

class Simulation:
    def __init__(self):
        pass

    def __repr__(self):
        pass

# RUNTIME #
def main():
    pass

if __name__ == "__main__":
    main()