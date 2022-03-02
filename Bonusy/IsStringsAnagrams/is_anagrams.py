"""
    Script compares two strings if they are anagrams :-)

    Author: klusik@klusik.cz
"""

# CLASSES #
class Words:
    def __init__(self,
                 string_1, string_2):
        self.string_1 = string_1
        self.string_2 = string_2

    def is_anagram(self):
        """ Returns true if anagram """
        if len(self.string_1) == len(self.string_2):
            if ''.join(sorted(self.string_1)) == ''.join(sorted(self.string_2)):
                return True
            else:
                return False
        else:
            return False

# RUNTIME #
def main():
    string_1 = str(input("Enter the first string: "))
    string_2 = str(input("Enter the second string: "))

    words = Words(string_1, string_2)

    if words.is_anagram():
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()