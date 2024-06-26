"""
    Generate sentences in random fake language

    TODO:
        -   add sentence syntax model
        -   add letters probabilities
        -   create class for letter probabilities
        -   configure smartgit

    Author: Rudolf Klusal
    Year: 2023
"""

# IMPORTS #
import random


# EXCEPTIONS #
class BadLetterTypeError(TypeError):
    """Exception raised when a letter provided is not a string or of invalid length."""

    def __init__(self, letter: str):
        self.letter = letter
        self.message = f"{letter} is not a valid letter. Letters must be strings of length 1."
        super().__init__(self.message)


class BadSyllableTypeError(TypeError):
    """Exception raised when a syllable provided is not a string or of invalid length."""

    def __init__(self, syllable: str):
        self.syllable = syllable
        self.message = f"{syllable} is not a valid syllable. Syllables must be strings."
        super().__init__(self.message)


# CLASSES #
class Article:
    pass


class Paragraph:
    pass


class Alphabet:
    """ Frequency of characters in common English """
    char_frequency = {
        'e': 12.02,
        't': 9.10,
        'a': 8.12,
        'o': 7.68,
        'i': 7.31,
        'n': 6.95,
        's': 6.28,
        'r': 6.02,
        'h': 5.92,
        'd': 4.32,
        'l': 3.98,
        'u': 2.88,
        'c': 2.71,
        'm': 2.61,
        'f': 2.30,
        'y': 2.11,
        'w': 2.09,
        'g': 2.03,
        'p': 1.82,
        'b': 1.49,
        'v': 1.11,
        'k': 0.69,
        'x': 0.17,
        'q': 0.11,
        'j': 0.10,
        'z': 0.07,
    }

    @classmethod
    def get_sum_frequency(cls) -> float:
        return sum(cls.char_frequency.values())

    @classmethod
    def get_max_frequency(cls) -> float:
        return max(cls.char_frequency.values())

    @classmethod
    def get_normalized_frequencies(cls):
        normalized_chars = cls.char_frequency

        # Ratio would be 1 : max_value from character dict
        ratio = 1 / cls.get_max_frequency()

        return {
            # Create a tuples from items(), values save to letter and value and
            # create a dict, where key is a letter and value is a value multiplied
            # by ratio calculated before.
            letter : value * ratio for letter, value in cls.char_frequency.items()
        }


class Syntax:
    """ Hanldes various syntaxes from which could be generated various sentences

        -   subject: s
        -   predicate: p
        -   object: o
        -   adjectival specification: d
        -   complement: c
        -   adjective: a
    """

    # Usable syntaxes and probabilities of usage. Probabilities from 0 to 1.
    available_syntaxes = {
        "sp": 0.3,  # Short sentences Dog walks. Mum bakes. He drives. I fly.
        "spo": 0.4,  # Short sentence with object: I fly planes. Mum bakes a quiche.
        "spao": 0.5,  # Verbose version of 'spo' -- mum bakes a nice quiche.
        "pso": 0.4,  # Basic question: bake mum a quiche?
        "psao": 0.5,  # more full sentence, bake mum a nice quiche?
    }


class Mark:
    """ Marks and their priority

        Priority a number from 0 to 1

    """
    marks = {
        '.': 0.8,
        '?': 0.2,
        '!': 0.05,
    }


class Sentence:
    """
    A class representing a sentence, consisting of a list of words and a sentence ending.
    The sentence can be between 2 and 8 words long and can end with either a dot, question mark,
    exclamation mark, or comma.
    """

    def __init__(self,
                 dictionary=None, # If defined, it uses dictionary
                 syntax=None, # If defined, it uses predefined syntax
                 ):
        # Sentence lengths: 2--8 words
        self.sentence_length = random.randint(2, 8)

        # Sentence ending: dot, question mk., exclamation mk. Comma
        self.sentence_endings = ['.', '?', '!', ',']
        self.sentence_ending: str = str(random.choice(self.sentence_endings))

        # Generate sentence
        self.sentence: list[Word] = self.make_sentence()

    def __str__(self):
        """
        Returns a string representation of the sentence.
        """
        return self.get_text()

    def get_text(self):
        """
        Returns the sentence as a concatenated string, with the first word capitalized and
        the sentence ending added.

        Returns:
        str: The letter
        """
        return str(" ".join(map(str, self.sentence))).capitalize() + self.sentence_ending + ' '

    def make_sentence(self,
                      syntax_format=None,  # If specified, use specific syntax
                      ) -> list:
        """
        Creates a list of words to form a sentence.
        """
        sentence: list[Word] = []

        for _ in range(self.sentence_length):
            sentence.append(Word())

        return sentence


