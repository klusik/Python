"""
    Home Finances

    Pyladies 2024 / jarní kurz
    v1 by Klusik
    
"""

# IMPORTS #
import json
import datetime
import logging

from pathlib import Path

from src.config import Config


# CLASSES #
class App:
    def __init__(self):
        self.ftypes = ['incomes', 'expenses']
        # Load data from file, create a file if not exist
        self._json_data = self._load_data_from_file()
        self.json_sync()
        

    @staticmethod
    def _load_data_from_file(file=None) -> dict:
        """
        Loads data from a data file
        :param file: File name to access
        :return: Dictionary with structured data
        :rtype: dict
        """
        if not file:
            file = Config.data_file()

        # Check if such file exist
        file_name = Path(file)
        file_name.parent.mkdir(parents=True, exist_ok=True)
        file_name.touch(exist_ok=True)

        try:
            # Check if empty file, create a valid json structure
            if not file_name.exists() or file_name.stat().st_size == 0:
                with open(file, 'w', encoding=Config.default_encoding()) as f_check_validity:
                    json.dump({}, f_check_validity)

            # Opening such file
            with open(file, 'r', encoding=Config.default_encoding()) as f_data:
                finaces_data = json.load(f_data)

            return finaces_data

        except FileNotFoundError as fnf_err:
            # File with finances data doesn't exist
            logging.error(f"File {file} could not be opened!\n", str(fnf_err))
            exit()

        except json.JSONDecodeError as json_err:
            # File with finances exist, but it's not a valid json file
            logging.error(f"File {file} is not valid data file!\n", str(json_err))
            exit()

    def json_sync(self) -> None:
        """
        Sets the right structure for JSON data file
        :return: None
        """
        for ftypes in self.ftypes:
            if ftypes not in self._json_data:
                self._json_data[ftypes] = []

        # Update the file
        try:
            with open(Config.data_file(), 'w', encoding=Config.default_encoding()) as f_json:
                json.dump(self._json_data, f_json, ensure_ascii=False, indent=Config.json_indent())

        except json.JSONDecodeError as json_err:
            logging.error("Error during updating the data file.\n", str(json_err))
    
    def add_transaction(self, ttype: str, tvalue: float, tdescription: str) -> bool:
        """
        Adds a transaction to the list
        :param ttype: type of transaction (String)
        :param tvalue: transaction value (Float)
        :param tdescription: descritpion (String)
        :return: True if success
        :rtype: bool
        """
        # Add new transaction
        self._json_data[ttype].append(
            {
                "ammount": tvalue,
                "description": tdescription,
                "date": datetime.datetime.now().strftime("%d. %m. %Y"),
            }
        )

        # Update the file
        try:
            with open(Config.data_file(), 'w', encoding=Config.default_encoding()) as f_json:
                json.dump(self._json_data, f_json, ensure_ascii=False, indent=Config.json_indent())

            # Success
            return True

        except json.JSONDecodeError as json_err:
            logging.error("Error during updating the data file.\n", str(json_err))
            return False
        

    def print_list(self) -> None:
        """
        Prints the list from loaded JSON file
        :return: None
        """
        for ftypes in self.ftypes:
            self.print_detail(ftypes)
            self.print_subtotal(ftypes)

        self.print_total()

    def print_subtotal(self, mode=None) -> float:
        """
        Print total ammount of expenses or incomes
        :param mode: Mode is 'incomes' or 'expenses'
        :return: Float value of total sum
        :rtype: float
        """
        if mode in self.ftypes:
            #print(mode)
            sum_ammount = sum([ammount['ammount'] for ammount in self._json_data[mode]])
            print("Total sum of", mode,": {:>9}".format(sum_ammount))
        else:
            sum_ammount = 0
        
        return sum_ammount

    def print_total(self) -> float:
        """
        Print total ammount of expenses and incomes 
        :return: Float value of total sum
        :rtype: float
        """
        
        sum_ammount = (
            sum([ammount['ammount'] for ammount in self._json_data['incomes']])
            - sum([ammount['ammount'] for ammount in self._json_data['expenses']])
        )
        print("Total income/expense: {:>9}".format(sum_ammount))
        return sum_ammount


    def print_detail(self, mode=None) -> None:
        """
        Prints details
        :return: None
        """

        print(mode.capitalize(), "list\n{:<15} {:>15} {}".format("Date", "Ammount", "Description"))
        for ftrans in self._json_data[mode]:
            print("{:<15} {:>15} {}".format(ftrans['date'], ftrans['ammount'], ftrans['description']))
    
    def add_check(self, mode, value, desc) -> bool:
        """
        Check new inputs
        
        :return: True if success
        :rtype: bool
        """                        
        
        try:
            new_value = float(value)
            if new_value > 0:
             
                return True
            else:
                print("Please add the income again, the value needs to be positive")
                return False
            
        except ValueError:
            print("Please add the income again, the income needs to be float value")
            return False
        
        
# RUNTIME #
def main():
    # Create an app instance
    app = App()
    # User input
    try:
        while True:  # Main loop
            # User  input
            user_input = input("Enter the command or 'help' for help: ")

            # Displaying HELP
            if user_input.lower() == 'help':
                print("Display commands: \n"
                      "help:\tDisplays this help\n"
                      "list:\tDisplays the list of income and expenses\n"
                      "income:\tDisplays onle the list of incomes to account\n"
                      "expense:\tDisplays only the list of of expenses\n"
                      "\n"
                      "Account commands: \n"
                      "add:\tAdd some income to the account\n"
                      "pay:\tAdd some expense to the account\n"
                      "delete:\tDeletes some item in a roster\n"
                      "\n"
                      "System commands: \n"
                      "exit:\tExits the program\n"
                      "about:\tDisplays the information about this app.\n")
            
            # Exit
            elif user_input.lower() == 'exit':
                exit()

            # List the income 
            elif user_input.lower() == 'income' or user_input.lower() == 'expense':
                mode=user_input.lower() + 's'
                #print(mode)
                app.print_detail(mode)
                app.print_subtotal(mode)
                
            # List the income and expenses
            elif user_input.lower() == 'list':
                app.print_list()
                
            # Add income
            elif user_input.lower() == 'add':
                income_desc = input("Enter the description of this income: ")
                income_value = input("Enter the income: ")
                if app.add_check('incomes', income_value, income_desc):
                    app.add_transaction('incomes', float(income_value), income_desc)
            #    else:
            #        print("error")

            # Add expense
            elif user_input.lower() == 'pay':
                expense_desc = input("Enter the description of the expense: ")
                expense_value = input("Enter the expense: ")
                if app.add_check('expenses',expense_value, expense_desc):
                    app.add_transaction('expenses', float(expense_value), expense_desc)
            #    else:
            #        print("error")
 
            # delete row MISSING CODE
            elif user_input.lower() == 'delete':
                print("Awaiting development")
                # Sync all data
                self.json_sync()
                continue
            
            elif user_input.lower() == 'about':
                print("Developed by: Klusik\n"
                      "Modified by: Wendy")              

            else:
                print("Please use 'help' for more details")

    except KeyboardInterrupt as kbd_intr:
        exit()


if __name__ == "__main__":
    main()
