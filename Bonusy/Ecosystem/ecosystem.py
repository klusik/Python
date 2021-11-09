"""Simulation of an ecosystem"""

# IMPORTS
import logging
import random
import time
import os

from enum import Enum


# CLASSES
class Defaults:
    """Default values"""

    # Attributes

    # Number of trees
    trees = 100
    treeMaxAge = 100 * 365  # 100 years

    # Number of humans
    humans = 100
    humanMaxAge = 71 * 365  # 71 years

    # Number of omnivores
    omnivores = 100
    omnivoreMaxAge = 30 * 365  # 30 years

    # Number of herbivores
    herbivores = 100
    herbivoreMaxAge = 30 * 365  # 30 years

    # Number of predators
    predators = 100
    predatorMaxAge = 20 * 360  # 20 years

    # Default length of a separator
    separatorLength = 80

    # Default symbol for a separator
    separatorSymbol = '-'

    # Default number of simulated days
    maxSimulatedDays = 1000

class Ecosystem:
    """Ecosystem playground"""

    # Set of all ids available
    idSet = set()

    # Actual date (day in simulation)
    day = 0

    # Static methods
    @staticmethod
    def printSeparator(symbol = Defaults.separatorSymbol,
                       number = Defaults.separatorLength):
        print(symbol * number)

    @staticmethod
    def printHeader(text, firstSpace = True):
        if firstSpace:
            print("")

        Ecosystem.printSeparator()
        print(text)
        Ecosystem.printSeparator()


    # Instance methods
    def generateId(self):
        """Generate unique id not previously present at idSet"""
        if not len(self.idSet):
            # Empty set
            self.idSet.add(1)
            return 1

        else:
            # Not empty set
            addition = 1
            while True:
                newId = max(self.idSet) + addition
                if newId in self.idSet:
                    addition += 1
                    continue
                else:
                    self.idSet.add(newId)
                    return newId

    def getTrees(self, treeId=None):
        if treeId:
            print(f"Tree with id = {treeId}")
        else:
            for tree in self.trees:
                print(f"Tree: Id = {str(tree.treeId):5} | "
                      f"Happiness: {str(tree.happiness):1.3} | "
                      f"Age: {str(tree.age):3} | "
                      f"Sex: {str(Sex(tree.sex).name):7}")

    def __init__(self, initialState=None,
                 trees=Defaults.trees,
                 herbivores=Defaults.herbivores,
                 omnivores=Defaults.omnivores,
                 predators=Defaults.predators,
                 humans=Defaults.humans
                 ):
        try:
            # Generate beings

            self.beings = list()

            for tree in range(trees):
                newTreeId = self.generateId()
                self.beings.append(Tree(treeId=newTreeId))

            # Generate herbivores
            for herbivore in range(herbivores):
                newHerbivoreId = self.generateId()
                self.beings.append(Herbivore(herbivoreId=newHerbivoreId))

            # Generate omnivores
            for omnivore in range(omnivores):
                self.beings.append(Omnivore(omnivoreId=self.generateId()))

            # Generate predators
            for predator in range(predators):
                self.beings.append(Predator(predatorId=self.generateId()))

            # Generate humans
            for human in range(humans):
                self.beings.append(Human(humanId=self.generateId()))

        except Exception as exception:
            raise exception

    def nextDay(self):
        """Simulates next day"""
        self.day += 1

    def getAllStats(self):
        """Returns a dict with alive & dead
            and all stats of all beings."""

        # Compute all alive & dead beings

        # Total numbers
        allAliveDead = dict()
        allAliveDead['alive'] = 0
        allAliveDead['dead'] = 0

        # Numbers for all Classes
        allInEcosystem = dict()

        for being in self.beings:
            # Alive counter
            if being.alive:
                allAliveDead['alive'] += 1
            else:
                allAliveDead['dead'] += 1

            # All beings counter
            if being.getClass() in allInEcosystem:
                # If that class name exists in the dict,
                # just iterrate
                if being.alive:
                    allInEcosystem[being.getClass()]['alive'] += 1
                else:
                    allInEcosystem[being.getClass()]['dead'] += 1
            else:
                # Create new key in dict, if
                # the class name doesn't exist
                allInEcosystem[being.getClass()] = dict()
                if being.alive:
                    allInEcosystem[being.getClass()]['alive'] = 1
                    allInEcosystem[being.getClass()]['dead'] = 0
                else:
                    allInEcosystem[being.getClass()]['alive'] = 0
                    allInEcosystem[being.getClass()]['dead'] = 1

        return {'alivedead': allAliveDead,
                'allInEcosystem': allInEcosystem}

    def displayStats(self):
        """Display statistics about current day"""
        Ecosystem.printHeader("Simulation", False)

        print(f"This is the day {self.day} of the simulation.")

        # Read all statistics
        allStats = self.getAllStats()

        # Read just dead & alive
        beingsAliveAndDead = allStats['alivedead']

        alive = beingsAliveAndDead['alive']
        dead = beingsAliveAndDead['dead']
        total = alive + dead

        # Final prints
        Ecosystem.printHeader("Alive & dead")

        print(f"There is {total} beings in total, {alive} beings alive and {dead} beings dead.")

        Ecosystem.printHeader("All beings alive & dead")

        maxBeingNameLength = len(max(list(allStats['allInEcosystem'].keys()), key=len))

        for beingTypeKey, beingTypeAlive in allStats['allInEcosystem'].items():
            print(f"{beingTypeKey:{maxBeingNameLength+1}}: Alive: {beingTypeAlive['alive']} Dead: {beingTypeAlive['dead']}")



