"""
    Default home-finance budget app
    just for training purposes (Pyladies)

    # Goal: #
    *   Add/remove finances to/from your personal wallet
    *   Add/remove finances to/from your personal account
    *   Savings

    # Additional goals: #
    *   Guess proffits over longer periods of time into the future

"""


# CLASSES #
class Config:
    DATA_FILE_NAME = "data.kls"


class Bank:
    pass


class Wallet:
    pass

class Budget:
    def __init__(self,
                 filename=None,
                 ):
        # Load default data

        self.load_data(filename)

    def load_data(self,
                  filename:str = None,
                  ) -> dict:
        """

        :rtype: dict
        :param filename: String with a file name (optional)
        """

        # Using the default name value
        if not filename:
            filename = Config.DATA_FILE_NAME

        data:str = ""

        try:
            # Create a file if not exist
            with open(filename, 'a') as fData:
                pass

            # Read the file
            with open(filename, 'r') as fData:
                data = fData.read()

        except FileNotFoundError:
            print(f"File {filename} can't be accessed!")
            raise FileNotFoundError

        finally:
            # Everything went well
            # Return a datastructure
            pass

# RUNTIME #
def main():
    budget = Budget()


if __name__ == "__main__":
    main()
