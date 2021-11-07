"""Simulation of an ecosystem"""

# IMPORTS
import logging


# CLASSES
class Defaults:
    """Default values"""

    # Attributes

    # Number of trees
    trees = 100

    # Number of humans
    humans = 100

    # Number of omnivores
    omnivores = 100

    # Number of herbivores
    herbivores = 100

    # Number of predators
    predators = 100


class Ecosystem:
    """Ecosystem playground"""

    # Set of all ids available
    idSet = set()

    def generateId(self):
        """Generate unique id not previously present at idSet"""
        if not len(self.idSet):
            # Empty set
            self.idSet.add(1)

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

    def getTrees(self):
        for tree in self.trees:
            print(f"Tree: Id = {tree.treeId}")


    def __init__(self, initialState = None, trees = Defaults.trees):
        try:
            self.trees = list()
            for tree in range(trees):
                newTreeId = self.generateId()
                self.trees.append(Tree(treeId = newTreeId))

        except Exception as exception:
            raise exception



class Tree:
    def __init__(self, treeId):
        self.treeId = treeId


class Herbivore:
    pass


class Omnivore:
    pass


class Predator:
    pass


class Human:
    pass


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
