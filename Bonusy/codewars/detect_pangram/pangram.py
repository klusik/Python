"""
    Detect pangram
    CW: https://www.codewars.com/kata/545cedaa9943f7fe7b000048/train/python
"""


def is_pangram(input_string: str) -> bool:
    """
        Detect if input string is a pangram

        A pangram is a sentence that contains every single letter
        of the alphabet at least once.

        For example, the sentence "The quick brown fox jumps over the lazy dog"
        is a pangram, because it uses the letters A-Z at least once (case is irrelevant).

        Given a string, detect whether it is a pangram.
        Return True if it is, False if not.
        Ignore numbers and punctuation.

        :rtype: bool
        :param input_string: String to test
    """
    alphabet = set(map(chr, range(97, 123)))
    input_set = set(input_string.lower())
    if ' ' in input_set:
        input_set.remove(' ')
    return alphabet.issubset(input_set)


if __name__ == "__main__":
    test_string = "The quick brown fox jumps over the lazy dog"
    input_string = input("Enter some text: ")
    if input_string:
        test_string = input_string

    print(f"String: {test_string}\nresult: {is_pangram(test_string)}.")
