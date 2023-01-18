""" A code from ChatGPT

Input query: Create simple model in python which behaves like a viral population, where there's some possibility
to be infected, some possibility to gain immunity to infection  and so on. S
imulate randomized movement of healthy non-imunized people and create an infection somewhere.

"""
import random


class Person:
    def __init__(self):
        self.is_infected = False
        self.is_immune = False

    def update(self):
        if not self.is_infected and not self.is_immune:
            if random.random() < 0.1:  # 10% chance of becoming infected
                self.is_infected = True
        elif self.is_infected:
            if random.random() < 0.2:  # 20% chance of gaining immunity
                self.is_infected = False
                self.is_immune = True


class Population:
    def __init__(self, size):
        self.people = [Person() for _ in range(size)]

    def spread_infection(self):
        infected_count = sum(1 for person in self.people if person.is_infected)
        if infected_count > 0:
            for person in self.people:
                if (not person.is_infected) and (
                not person.is_immune) and random.random() < 0.05:  # 5% chance of becoming infected when in contact with an infected person
                    person.is_infected = True

    def update(self):
        for person in self.people:
            person.update()
        self.spread_infection()


population = Population(1000)

# Infect one person in the population
population.people[0].is_infected = True

# Simulate the spread of the infection over time
for i in range(100):
    population.update()
    infected_count = sum(1 for person in population.people if person.is_infected)
    immune_count = sum(1 for person in population.people if person.is_immune)
    print(f"At time step {i}, {infected_count} people are infected and {immune_count} people are immune.")
