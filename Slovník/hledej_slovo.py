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


    def load_dictionary_from_file(self,
                                  file = Config.dictionary_path):
        """ Populates a dictionary from a file """

        with open(file, 'r', encoding='UTF-8') as f_dictionary:
            file_content = f_dictionary.read()
            f_dictionary.close()

        list_of_all_words_from_file = file_content.split()

        # It's necessary, the first line contains only a number of words in list
        num_of_words_check = int(list_of_all_words_from_file.pop(0))
        num_of_words = len(list_of_all_words_from_file)

        if num_of_words_check == num_of_words:
            print(f"Načteno {num_of_words} položek.")
        else:
            print(f"Načteno {num_of_words} položek, ale slovník tvrdí, "
                  f"že jich obsahuje {num_of_words_check}. ")

        # Some words contains only CAPITALLETTERS, these are not words,
        # these are headers of sections, like 'ABB'




# RUNTIME #
def main():
    """ Main runtime"""
    dictionary = Dictionary()

    dictionary.load_dictionary_from_file()


if __name__ == "__main__":
    main()