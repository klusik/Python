'''
Napiš funkci tah_pocitace, která dostane řetězec s herním polem, vybere pozici, 
na kterou hrát, a vrátí herní pole se zaznamenaným tahem počítače.

Použij jednoduchou náhodnou „strategii”:

    Vyber číslo od 0 do 19.
    Pokud je dané políčko volné, hrej na něj.
    Pokud ne, opakuj od bodu 1.

Hlavička funkce by tedy měla vypadat nějak takhle:

def tah_pocitace(pole):
    "Vrátí herní pole se zaznamenaným tahem počítače"
'''
# IMPORTS
import random
def tah_pocitace(pole):
    '''
    Vrátí herní pole se zaznamenaným tahem počítače
    '''
    CML_turn = random.randint(1, 20) # CML = centralni mozek lidstva
    print(f'CML choice: {CML_turn}.')

    # backup plan: IF field is like 'x-----xoxoxoxoxooxox' and CML choice is 12
    # => taken position and every other field position is taken until end, yet
    # there are still some available positions left to play
    planB = 0 
    # field available
    while True:
        # position not available, look for available position from beginning
        if not(pole[CML_turn] == '-'):
            planB = planB + 1
            CML_turn = planB
        else:
            # hardcoded CML symbol
            CML_symbol = 'o'
            pre_position = pole[:CML_turn]
            post_position = pole[CML_turn:]
                # fix adding extra character
            if CML_turn == 19:
                new_field = pre_position + CML_symbol
                return new_field
            else:
                new_field = pre_position + CML_symbol + post_position
                return new_field

print(tah_pocitace('x-----xoxoxoxoxooxox'))
