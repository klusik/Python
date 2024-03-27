"""
    Home Finances

    Pyladies 2024 / jarní kurz
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
        # Load data from file, create a file if not exist
        self._json_data = self._load_data_from_file()
        self.json_sync()


    def _load_data_from_file(self, file=None) -> dict:
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

            self._json_data = finaces_data
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

        if 'incomes' not in self._json_data:
            self._json_data['incomes'] = []

        if 'expenses' not in self._json_data:
            self._json_data['expenses'] = []

        # Update the file
        try:
            with open(Config.data_file(), 'w', encoding=Config.default_encoding()) as f_json:
                json.dump(self._json_data, f_json, ensure_ascii=False, indent=Config.json_indent())

        except json.JSONDecodeError as json_err:
            logging.error("Error during updating the data file.\n", str(json_err))

    def add_income(self, income: float, income_description: str) -> bool:
        """
        Adds an income to the list
        :param income: Income value (Float)
        :param income_description: Income descritpion (String)
        :return: True if success
        :rtype: bool
        """

        # Ensure there's a key 'income' in the json file
        if 'incomes' not in self._json_data:
            # Create empty income
            self._json_data['incomes'] = []

        # Add new income
        self._json_data['incomes'].append(
            {
                "amount": income,
                "description": income_description,
                "date": datetime.datetime.now().strftime("%d. %m. %Y"),
            }
        )

        # Update the file
        self.json_sync()

    def add_expense(self, expense: float, expense_description: str) -> bool:
        """
        Updates the JSON file with a new expense
        :param expense: Float value of expense
        :param expense_description: String description
        :return: True if success
        :rtype: bool
        """

        # Ensure expenses are in
        if not 'expenses' in self._json_data:
            self._json_data['expenses'] = []

        # Adding expense
        self._json_data['expenses'].append(
            {
                "amount": expense,
                "description": expense_description,
                "date": datetime.datetime.now().strftime("%d. %m. %Y"),
            }
        )

        # Update the file
        self.json_sync()

    def print_list(self) -> None:
        """
        Prints the list from loaded JSON file
        :return: None
        """
        self.print_incomes()
        self.print_total('incomes')

        self.print_expenses()
        self.print_total('expenses')

        self.print_total()

    def print_total(self, mode=None) -> float:
        """
        Print total amount of expenses, incomes or both
        :param mode: Mode is either None, 'incomes' or 'expenses'
        :return: Float value of total sum
        :rtype: float
        """

        # Sync all data
        self.json_sync()

        # What mode selected
        if mode in ['incomes', 'expenses', None]:
            if mode == 'incomes':
                sum_amount = sum([amount['amount'] for amount in self._json_data['incomes']])
                print(f"Total sum of incomes: {sum_amount}")
                return sum_amount

            elif mode == 'expenses':
                sum_amount = sum([amount['amount'] for amount in self._json_data['expenses']])
                print(f"Total sum of expenses: {sum_amount}")
                return sum_amount

            elif not mode:
                sum_amount = (
                    sum([amount['amount'] for amount in self._json_data['incomes']])
                    - sum([amount['amount'] for amount in self._json_data['expenses']])
                )
                print(f"Total income/expense: {sum_amount}")
                return sum_amount

            else:
                print('Invalid mode')
                return False

    def print_incomes(self) -> None:
        """
        Prints only incomes
        :return: None
        """

        print("Income list\n{:<15} {:<15} {}".format("Date", "Amount", "Description"))
        for income in self._json_data['incomes']:
            print("{:<15} {:>15} {}".format(income['date'], income['amount'], income['description']))

    def print_expenses(self) -> None:
        """
        Prints only expenses
        :return: None
        """
        print("Expense list\n{:<15} {:<15} {}".format("Date", "Amount", "Description"))
        for expense in self._json_data['expenses']:
            print("{:<15} {:>15} {}".format(expense['date'], expense['amount'], expense['description']))


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

                continue

            # Exit
            if user_input.lower() == 'exit':
                exit()

            # List the income and expenses
            if user_input.lower() == 'list':
                app.print_list()
                continue

            # Add income
            if user_input.lower() == 'add':
                income_desc = input("Enter the description of this income: ")
                income_value = float(input("Enter the income: "))

                app.add_income(income_value, income_desc)
                continue

            if user_input.lower() == 'pay':
                expense_desc = input("Enter the description of the expense: ")
                expense_amount = float(input("Enter the expense: "))

                app.add_expense(expense_amount, expense_desc)

    except KeyboardInterrupt as kbd_intr:
        exit()


if __name__ == "__main__":
    main()
