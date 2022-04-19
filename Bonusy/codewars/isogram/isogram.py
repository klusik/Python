"""
An isogram is a word that has no repeating letters, consecutive or non-consecutive.
Implement a function that determines whether a string that contains only letters is an isogram.
Assume the empty string is an isogram. Ignore letter case.

Example: (Input --> Output)

"Dermatoglyphics" --> true
"aba" --> false
"moOse" --> false (ignore letter case)

"""

# RUNTIME #

def is_isogram(input_string = ""):
    """ Returns True / False """

    # My approach would be using dict with keys for every letter,
    # everything should be there only once

    histogram = dict()

    for character in input_string.lower():
        if input_string.lower().count(character) > 1:
            return False

    # Everything only once
    return True


if __name__ == "__main__":
    """ Main runtime """

    if is_isogram(str(input("Enter a word: "))):
        print("Yes, it's an isogram.")
    else:
        print("Nope, not an isogram.")