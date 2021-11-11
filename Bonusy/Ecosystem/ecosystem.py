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
    treeInitialFruits = 100 # 100 fruits for every tree
    treeFruitDailyBase = 1 # One fruit each day



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
    maxSimulatedDays = 10

    # Default time delay between days
    timeDelay = 0.1

    # Happiness default lenght in days
    lengthOfHistory = 10

    # Default happiness
    happiness = 1.0

    # Happiness triggers
    superHappy = 0.8
    normalHappy = 0.5
    lessHappy = 0.3
    reallyUnhappy = 0.1

class Render:
    """Text renderer"""

    # List of lines to render
    _renderBuffer = list()

    def addToRender(self, textToRender):
        """Adds a string to the list to render"""
        self._renderBuffer.append(str(textToRender))

    def render(self):
        """Rendering"""
        renderedString = "".join(self._renderBuffer)
        print(renderedString)


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

        # Rules:
        #
        # PREGNANCY:
        # If there's at least two of the same species,
        # both having happines > 0.5
        # for more than some days in row,
        # having different genders and both are fertile,
        # they can have an ancestor.
        #
        # FOOD:
        # Happiness determines how much the being
        # wants to eat. More happiness, less it
        # wants to eat. Happiness at very low levels
        # for a few days means death.
        #
        # Trees have 'fruits'. More of happiness means
        # more fruits to be regenerated every day
        #
        # Herbivores eat fruits from trees, nothing else.
        #
        # Omnivores eat fruits and dead herbivores, omnivores and predators.
        # More happier omnivore eats more fruits and less dead beings.
        #
        # Predators eat only alive omnivores, herbivores and other predators,
        # determined by happiness, if happiness very low, they eat
        # even other predators.

        # Simulation goes through all beings
        # feed them, change their happiness in once
        # adds some 'randomization' to happiness and everything.

        # Days counter incrementation
        self.day += 1

        # Let's go through all the beings and
        # as we determine what class they're from
        # we can co class-dependent stuff with them.
        for being in self.beings:
            if being.getClass() == "Tree":
                # Tending of trees

                # Each tree must grow new fruits if possible
                being.growNewFruits()


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

        # Average happiness
        allAverageHappiness = dict() # Average happiness for every class
        allBeingsHappiness = dict()  # Every happiness for every class

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

            # Log all beings happiness for later
            # computation of average
            if being.getClass() not in allBeingsHappiness:
                # Creating a new list in dict, key is the name
                # of the class (as a being species).
                allBeingsHappiness[being.getClass()] = list()

            # Insert a being happiness to list
            allBeingsHappiness[being.getClass()].append(being.happiness)

        # Averages counging
        for species in allBeingsHappiness:
            # Average is just a sum of all happinesses for
            # given species divided by number of
            # beings of that species (class)
            allAverageHappiness[species] = sum(allBeingsHappiness[species])/len(allBeingsHappiness[species])

        return {'alivedead': allAliveDead,
                'allInEcosystem': allInEcosystem,
                'allAverageHappiness': allAverageHappiness
                }

    def displayStats(self):
        """Display statistics about current day"""
        Ecosystem.printHeader("Simulation", False)

        print(f"This is the day {self.day} of the simulation.")

        # Read all statistics
        # in allStats is stored the whole dict of a Ecosystem
        allStats = self.getAllStats()

        # Read just dead & alive
        beingsAliveAndDead = allStats['alivedead']

        alive = beingsAliveAndDead['alive']
        dead = beingsAliveAndDead['dead']
        total = alive + dead

        # Final prints
        Ecosystem.printHeader("Alive & dead")

        print(f"There is {total} beings in total, "
              f"{alive} beings alive and "
              f"{dead} beings dead.")

        Ecosystem.printHeader("All beings alive & dead")

        # Just a helper for formatting.
        # Determines the maximal length of a key in dict allStats
        # so then it can print the whitespaces accordingly
        maxBeingNameLength = len(max(list(allStats['allInEcosystem'].keys()), key=len))

        # Print out the results table
        for beingTypeKey, beingTypeAlive in allStats['allInEcosystem'].items():
            print(f"{beingTypeKey:{maxBeingNameLength+1}}| "
                  f"Alive: {beingTypeAlive['alive']:5}, "
                  f"Dead: {beingTypeAlive['dead']:5}, "
                  f"Average happiness: {allStats['allAverageHappiness'][beingTypeKey]:5}")




