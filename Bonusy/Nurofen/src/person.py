"""
    Person class
    Author: Rudolf Klusal
"""


class Person:
    """ Person class """

    def __init__(self,
                 name: str = None,
                 age: int = None,
                 ):

        if not (name and age):
            # Need other definitions
            pass
        else:
            self.__name: str = name
            self.__age: int = age

    @property
    def age(self) -> int:
        return self.__age

    pass
