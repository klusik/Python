"""Simulation of an ecosystem"""

# IMPORTS
import logging
import random

from enum import Enum

# CLASSES
class Defaults:
    """Default values"""

    # Attributes

    # Number of trees
    trees = 100
    treeMaxAge = 100 * 365 # 100 years


    # Number of humans
    humans = 100
    humanMaxAge = 71 * 365 # 71 years

    # Number of omnivores
    omnivores = 100
    omnivoreMaxAge = 30 * 365 # 30 years

    # Number of herbivores
    herbivores = 100
    herbivoreMaxAge = 30 * 365 # 30 years

    # Number of predators
    predators = 100
    predatorMaxAge = 20 * 360 # 20 years



class Ecosystem:
    """Ecosystem playground"""

    # Set of all ids available
    idSet = set()

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
                    break

    def getTrees(self, treeId = None):
        if treeId:
            print(f"Tree with id = {treeId}")
        else:
            for tree in self.trees:
                print(f"Tree: Id = {str(tree.treeId):5} | "
                        f"Happiness: {str(tree.happiness):1.3} | "
                        f"Age: {str(tree.age):3} | "
                        f"Sex: {str(sex(tree.sex).name):7}")


    def __init__(self, initialState = None,
                 trees = Defaults.trees,
                 herbivores = Defaults.herbivores,
                 omnivores = Defaults.omnivores,
                 predators = Defaults.predators,
                 humans = Defaults.humans):
        try:
            # Generate trees
            self.trees = list()
            for tree in range(trees):
                newTreeId = self.generateId()
                self.trees.append(Tree(treeId = newTreeId))

            # Generate herbivores
            self.herbivores = list()
            for herbivore in range(herbivores):
                newHerbivoreId = self.generateId()
                self.herbivores.append(Herbivore(herbivoreId = newHerbivoreId))

            # Generate omnivores
            self.omnivores = list()
            for omnivore in range(omnivores):
                self.omnivores.append(Omnivore(omnivoreId = self.generateId()))

            # Generate predators
            self.predators = list()
            for predator in range(predators):
                self.predators.append(Predator(predatorId = self.generateId()))

            # Generate humans
            self.humans = list()
            for human in range(humans):
                self.humans.append(Human(humanId = self.generateId()))

        except Exception as exception:
            raise exception


class sex(Enum):
    MALE = 1
    FEMALE = 2


class Being():
    """Default class for every being in Ecosystem"""

    # Happiness ranges from 0 to 1, 0 totally sad, 1 totally happy
    happiness = 1.0
    age = 0
    sex = 0

class Tree(Being):
    def __init__(self, treeId):
        self.treeId = treeId
        self.sex = random.randrange(1, 3, 1)


class Herbivore(Being):
    def __init__(self, herbivoreId):
        self.herbivoreId = herbivoreId
        self.sex = random.randrange(1, 3, 1)


class Omnivore(Being):
    def __init__(self, omnivoreId):
        self.omnivoreId = omnivoreId
        self.sex = random.randrange(1, 3, 1)


class Predator(Being):
    def __init__(self, predatorId):
        self.predatorId = predatorId
        self.sex = random.randrange(1, 3, 1)


class Human(Being):
    def __init__(self, humanId):
        self.humanId = humanId
        self.sex = random.randrange(1, 3, 1)


# CONFIG
logging.basicConfig(level=logging.INFO)


# RUNTIME
def main():
    try:
        # Creating an ecosystem playground
        ecosystem = Ecosystem()
        ecosystem.getTrees()


    except TypeError:
        logging.INFO("e")

    finally:
        print("That's all :-)")


if __name__ == "__main__":
    main()
