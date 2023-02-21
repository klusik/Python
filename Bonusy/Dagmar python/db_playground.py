"""
    Playground for MySQL stuff

    Author:     R. Klusal
    Year:       2023
"""

# IMPORTS #
import sqlite3


# CLASSES #
class ViewUsers:
    """ View for users """
    user_id = 'id_lidi'
    name = 'jmeno'
    surname = 'prijmeni'
    year = 'rok_narozeni'
    table = 'lidi'

    @classmethod
    def __str__(cls):
        return str(f"SELECT "
                   f"{cls.user_id},"
                   f"{cls.name}, "
                   f"{cls.surname},"
                   f"{cls.year}"
                   f" FROM "
                   f"{cls.table}")


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

            except FileNotFoundError:
                print(f"Necessary file not found, exiting program.")
                exit(3)

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
        sql_get_users = str(ViewUsers())

        # Retrieve data
        users_data = db_cursor.execute(sql_get_users).fetchall()

        return users_data


# RUNTINE #
def main():
    db = DB()

    print(db.get_users())


if __name__ == "__main__":
    main()
