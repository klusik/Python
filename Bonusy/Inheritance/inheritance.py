"""
    Explore OOP inheritance
"""


class Color:
    pass


class Liquid:
    def __init__(self,
                 mass_concentration
                 ):
        self.liquid = True
        self.mass_concentration = mass_concentration
        self.color = None


class Milk(Liquid):
    def __init__(self):
        super().__init__(1)
        self.color = "white"


if __name__ == "__main__":
    milk = Milk()

    print(milk.color, milk.mass_concentration)
