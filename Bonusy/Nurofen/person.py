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
            self.setup_new_user()

    # PROPERTIES HANDLING #
    @property
    def age(self) -> int:
        return self.__age

    @property
    def name(self) -> str:
        return self.__name

    # METHODS #
    def setup_new_user(self):
        """ Creates a new user """

        # User name
        while True:
            try:
                input_name = str(input(f"Enter the new user name (hit Enter for '{self.name}'): ")) or self.name
                input_age = str((input(f"Enter the new user age (hit Enter for '{self.age}'): ")) or self.age)

            except ValueError as err:
                print(f"Entered value is not valid, try different name.")
                
            except KeyboardInterrupt as err:
                print(f"Ending program. {str(err)}")
                exit(1)

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