class Word:
    """ Class handling words from Syllables

        Words could be 1, 2 or 3 syllables long.

        Words could be complemented from more words, but that should be done from top level
        from Sentence class.
    """

    def __init__(self):
        # Set up word
        self.word_lengths = [1, 2, 3]

        self.word_length = random.choice(self.word_lengths)

        # Create word
        self.word: list[Syllable] = self.make_word()

    def __str__(self):
        return self.get_text()

    def __add__(self, other: 'Word'):
        return str(self.get_text() + other.get_text().capitalize())

    def get_text(self) -> str:
        """
        Get the word

        Returns:
        str: The word
        """

        return ''.join(map(str, self.word))

    def make_word(self) -> list:
        """ Makes a word of 1, 2 or 3 syllables """
        word: list[Syllable] = []

        for _ in range(self.word_length):
            word.append(Syllable())

        return word


class Syllable:
    """
    Class representing a syllable in a word.

    A syllable could have the following forms:

        - Consonant + Vowel (cv)
        - Consonant + Vowel + Vowel (cvv)
        - Consonant + Vowel + Consonant (cvc)
    """

    def __init__(self):
        # Possible syllable forms
        self.forms = ['cv', 'cvv', 'cvc']

        # Choose a random form for this syllable
        self.form = random.choice(self.forms)

        # Generate the syllable
        self.syllable = self.make_syllable()

    def __str__(self):
        return self.get_text()

    def __add__(self, other: 'Syllable') -> str:
        return self.get_text() + other.get_text()

    def get_text(self) -> str:
        """
        Get syllable

        Returns:
        str: The syllable
        """
        return ''.join(map(str, self.syllable))

    def make_syllable(self) -> list:
        syllable: list = []

        for letter_type in self.form:
            if letter_type == 'c':
                syllable.append(Letter(letter_type='consonant'))
            elif letter_type == 'v':
                syllable.append(Letter(letter_type='vowel'))
            else:
                raise BadSyllableTypeError(f"Invalid syllable form: {self.form}")

        return syllable


class Letter:
    """
    Class representing a single letter, can be either a vowel, consonant or a random letter
    """

    def __init__(self, letter_type: str = None):
        """
        Initialize the class and create the letter

        Args:
        letter_type (str): Type of letter to create, either 'vowel', 'consonant' or None for random letter
        """
        # All letters in the English alphabet
        self.__letter_pool: str = "abcdefghijklmnopqrstuvwxyz"

        # All vowels in the English alphabet
        self.__vowel_pool: str = "aeiouy"

        # Create consonants by removing vowels from letter_pool
        self.__consonant_pool: str = self.__letter_pool
        for char in self.__vowel_pool:
            self.__consonant_pool = self.__consonant_pool.replace(char, '')

        # Variable to store the resulting letter
        self.__letter: str = ""

        # Check if letter type is specified
        if letter_type:
            # Type specified
            if letter_type == "vowel":
                # Choose a random vowel from vowel_pool
                self.__letter = random.choice(self.__vowel_pool)
            elif letter_type == "consonant":
                # Choose a random consonant from consonant_pool
                self.__letter = random.choice(self.__consonant_pool)
            else:
                # Raise an error if letter_type is not 'vowel' or 'consonant'
                raise BadLetterTypeError("letter_type must be either 'vowel' or 'consonant'")
        else:
            # None specified, choose a random letter from letter_pool
            self.__letter = random.choice(self.__letter_pool)

    def __str__(self) -> str:
        """
        Override the default string representation of the class

        Returns:
        str: The letter
        """
        return self.__letter

    def __add__(self, other: 'Letter') -> str:
        """
        Override the addition operator to concatenate two letters

        Args:
        other (Letter): Another instance of the Letter class

        Returns:
        str: The concatenated letters
        """
        return str(self.get_letter() + other.get_letter())

    def get_letter(self) -> str:
        """
        Get the letter

        Returns:
        str: The letter
        """
        return self.__letter

    def get_vowel(self) -> str:
        """
        Get a random vowel

        Returns:
        str: A random vowel
        """
        return random.choice(self.__vowel_pool)

    def get_consonant(self) -> str:
        """
        Get a random consonant

        Returns:
        str: A random consonant
        """
        return random.choice(self.__consonant_pool)


# RUNTIME #
def main():
    # Tests

    for _ in range(2):
        sentence = Sentence()
        print(sentence, end='')

    print()

    print(Alphabet.get_normalized_frequencies())


if __name__ == "__main__":
    main()
