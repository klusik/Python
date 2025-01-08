"""
    CW: https://www.codewars.com/kata/5629db57620258aa9d000014/train/python

    Author: Rudolf Klusal

    Description:

    Given two strings s1 and s2, we want to visualize how different the two strings are.
    We will only take into account the lowercase letters (a to z).
    First let us count the frequency of each lowercase letters in s1 and s2.

    s1 = "A aaaa bb c"

    s2 = "& aaa bbb c d"

    s1 has 4 'a', 2 'b', 1 'c'

    s2 has 3 'a', 3 'b', 1 'c', 1 'd'

    So the maximum for 'a' in s1 and s2 is 4 from s1; the maximum for 'b' is 3 from s2.
    In the following we will not consider letters when the maximum of their occurrences is less than or equal to 1.

    We can resume the differences between s1 and s2 in the following string:
    "1:aaaa/2:bbb" where 1 in 1:aaaa stands for string s1 and aaaa because the maximum for a is 4.
    In the same manner 2:bbb stands for string s2 and bbb because the maximum for b is 3.

    The task is to produce a string in which each lowercase letters of s1 or s2 appears as many times
    as its maximum if this maximum is strictly greater than 1; these letters will be prefixed by
    the number of the string where they appear with their maximum value and :.
    If the maximum is in s1 as well as in s2 the prefix is =:.

    In the result, substrings (a substring is for example 2:nnnnn or 1:hhh;
    it contains the prefix) will be in decreasing order of their length and when
    they have the same length sorted in ascending lexicographic order
    (letters and digits - more precisely sorted by codepoint);
    the different groups will be separated by '/'. See examples and "Example Tests".

    Hopefully other examples can make this clearer.

    s1 = "my&friend&Paul has heavy hats! &"
    s2 = "my friend John has many many friends &"
    mix(s1, s2) --> "2:nnnnn/1:aaaa/1:hhh/2:mmm/2:yyy/2:dd/2:ff/2:ii/2:rr/=:ee/=:ss"

    s1 = "mmmmm m nnnnn y&friend&Paul has heavy hats! &"
    s2 = "my frie n d Joh n has ma n y ma n y frie n ds n&"
    mix(s1, s2) --> "1:mmmmmm/=:nnnnnn/1:aaaa/1:hhh/2:yyy/2:dd/2:ff/2:ii/2:rr/=:ee/=:ss"

    s1="Are the kids at home? aaaaa fffff"
    s2="Yes they are here! aaaaa fffff"
    mix(s1, s2) --> "=:aaaaaa/2:eeeee/=:fffff/1:tt/2:rr/=:hh"
    Note for Swift, R, PowerShell
    The prefix =: is replaced by E:

    s1 = "mmmmm m nnnnn y&friend&Paul has heavy hats! &"
    s2 = "my frie n d Joh n has ma n y ma n y frie n ds n&"
    mix(s1, s2) --> "1:mmmmmm/E:nnnnnn/1:aaaa/1:hhh/2:yyy/2:dd/2:ff/2:ii/2:rr/E:ee/E:ss"
"""

# IMPORTS #
import re
import string


# RUNTIME #
def count_letters(
        input_string: str,
        empty: bool = False,
        sort: bool = True,
) -> dict:
    """
    Counts letters and creates a dictionary with letters as keys, values are counts
    :param input_string: String to count letters in
    :param empty: Flag if ignore the empty letters by default (set to True if you want zeroes in output)
    :param sort: FLag, by default True, if you want to return sorted dictionary
    :return: Dictionary, where keys are letters and values are numbers of occurences
    """

    output_dict = dict()

    for letter in string.ascii_lowercase:
        frequency = input_string.count(letter)
        if frequency > 0 and not empty:
            output_dict[str(letter)] = frequency

    return dict(sorted(output_dict.items(), key=lambda item: item[1], reverse=True)) if sort else output_dict


def mix(s1: str, s2: str) -> str:
    """
    Main function for CW
    :param s1: First string
    :param s2: Second string
    :return: Returns final string by CW
    """

    # STEP 1: Only take lowercase letters

    s1 = str(re.findall(r'[a-z]', s1))
    s2 = str(re.findall(r'[a-z]', s2))

    # STEP 2: Count occurences of all letters in both lists
    s1_freq = count_letters(s1, sort=True)
    s2_freq = count_letters(s2, sort=True)

    # STEP 3: Count differences for each letter
    output_dict = {}

    for letter in string.ascii_lowercase:
        s1_occ = s1_freq.get(letter, 0)
        s2_occ = s2_freq.get(letter, 0)

        if max(s1_occ, s2_occ) > 1:
            if s1_occ > s2_occ:
                output_dict[letter] = (1, s1_occ)
            elif s2_occ > s1_occ:
                output_dict[letter] = (2, s2_occ)
            else:
                output_dict[letter] = ('=', s1_occ)

    # STEP 4: Sort output_dict by length (descending) and lexicographically
    sorted_items = sorted(
        output_dict.items(),
        key=lambda item: (-item[1][1], str(item[1][0]), item[0])
    )

    # STEP 5: Format output
    output_string = '/'.join(f"{prefix}:{letter * count}" for letter, (prefix, count) in sorted_items)
    print(output_string)
    return (output_string)


if __name__ == "__main__":
    s1 = "A aaaa bbb 343 cccc"
    s2 = "! AaAabB bbbb 29!!"

    mix(s1, s2)
    mix("Are they here", "yes, they are here")
