"""
    Just a test if everything works under linux mint :-)
"""


# CLASSES #
class Pudding:
    def __init__(self,
                taste: str = None,
                ):
        if taste:
            self.__taste = taste
        else:
            self.__taste = "vanilla"

    @property
    def taste(self):
        return self.__taste

    @taste.setter
    def taste(self, taste):
        self.__taste = taste




# RUNTIME #
if __name__ == "__main__":
    cokopuding = Pudding("chocolate")

    print(cokopuding.taste)


