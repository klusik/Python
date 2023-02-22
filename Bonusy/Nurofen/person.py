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

    @age.setter
    def age(self, age: int):
        self.__age = age

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    # OBJECT METHODS #
    def __str__(self):
        return f"Name: {self.name}\nAge: {self.age}"

    # METHODS #
    def save_to_file(self):
        """ Saves all data to a file """
        try:
            with open(f"{config.Config.data_path}/{self.name}.nur", "w", encoding="utf8") as f_person:
                f_person.write("ahoj")
        except IOError as err:
            print(f"Unable to save file: {str(err)}")

    def setup_new_user(self):
        """ Creates a new user """

        # User name
        while True:
            try:
                input_name = str(input(f"Enter the new user name (hit Enter for '{self.name}'): ")) or self.name
                input_age = int((input(f"Enter the new user age (hit Enter for '{self.age}'): ")) or self.age)

            except ValueError as err:
                print(f"Entered value is not valid, try different name.")
                continue

            except KeyboardInterrupt as err:
                print(f"Ending program. {str(err)}")
                exit(1)

            self.name = input_name
            self.age = input_age
            break

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
