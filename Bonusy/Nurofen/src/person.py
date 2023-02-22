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

    # PROPERTIES HANDLING #
    @property
    def age(self) -> int:
        return self.__age

    @property
    def name(self) -> str:
        return self.__name

    pass
