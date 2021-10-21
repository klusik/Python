# Objects test
#
# The goal is to test a object oriented stuff in Python, 
# basic principles

# IMPORTS

from urllib.request import urlopen

class Characters:
    """Characters from the webpage"""
    def __init__(self):
        self.characters = dict()
        self.url = "http://wikipedia.cz"

    def notConsists(self, character):
        return character not in self.characters

    def addNewCharacter(self, character):
        self.characters[character] = 1

    def addExistingCharacter(self, character):
        self.characters[character] += 1

    def getAllCharacters(self):
        return dict(sorted(self.characters.items(), key = lambda item: item[1], reverse = True))

def main():

    # Creating an instance
    characters = Characters()

    # Reading a file

    webRead = urlopen(characters.url)
    webContent = str(webRead.read())


    # Going through all the characters
    for character in webContent:
        if characters.notConsists(character):
            characters.addNewCharacter(character)
        else:
            characters.addExistingCharacter(character)

    # Get all characters
    allCharacters = characters.getAllCharacters()


    # Get it out
    print(f"All characters from {characters.url}: ")
    for character in allCharacters:
        print(f"{character}: {allCharacters[character]}")

if __name__ == "__main__":
    main()