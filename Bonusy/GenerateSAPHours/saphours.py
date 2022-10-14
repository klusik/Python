"""
    It won't be as great as Mr. Smallcastle's vision,
    but for default distribution, it should work.
"""
# IMPORTS #
import datetime


# CLASSES #
class Config:
    """ This class just handles configuration """

    # Configuration file
    config_file = "config.ini"

    # Used SAP numbers
    saves = "sap_numbers.txt"

    @staticmethod
    def get_config_file():
        return Config.config_file

    @staticmethod
    def get_saves_file():
        return Config.saves


class Calendar:
    """ Handles calendar """

    def __init__(self,
                 month=None):
        """ If month is not set up, uses actual month """

        if not month:
            # Set up an actual month
            month = datetime.datetime.now().month

        print(month)


class SAPNumbers:
    """ Handles everything about SAP numbers """

    def __init__(self):

        # List of SAP numbers
        self.numbers = []

        # Loading or creating SAP numbers
        if self.previous_exist():
            # Ask user if use previously saved sap numbers
            answer = ""
            while answer.lower() not in ['y', 'n']:
                answer = input("Previous numbers found, use? (y/n): ")

            if answer.lower() == 'y':
                # Load old numbers
                self.load_previous()
            else:
                # Create a list of new numbers
                self.create_new_numbers()
        else:
            # Create new if previous don't exist
            self.create_new_numbers()

        # After creating or loading, save SAP numbers to file
        with open(Config.get_saves_file(), 'w') as sap_numbers_file:
            sap_numbers_file.write("\n".join(self.numbers))
            print("SAP numbers updated to file. ")

    def previous_exist(self):
        """ Checks if the previous SAP numbers exist,
            if yes, asks user if use them, if not, automatically
            ask to add sap numbers """
        sap_numbers = []
        try:
            with open(Config.get_saves_file(), 'r') as sap_numbers_file:
                sap_numbers = sap_numbers_file.read().split()
        except FileNotFoundError:
            # Sap number file doesn't exist, create it
            with open(Config.get_saves_file(), 'w') as sap_numbers_file:
                sap_numbers_file.write('')

        return bool(len(sap_numbers))

    def create_new_numbers(self):
        # Clear a list
        self.numbers.clear()

        # User adds various numbers until hits an empty line
        user_input = None

        while user_input != "":
            # List already saved numbers
            if self.sap_numbers_count():
                print(f"Saved {self.sap_numbers_count()} numbers:")
                for sap_count, number in enumerate(self.numbers):
                    print(f"{sap_count + 1}: {number}")
            else:
                # If the list of SAP numbers is empty, tell that to user
                print("So far no SAP numbers saved.")

            # User input
            user_input = input("Enter a SAP number (enter for finish): ")

            # Save number
            if user_input:
                self.create_number(user_input)

    def create_number(self, number):
        """ Creates a new sap number """
        self.numbers.append(number)

    def sap_numbers_count(self):
        """ Returns a count of SAP numbers saved """
        return len(self.numbers)

    def load_previous(self):
        """ Loads previously saved SAP number file and create a list """
        self.numbers.clear()
        with open(Config.get_saves_file(), 'r') as sap_numbers_file:
            self.numbers = sap_numbers_file.read().split()

    def edit_previous(self):
        pass


# RUNTIME #
def main():
    """ Main runtime """

    ## Main workflow ##

    # Load previously saved numbers
    sap_numbers = SAPNumbers()

    # Ask user if do distribution for current month or different

    # Ask user how many days ommit (vacation, public holiday) in given month
    # Or better solution, which day numbers to omit (e.g. 17 for November)

    # Ask user how many hours to distribute

    # Load calendar for that month

    # Compute for all remanining (not holidays/vacation) workdays

    # Generate CSV (could be easily opened in Excel or something and copied to SAP)
    # Experiment with text file, values divided by \t or something like that


if __name__ == "__main__":
    main()
