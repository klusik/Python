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
    '''
    
    # keeps track of value of roman number
    result = 0
    
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

    # flag skip, used for skipping next letter in 'iv' pattern and similar
    skip = False
    
    # index used for easy recognition of next number
    for index, current_roman in enumerate(whole_roman_number):
        
        # 'iv' pattern handle
        if skip:
            skip = False
            continue
        
        # index in roman  string
        next_roman_index = index + 1 
        
        # no next character
        if next_roman_index >= len(whole_roman_number):
            next_roman_string = current_roman
        else:
            # value of next roman string derived from index
            next_roman_string = whole_roman_number[next_roman_index]

        # retrieve values from table
        current_roman_value = table[table.index(current_roman)-1]
        next_roman_value = table[table.index(next_roman_string)-1]

        # next is bigger
        if next_roman_value >= current_roman_value:
            # add current roman number and next number
            result = current_roman_value + result
        # next is smaller
        else:
            result = result + (current_roman_value - next_roman_value)
            skip = True
            
    return result

print(rom_to_int('mcmxciv'))