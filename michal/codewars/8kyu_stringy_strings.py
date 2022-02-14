# write me a function stringy that
# the string should start with a 1.
# a string with size 6 should return
# with size 4 should return : '1010'.
# with size 12 should return : '101010101010'.
# The size will always be positive and will only use whole numbers.
def stringy(size):
    # Good Luck!
    string_even = '10'
    string1 = '1'
    if size % 2 == 0:
        output = size // 2 * string_even
    else:
        output = (size // 2 * string_even) + string1

    return output


print(stringy(5))
