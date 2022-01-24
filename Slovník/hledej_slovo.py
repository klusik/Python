""" Search for a word in Czech dictionary
    Seach is based on a letters given as an input
    by user (e.g. 'klsuta' will make words like 'klus', 'lusk' etc.)


"""

# IMPORTS #

# CLASSES #
class Config:
    """ Defaults """
    dictionary_path = "cs_CZ.dic"


class Word:
    def __init__(self, word):
        self.word = word

    def is_real_word(self):
        """ If the word is a real word or just a heading or something """

        # If the given word is only a digit, it's not a word
        if str(self.word).isdigit():
            return False

        # If the word contains ONLY capital letters (not any, ONLY),
        # then it's not a word as well.
        if str(self.word).upper() == str(self.word):
            return False


        return True

    def get_word(self):
        """ Words could contain a forward slash and grammar case and other stuff
            in that, so if that's the case, return just a word before that. """
        return str(self.word).split("/")[0]

class Dictionary:
    """Class contains the dictionary stuff """
    def __init__(self):

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

        all_words = set()

        for line_from_file in list_of_all_words_from_file:
            word = Word(line_from_file)

            if word.is_real_word():
                all_words.add(word.get_word())

            # Clear the memory
            del(word)

# RUNTIME #
def main():
    """ Main runtime"""
    dictionary = Dictionary()

    dictionary.load_dictionary_from_file()


if __name__ == "__main__":
    main()