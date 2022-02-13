# this program helps solve the WOW puzzle
# user defines number of position and available characters for each position
# program returns all possible combinations of characters on each position

# user can enter a fixed string on specific position

# imports
import itertools

def solver(positions, characters):
    '''
    input arguments
    positions = length of searched word
    characters = all available characters separated by comma
    output = list of all available characters

    principle of operation:
            column
    line    0   1   2   3
    1       A   A   A   A
    2       A   A   A   B
    3       A   A   A   C
    4       A   A   A   D   <- LAST CHAR
    5       A   A   B   A
    6       A   A   B   B
    7       A   A   B   C
    8       A   A   B   D   <- LAST CHAR
    9       A   A   C   A
    10      A   A   C   B
    11      A   A   C   C
    12      A   A   C   D   <- LAST CHAR
    13      A   A   D   A
    etc...

    provides  itertools.combinations_with_replacement(iter, len) funciton

    '''

    # split characters into a list of separated characters strings
    #character = characters.split(", ")
    #character = ''.join(character)

    # generate list of all possible combinations
    l = list(itertools.product(characters, repeat = positions))

    for item in l:
        yield item
    # return l



    


for item in solver(6, 'saltoy'):
    print(item)

