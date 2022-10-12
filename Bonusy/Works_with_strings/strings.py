"""
    Use text: https://www.gutenberg.org/files/1342/1342-0.txt


"""
# IMPORTS #
import urllib.request
import sys


# CLASSES #
class Word:
    def __init__(self, word):
        self.word = word
        self.length = len(word)
        self.letters = dict()

        self.process_letters()

    def process_letters(self):
        for letter in str(self.word):
            if letter in self.letters:
                self.letters[letter] += 1
            else:
                self.letters[letter] = 1
            

class Text:
    def __init__(self):
        self.path = "https://www.gutenberg.org/files/1342/1342-0.txt"
        self.text = str()

        self.read_file()

        self.words = []

        self.processed_words = []

    def read_file(self):
        file = urllib.request.urlopen(self.path)
        self.text = file.read()
        print(f"{int(len(self.text) / 1024 + 1)}kB file loaded.")

    def print_file(self):
        print(self.text)

    def process_file(self):
        self.words = self.text.split()
        print(f"Processing {len(self.words)} words...")

        for counter, word in enumerate(self.words):
            self.processed_words.append(Word(word))

        print(f"Done, {len(self.words)} words processed.")


# RUNTIME #
def main():
    text = Text()
    text.process_file()


if __name__ == "__main__":
    main()
