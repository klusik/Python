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
                 month = None):
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


        # Runtime
        if self.previous_exist():
            # Aski if use
            answer = ""
            while answer.lower() not in ['y', 'n']:
                answer = input("Previous numbers found, use? (y/n): ")

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

    def load_previous(self):
        pass

    def edit_previous(self):
        pass



# RUNTIME #
def main():
    """ Main runtime """

    ## Main workflow ##

    # Load previously saved numbers
    sap_numbers =SAPNumbers()

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