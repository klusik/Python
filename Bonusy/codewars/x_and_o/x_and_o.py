"""
Check to see if a string has the same amount of 'x's and 'o's. The method must return a boolean and be case insensitive. The string can contain any char.

Examples input/output:

XO("ooxx") => true
XO("xooxx") => false
XO("ooxXm") => true
XO("zpzpzpp") => true // when no 'x' and 'o' is present should return true
XO("zzoo") => false

"""

def xo(s):
    return s.lower().count('o') == s.lower().count('x')

if __name__ == "__main__":
    user_input = str(input("Enter string: "))

    if xo(user_input):
        print("Same count.")
    else:
        print("Different count.")