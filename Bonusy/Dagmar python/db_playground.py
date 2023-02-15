"""
    Playground for MySQL stuff

    Author:     R. Klusal
    Year:       2023
"""

# IMPORTS #
import sqlite3


# CLASSES #
class ViewUsers:
    """A class representing a view of users in a database."""

    # Define a dictionary to map user attributes to their corresponding column names in the database.
    users_table = {
        'user_id': 'id_lidi',
        'name': 'jmeno',
        'surname': 'prijmeni',
        'year': 'rok_narozeni',
        'table': 'lidi',
    }

    @classmethod
    def __init__(cls,
                 order_by=None,  # Optional parameter to specify the column to order the results by.
                 order=None,  # Optional parameter to specify the order in which to sort the results.
                 ):
        """
        Initializes the ViewUsers class.

        Args:
        - order_by: Optional. The column to order the results by.
        - order: Optional. The order in which to sort the results.
        """
        # If the order_by parameter is provided, add it to the users_table dictionary.
        if order_by:
            cls.users_table['order_by'] = order_by

        # If the order parameter is provided, add it to the users_table dictionary.
        if order:
            cls.users_table['order'] = order

    @classmethod
    def __str__(cls):
        # Create initial string with column names and table name for SELECT query
        output_str = f"SELECT " \
                     f"{cls.users_table['user_id']}," \
                     f"{cls.users_table['name']}, " \
                     f"{cls.users_table['surname']}," \
                     f"{cls.users_table['year']}" \
                     f" FROM " \
                     f"{cls.users_table['table']}"

        # Check if 'order_by' key exists in users_table dictionary
        if 'order_by' in cls.users_table.keys():
            # Get the corresponding column name from the dictionary using the 'order_by' key
            order_by_key = cls.users_table[cls.users_table['order_by']]
            # Add ORDER BY clause to the query with the corresponding column name
            output_str += f" ORDER BY {order_by_key}"

        # Check if both 'order' and 'order_by' keys exist in users_table dictionary
        if {'order', 'order_by'}.issubset(cls.users_table.keys()):
            # Add the sorting order to the query
            output_str += f" {cls.users_table['order']}"

        # Return the final string as a string object
        return str(output_str)


class DB:
    """ Class containing all DB methods """

    def __init__(self):
        """ Connects automatically """

        # Open db file
        self.db_conn = sqlite3.connect('db_kls.db')

        # Check DB and initialize if not ready
        self.__init_db()

    def __init_db(self):
        """ Init tables if not exist """
        db_cursor = self.db_conn.cursor()
        tables = db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()

        if len(tables) == 0:
            # Tables don't exist at all
            print("Empty DB, initializing DB...")

            try:
                with open('default_db.sql', 'r', encoding='utf8') as f_init_query:
                    init_query = f_init_query.read()

            except FileNotFoundError as err:
                print(f"Necessary file not found, exiting program: {str(err)}")
                exit(3)

            except sqlite3.Error as err:
                print(f"Sqlite error: {str(err)}")
                exit(4)

            except IOError as err:
                print(f"I/O error: {str(err)}")
                exit(5)

            # Creating a default structure
            for row in str(init_query).split(';'):
                db_cursor.execute(row)
                self.db_conn.commit()

    @staticmethod
    def __get_db_credentials() -> dict:
        """ Returns dict with login credentials """

        # Output dict
        credentials = dict()

        try:
            with open('db_info.dat', 'r') as f_db:
                f_data = str(f_db.read()).split('\n')

            for row in f_data:
                credentials[str(row).split(':')[0]] = str(row).split(':')[1]

            return credentials

        except FileNotFoundError:
            # If file not found
            print(f"Config file not found, exiting.")
            exit(1)

        except IndexError:
            # Probably an issue with data file
            print(f"Config file corrupted, exiting.")
            exit(2)

    # Data methods #
    def get_users(self,
                  filter=None,
                  ) -> list:
        """ Returns users """

        # DB cursor
        db_cursor = self.db_conn.cursor()

        # SQL query string
        sql_get_users = str(ViewUsers(order_by='surname', order='desc'))

        # Retrieve data
        users_data = db_cursor.execute(sql_get_users).fetchall()

        return users_data


# RUNTINE #
def main():
    db = DB()

    print(db.get_users())


if __name__ == "__main__":
    main()
