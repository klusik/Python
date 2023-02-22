"""
    Person class
    Author: Rudolf Klusal
"""
# IMPORTS #
import config


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

        # Person initialization
        if not self.load_person_from_file():
            pass

    # PROPERTIES HANDLING #
    @property
    def age(self) -> int:
        return self.__age

    @property
    def name(self) -> str:
        return self.__name

    # METHODS #
    def load_person_from_file(self) -> bool:
        """ If that person in particular already exists,
        load it instead of creating a new person
        @rtype: bool
        """
        try:
            print(config.Config.data_path + '/soubor.dat')
            with open(f"{config.Config.data_path}/{self.name}.nur", 'r') as f_person:
                pass
        except FileNotFoundError as err:
            # New user
            return False
