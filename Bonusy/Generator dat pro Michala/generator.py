""" Data generator for Michal """

import random
import names
from enum import Enum


class Gender(Enum):
    MALE = 0
    FEMALE = 1

class Animal:

    def __init__(self):
        self.weight = random.randrange(5, 25, 1)
        self.gender = Gender(random.randrange(0,2,1)).name

        if self.gender == "FEMALE":
            self.name = names.get_first_name(gender="female")
        else:
            self.name = names.get_first_name(gender="male")

        self.age = random.randrange(2, 15, 1)


class Dog(Animal):
    def __init__(self):
        super().__init__()

class Cat(Animal):
    def __init__(self):
        super().__init__()

class Turtle(Animal):
    def __init__(self):
        super().__init__()

class Giraffe(Animal):
    def __init__(self):
        super().__init__()


def main():

    # Create animals in zoo

    animals = set()

    for animal in range(65535):
        if animal%10000 == 0:
            print(f"{animal} animals generated.")
        animal = random.randrange(1,5,1)
        if animal == 1:
            animals.add(Dog())
        if animal == 2:
            animals.add(Cat())
        if animal == 3:
            animals.add(Turtle())
        if animal == 4:
            animals.add(Giraffe())

    print(f"{len(animals)} animals")

    with open("animals.txt", "w") as fileW:
        for number, animal in enumerate(animals):
            if number%10000 == 0:
                print(f"{number} animals written to file...")
            print(f"{number+1:7} | "
                  f"{(animal.name + ' (' + str(animal.__class__.__name__) + ') '):24}| "
                  f"{animal.gender:7} "
                  f"{animal.weight:3} kg "
                  f"{animal.age:3} years"
                  , file=fileW)


if __name__ == "__main__":
    main()