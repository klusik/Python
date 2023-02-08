"""
    Generate sentences in random fake language

    Author: Rudolf Klusal
    Year: 2023
"""

# IMPORTS #
import random


# EXCEPTIONS #
class BadLetterTypeError(Exception):
    pass


class BadSyllableTypeError(Exception):
    pass


# CLASSES #
class Marks:
    """ Marks and their priority

        Priority a number from 0 to 1

    """
    marks = {
        '.': 0.8,
        '?': 0.2,
        '!': 0.05,
    }


class Sentence:
    """ Create the whole sentence from words """

    def __init__(self):
        # Sentence lengths: 2--8 words
        self.sentence_length = random.randint(2, 8)

        # Sentence ending: dot, question mk., exclamation mk. Comma
        self.sentence_endings = ['.', '?', '!']
        self.sentence_ending: str = str(random.choice(self.sentence_endings))

        # Generate sentence
        self.sentence: list[Word] = self.make_sentence()

    def __str__(self):
        return self.get_text()

    def get_text(self):
        return str(" ".join(map(str, self.sentence))).capitalize() \
            + self.sentence_ending + ' '

    def make_sentence(self) -> list:
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
        return ''.join(map(str, self.word))

    def make_word(self) -> list:
        word: list[Syllable] = []

        for _ in range(self.word_length):
            word.append(Syllable())

        return word


class Syllable:
    """
        Syllables could be found in forms:

        Consonants (c) and vowels (v):

            Form 1: cv
            Form 2: cvv
            Form 3: cvc
    """

    def __init__(self):
        letter = Letter()

        # Forms of syllables
        self.forms = [
            'cv',  # cu mu xi fa ba by
            'cvv',  # lea mey xiu fau fue
            'cvc',  # let meg gem bat
        ]

        # Get random syllable
        self.form = random.choice(self.forms)

        # Generate a syllable
        self.syllable = self.make_syllable()

    def __str__(self):
        return str(self.get_text())

    def __add__(self, other: 'Syllable') -> str:
        return str(self.get_text() + other.get_text())

    def get_text(self) -> str:
        return ''.join(map(str, self.syllable))

    def make_syllable(self) -> list:
        syllable: list[Letter] = list()

        for syllable_type in self.form:
            if syllable_type == 'c':
                syllable.append(Letter(letter_type='consonant'))
            elif syllable_type == 'v':
                syllable.append(Letter(letter_type='vowel'))
            else:
                raise BadSyllableTypeError

        return syllable


class Letter:
    def __init__(self,
                 letter_type=None,  # vowel, consonant or None
                 ):
        self.__letter_pool: str = "abcdefghijklmnopqrstuvwxyz"
        self.__vowel_pool: str = "aeiouy"

        # Create consonants
        self.__consonant_pool: str = self.__letter_pool

        for char in self.__vowel_pool:
            self.__consonant_pool = self.__consonant_pool.replace(char, '')

        # Variable for resulting letter
        self.__letter: str = ""

        if letter_type:
            # Type specified
            if letter_type == "vowel":
                self.__letter = random.choice(self.__vowel_pool)
            elif letter_type == "consonant":
                self.__letter = random.choice(self.__consonant_pool)
            else:
                raise BadLetterTypeError
        else:
            # None specified, would be random letter
            self.__letter = random.choice(self.__letter_pool)

    def __str__(self):
        return self.__letter

    def __add__(self, other: 'Letter'):
        return str(self.get_letter() + other.get_letter())

    def get_letter(self) -> str:
        return self.__letter

    def get_vowel(self) -> str:
        return random.choice(self.__vowel_pool)

    def get_consonant(self) -> str:
        return random.choice(self.__consonant_pool)


# RUNTIME #
def main():
    # Tests

    for _ in range(57):
        sentence = Sentence()
        print(sentence, end='')

    print()


if __name__ == "__main__":
    main()
