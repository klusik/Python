'''
Napiš funkci tah, která dostane řetězec s herním polem, číslo políčka (0-19),
a symbol (x nebo o) a vrátí herní pole (t.j. řetězec) s daným symbolem 
umístěným na danou pozici.

Hlavička funkce by tedy měla vypadat nějak takhle:

def tah(pole, cislo_policka, symbol):
    "Vrátí herní pole s daným symbolem umístěným na danou pozici"
    ...

'''

def turn(field, position, symbol):
    '''
    Return updated game field with given symbol placed into original game filed.
    Positions are being calculated from 0

    INPUT
    field - field consisting of '-', 'x' or 'o', string
    position - index number where new char should be placed, integer
    symbol - players symbol 'x' or 'o', string

    RETURN
    new_field - new game field including players symbol
    '''
    # divide field to three parts, pre-position, position and after-position
    pre_position_field = field[:position]

    # post position 
    post_position_field = field[position:]

    # char on selected position
    position_char = field[position]
    # test for available position
    if not(position_char == '-'):
        print('invalid position')
    else:
        # concatenate three parts into output game field
        new_field = pre_position_field + symbol + post_position_field
    
    return new_field

print(turn('-----xoxoxxo--------', 4, 'x'))
