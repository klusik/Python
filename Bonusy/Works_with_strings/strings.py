"""
    Use text: https://www.gutenberg.org/files/1342/1342-0.txt


"""
# IMPORTS #
import urllib.request

# CLASSES #
class Word:
    pass


class Text:
    def __init__(self):
        self.path = "https://www.gutenberg.org/files/1342/1342-0.txt"
        self.text = str()

        self.read_file()

    def read_file(self):
        file = urllib.request.urlopen(self.path)
        self.text = file.read()

    def print_file(self):
        print(self.text)

    def process_file(self):
        pass





# RUNTIME #
def main():
    text = Text()
    text.process_file()


if __name__ == "__main__":
    main()