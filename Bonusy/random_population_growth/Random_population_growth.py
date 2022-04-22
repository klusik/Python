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
    initial_sex_distribution = 0.8

    # Simulation length
    maximal_number_of_iterations = 100


class Person:
    def __init__(self):
        # Determine sex by chance
        self.sex = self.decide_sex()

        self.age = 0

    def __repr__(self):
        output_string = f"Sex:\t\t{self.sex}\n"
        output_string += f"Age:\t\t{self.age}\n"
        return (output_string)

    def decide_sex(self):
        # Higher probability means more M than F
        return random.random() < Defaults.initial_sex_distribution


class Simulation:
    def __init__(self):
        # Set up defaults
        self.iteration = 1

        # Create a population
        self.population = []

        for _ in range(Defaults.initial_population):
            self.population.append(Person())

    def __repr__(self):
        output_string = "-" * 30 + "\n"
        output_string += f"Iteration:\t\t{self.iteration}\n"
        output_string += f"Population: \t{self.count_persons()}, M: {self.count_persons(1)} F: {self.count_persons(0)}"
        return (output_string)

    def count_persons(self,
                      sex = None):
        if sex in [0, 1]:
            # counter
            male_or_female = 0

            for person in self.population:
                if person.sex == sex:
                    male_or_female += 1
            return male_or_female
        else:
            return len(self.population)

    def step(self):
        self.iteration += 1


# RUNTIME #
def main():
    simulation = Simulation()

    for step in range(1, Defaults.maximal_number_of_iterations):
        simulation.step()

    # Final simulation
    print(simulation)


if __name__ == "__main__":
    main()
