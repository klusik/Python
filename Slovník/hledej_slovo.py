""" Search for a word in Czech dictionary
    Seach is based on a letters given as an input
    by user (e.g. 'klsuta' will make words like 'klus', 'lusk' etc.)

    @author:    klusik@klusik.cz
    @year:      2022
"""


# IMPORTS #

# CLASSES #
class Config:
    """ Defaults """

    # Path to dictionary
    dictionary_path = "cs_CZ.dic"

    # Default minimal lenght of a word
    word_min_length = 3


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
        # self.dictionary = dict()    # Contains all words
        self.all_words = set()  # Contains all words

    def print_words(self, filter=None):
        if filter:
            # Display a words based on the filter
            if filter.isalpha():
                # We're in

                # In these fixed_positions there'll be (if any)
                # indexes of final word, where the fixed letters
                # would be. This list can be empty, if no capital
                # letters will be provided.
                fixed_positions = list()

                # Find capital letters, other letters and make a filter from them
                for filter_char_index, filter_char in enumerate(filter):
                    if str(filter_char).isupper():
                        # Save a position
                        # It's not necessary to save the letter, the index
                        # is enough.
                        fixed_positions.append(filter_char_index)

                # Guessing the minimal lenght of a word from the saved indexes
                # If no saved or only on the first position, assuming minimal
                # length of 3 letters for a word

                if fixed_positions.count() > 0:
                    # guessing from the indeces
                    self.word_min_length = max(fixed_positions) + 1
                else:
                    # setting the default vaule
                    self.word_min_length = Config.word_min_length

            else:
                # It shouldn't happen, but here we are :-)
                print("Špatný formát filtru.")
        else:
            # Display all words in dictionary
            for word_index, word in enumerate(self.all_words):
                print(word_index, word)

    def load_dictionary_from_file(self,
                                  file=Config.dictionary_path):
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

        for line_from_file in list_of_all_words_from_file:
            word = Word(line_from_file)

            if word.is_real_word():
                self.all_words.add(word.get_word())

            # Clear the memory
            del (word)

        # Sorting alphabetically
        self.all_words = sorted(self.all_words)


# RUNTIME #
def main():
    """ Main runtime"""
    dictionary = Dictionary()

    dictionary.load_dictionary_from_file()

    while True:
        search_pattern = str(input("Zadejte množinu znaků, ze kterých čerpat. \n"
                                   "Velkými písmeny označíte přímo pozici znaku, \n"
                                   "např. Pabcd vyhledá všechny kombinace znaků 'pabcd' tak, \n"
                                   "že znak 'p' bude na prvním místě. Pokud zadáte pouze prázdný řetězec, \n"
                                   "zobrazí se seznam všech slov ve slovníku.\n\nZadejte množinu znaků: "))

        if search_pattern.isalpha():
            dictionary.print_words(filter=search_pattern)
            break

        if search_pattern == "":
            dictionary.print_words()
            break


if __name__ == "__main__":
    main()