class Sex(Enum):
    """It will accept only two biological genders"""
    MALE = 1
    FEMALE = 2


class Being:
    """Default class for every being in Ecosystem"""

    # Happiness ranges from 0 to 1, 0 totally sad, 1 totally happy
    happiness = Defaults.happiness

    # Fifo of happiness for last few days
    happinessHistory = list()

    # Lenght of happiness history
    happinessHistoryLength = Defaults.lengthOfHistory

    # Age in days
    age = 0

    # Maximal age
    maximalAge = 0

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

    # If a being is a fertile
    fertile = True

    # Some creatures can be pregnant, some doesn't
    canBePregnant = True

    # Minimal age to be able to get pregnant
    minimalPregnantAge = 0


    # Getter of the string of the class name
    def getClass(self):
        return str(type(self).__name__)

    def generateSex(self, numberOfSexes = 2):
        return random.randrange(1, numberOfSexes+1, 1)

    def __init__(self):
        self.sex = self.generateSex()


class Tree(Being):
    """Default tree with only general specifics"""
    def __init__(self, treeId):
        super().__init__()

        # ID
        self.treeId = treeId

        self.canBePregnant = False # Trees somehow cannot be pregnant :-)
        self.maximalAge = Defaults.treeMaxAge

        # Fruit stuff
        self.fruits = Defaults.treeInitialFruits
        self.maxFruits = Defaults.treeInitialFruits

    def growNewFruits(self):
        if self.fruits < self.maxFruits:
            # Growing new stuff
            # Depends on happiness
            if self.happiness >= Defaults.superHappy:
                # If superhappy, tree grows all fruits available
                self.fruits += Defaults.treeFruitDailyBase
            else:
                # If not superhappy, tree grows number of fruits
                # in dependency on it's own happiness.
                #
                # If the happiness is in the between of
                # lessHappy and superHappy, there's a linear
                # dependency as the multiplier.
                # If the happiness is below lessHappy,
                # the tree won't grow new fruits
                multiplierScale = Defaults.superHappy - Defaults.lessHappy
                multiplierOffset = Defaults.lessHappy

                if self.happiness >= Defaults.lessHappy:
                    # In case of hapiness between reasonable values
                    # just lower the fruit production
                    happinesScaled = (self.happiness - multiplierOffset) / multiplierScale
                else:
                    # If the happiness is really bad, just don't produce
                    # fruit at all.
                    happinesScaled = 0

                logging.info(f"Happines Scaled: {happinesScaled}")

                self.fruits += Defaults.treeFruitDailyBase * happinesScaled



        # randomize it always



class Herbivore(Being):
    """Default herbivore with only general specifics"""
    def __init__(self, herbivoreId):
        super().__init__()
        self.herbivoreId = herbivoreId
        self.maximalAge = Defaults.herbivoreMaxAge


class Omnivore(Being):
    """Default omnivore with only general specifics"""
    def __init__(self, omnivoreId):
        super().__init__()
        self.omnivoreId = omnivoreId
        self.maximalAge = Defaults.omnivoreMaxAge


class Predator(Being):
    """Default predator with only general specifics"""
    def __init__(self, predatorId):
        super().__init__()
        self.predatorId = predatorId
        self.maximalAge = Defaults.predatorMaxAge


class Human(Being):
    """Default human with only general specifics"""
    def __init__(self, humanId):
        super().__init__()
        self.humanId = humanId
        self.maximalAge = Defaults.humanMaxAge


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
            # clears the console output before rewriting
            clearScreen()

            # displays results
            ecosystem.displayStats()

            # a small delay to prevent blinking
            time.sleep(Defaults.timeDelay)

            # simulate a next day
            ecosystem.nextDay()



    except TypeError:
        logging.info("e")
        raise

    finally:
        print("That's all for today :-)")


if __name__ == "__main__":
    main()
