'''
Napiš funkci, která převede římské číslice zadané jako řetězec str na číslo int.
'''

# IMPORTS
# import sys

def rom_to_int(whole_roman_number):
    '''
    Convert roman numbers to standard integers (arabic numbers with base 10)

    INPUT
    roman_number = roman numbers, string

    OUTPUT
    result = converted number, integer

    DETAILS
    Implementation idea is to start from right (smallest number) and compare
    next number. If next number is bigger, add the next_number to result, 
    else subtract number from result.

    EXAMPLE

    MCMXCIV = 1994
    i = V -> V = 5
    i + 1 = I -> I = 1
    (i + 1) < i => result = 5 - 1 

    next iteration
    i = I
    i + 1 = C -> C = 100
    i + 1 > i => result + C
    result = 104

    if i + 1 = None: return result
    '''
    
    # keeps track of value of roman number
    result = 5
    
    # definition table of roman numbers
    table = [
            1,'I',
            5, 'V',
            10, 'X',
            50, 'L',
            100, 'C',
            500, 'D',
            1000, 'M'
            ]

    # fix upper/lower situation
    whole_roman_number = whole_roman_number.upper()

    # switch roman number with smallest number sitting on the left
    # due to fact algorith works from smallest numbers and to avoid using
    # minuses when looking for index of letter
    whole_roman_number = whole_roman_number[::-1]

    for current_roman in whole_roman_number:
        # index in roman  string
        next_roman_index = whole_roman_number.index(current_roman) + 1 
        # value derived from index
        next_roman_string = whole_roman_number[next_roman_index] 

        # retrieve values from table
        current_roman_value = table[table.index(current_roman)-1]
        next_roman_value = table[table.index(next_roman_string)-1]

        # next is bigger
        if next_roman_value >= current_roman_value:
            # add current roman number and next number
            result = next_roman_value + result
        # next is smaller
        else:
            result = result - next_roman_value
            
    return result

print(rom_to_int('mcmxciv'))