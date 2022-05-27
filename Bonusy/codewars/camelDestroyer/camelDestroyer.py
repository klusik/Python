"""

    CW: https://www.codewars.com/kata/5208f99aee097e6552000148/train/python

    Complete the solution so that the function will break up camel casing, using a space between words.

    Example
    "camelCasing"  =>  "camel Casing"
    "identifier"   =>  "identifier"
    ""             =>  ""
"""

# RUNTIME #
def solution(input_text):
    """ Stupid name for a function, but need to give it back to CW """

    # Create a new string
    decamelized = ""

    for letter in input_text:
        # Going through all letters, if a letter is CAPITAL letter,
        # just insert a space before
        if letter.isupper():
            decamelized += f" {letter}"
        else:
            decamelized += letter

    return decamelized

if __name__ == "__main__":
    input_text = str(input("Enter the camelcased identifier: "))

    print(solution(input_text))
