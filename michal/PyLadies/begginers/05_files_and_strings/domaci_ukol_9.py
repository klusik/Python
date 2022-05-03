'''
Napiš funkci tah_hrace, která dostane řetězec s herním polem, zeptá se hráče, 
na kterou pozici chce hrát, a vrátí herní pole se zaznamenaným tahem hráče. 
Funkce by měla odmítnout záporná nebo příliš velká čísla a tahy na obsazená 
políčka. Pokud uživatel zadá špatný vstup, funkce mu vynadá a zeptá se znova.
'''

def tah_hrace(field):
    '''
    Commit player turn, return field with player's turn. Ask for player input
    (not as function argument). 
    Check that player input is valid:
    -> refuse negative numbers
    -> refuse too big numbers
    -> refuse 'taken' fields = not('-')

    If conditions for player's input are not met, print warning message, 
    ask again for valid input until all conditions are met.
    '''

    # check valid turn
    while True:

        # ask for player's turn
        player_turn = int(input('Enter integer in range 0-19: '))   # position
        
        # check negative numbers
        if player_turn < 0:
            print('Selected position is under minimum, make a new choice.')
        
        # check maximum number
        elif player_turn > 19:
            print('Selected position is over maximum, make a new choice.')

        # check availability of the selected field
        elif not(field[player_turn] == '-'): # string under player field
            print('Selected position is already taken, make a new choice.')
        else:
            # hardcoded player symbol
            player_symbol = 'x'
            
            # parse field 
            pre_position = field[:player_turn]
            post_position = field[player_turn:]
            
            # fix the issue with adding extra char when last position choosen
            if player_turn == 19:
                new_field = pre_position + player_symbol
            else:
                new_field = pre_position + player_symbol + post_position
            
            return new_field

print(tah_hrace('x-------------------'))
