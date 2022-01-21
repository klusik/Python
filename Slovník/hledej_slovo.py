""" Search for a word in Czech dictionary
    Seach is based on a letters given as an input
    by user (e.g. 'klsuta' will make words like 'klus', 'lusk' etc.)


"""

# IMPORTS #

# CLASSES #
class Config:
    """ Defaults """
    dictionary_path = "cs_CZ.dic"

    
class Dictionary:
    """Class contains the dictionary stuff """
    def init(self):

        # ATTRIBUTES #
        self.dictionary = dict()    # Contains all words


    def load_dictionary_from_file(self):
        """ Populates a dictionary from a default file """



# RUNTIME #
def main():
    """ Main runtime"""

if __name__ == "__main__":
    main()