class Sex(Enum):
    """It will accept only two biological genders"""
    MALE = 1
    FEMALE = 2


class Being:
    """Default class for every being in Ecosystem"""

    # Happiness ranges from 0 to 1, 0 totally sad, 1 totally happy
    happiness = 1.0

    # Age in days
    age = 0

    # Birthday date (day in simulation)
    birthday = 0

    # Death date (day in simulation)
    death = 0

    # Sex as in the Enum(Sex)
    # Each instance creates (randomizes) its
    # own sex
    sex = 0

    # Being is by default alive, but after a while
    # it dies
    alive = True

    # Getter of the string of the class name
    def getClass(self):
        return str(type(self).__name__)


class Tree(Being):
    """Default tree with only general specifics"""
    def __init__(self, treeId):
        self.treeId = treeId
        self.sex = random.randrange(1, 3, 1)


class Herbivore(Being):
    """Default herbivore with only general specifics"""
    def __init__(self, herbivoreId):
        self.herbivoreId = herbivoreId
        self.sex = random.randrange(1, 3, 1)


class Omnivore(Being):
    """Default omnivore with only general specifics"""
    def __init__(self, omnivoreId):
        self.omnivoreId = omnivoreId
        self.sex = random.randrange(1, 3, 1)


class Predator(Being):
    """Default predator with only general specifics"""
    def __init__(self, predatorId):
        self.predatorId = predatorId
        self.sex = random.randrange(1, 3, 1)


class Human(Being):
    """Default human with only general specifics"""
    def __init__(self, humanId):
        self.humanId = humanId
        self.sex = random.randrange(1, 3, 1)


# CONFIG
logging.basicConfig(level=logging.INFO)


# RUNTIME
def main():
    def clearScreen():
        os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Creating an ecosystem playground
        ecosystem = Ecosystem()

        # Ecosystem created, now it's time to simulate
        # days in the ecosystem
        for day in range(Defaults.maxSimulatedDays):
            clearScreen()
            ecosystem.displayStats()
            time.sleep(0.1)
            ecosystem.nextDay()



    except TypeError:
        logging.info("e")
        raise

    finally:
        print("That's all for today :-)")


if __name__ == "__main__":
    main()
