'''
Výzva  Zvládneš pro počítač naprogramovat lepší strategii? Třeba aby se snažil hrát vedle svých existujících symbolů nebo aby bránil protihráčovi?

Stačí jen docela malé vylepšení!
'''

# IMPORTS
import random

def prepare_field(field, position, symbol):
    '''
    Place player symbol on defined position on the game field
    
    INPUTS
    field = game field, string
    position = postion to place symbol to, integer
    symbol = symbol to be inserted into game field, string
    
    output
    new_field = updated game field with new symbol in it, string
    '''
    pre_position = field[:position]
    post_position = field[position + 1:]
    # return new field
    new_field = pre_position + symbol + post_position
    return new_field

def evaluate(field):
    """
    Evaluate game status. Possible outcomes:
    x winner = 'xxx' in the game field is present.
    o winner = 'ooo' in the game field is present.
    no winner = '-' is no longer present in the field.
    ongoing = no previous conditions are met

    INPUT:
    field = game field, string # '--------------------'

    OUTPUT
    Only one outcome out of the following possibilities:
    - 'x' = winner is 'x', string
    - 'o' = winner is 'o', string
    - '!' = no winner, string
    - '-' = ongoing, string
    """
    if ('xxx' in field):
        print('Player with "x" is the winner.')
        return 'x'
    elif ('ooo') in field:
        print('Player with "o" is the winner.')
        return 'o'
    elif('-' not in field):
        print('There is no winner, it\'s a tie.')
        return '!'
    else:
        print('Game is not yet finished.')
        return '-'

def player_turn(field, player_symbol):
    """
    Ask player for position to place the symbol. Check availability
    of selected position. Return updated game field.

    INPUT
    field = field containing current game status, string
    player symbol = symbol representing player choince on the game field, string
    position = via input() gathered position number, integer

    OUTPUT
    new_field = updated game field containing current game status, string
    """
    
    # get valid user choice
    while True:
        position = int(input('Select the position to place your symbol: '))
        # invalid selection
        if not(field[position] == '-'):
            print('Invalid selection, position already taken. Make a new choice')
        # correct selection
        else:
            new_field = prepare_field(field, position, player_symbol)
            return new_field

def CML_turn(field, CML_symbol, player_symbol):
    '''
    Return updated game field with CML's turn.
    CML turn is randomly selected. If selected position is not available, 
    add symbol to first available position from 0 onwards.
    '''
    
    # ==================
    # DEFENSIVE STRATEGY
    # ==================

    # FIRST DEFENSIVE TURN:
    # if only one oponent field is taken, actively block oponent
    count_player_symbol = field.count(player_symbol)
    if count_player_symbol == 1:
        # get the position of the oponent symbol
        player_position = field.find(player_symbol)
        CML_position = player_position + 1
        # prepare new field    
        new_field = prepare_field(field, CML_position, CML_symbol)
        return new_field

    # LOSS STRATEGIES
    # try to avoid victory of oponent
    right_loss = player_symbol + player_symbol + '-' # xx-
    left_loss = '-' + player_symbol + player_symbol # -xx
    
    # LEFT LOSS '-xx'
    if left_loss in field:
        # BLOCK
        # get the postion
        block_position = (field.find(left_loss))
        # prepare new field
        new_field = prepare_field(field, block_position, CML_symbol)
        return new_field
    
    # RIGHT LOSS 'xx-'
    elif right_loss in field:
        # BLOCK
        # get the postion (+2 calculated to include len of loss string 'xx-')
        block_position = (field.find(left_loss)) + 2
        # prepare new field
        new_field = prepare_field(field, block_position, CML_symbol)
        return new_field

    # ==================
    # OFFENSIVE STRATEGY
    # ==================

    # FIRST TURN STRATEGY
    # start in the middle
    if field == 20 * '-': # '--------------------':
        # middle of the field
        middle_position = 10
        # prepare new field
        new_field = prepare_field(field, middle_position, CML_symbol)
        return new_field

    # VICTORY STRATEGIES
    right_win = CML_symbol + CML_symbol + '-' # 'xx-'
    left_win = '-' + CML_symbol + CML_symbol # '-xx'
    
    # INVESTIGATION NEEDED, 'xx-' pattern not recognised!
    # RIGHT WIN 'xx-'
    if right_win in field:
        # find index of substring
        index_right = field.find(right_win) # ---xx--- => returns index of 2, where substring starts
        # calculate position to place a winning symbol
        index_right_winning = index_right + len(right_win) - 1
        # prepare new field
        new_field = prepare_field(field, index_right_winning, CML_symbol)
        return new_field
    
    # LEFT WIN '-xx'
    elif left_win in field:
        # find index of substring
        index_left = field.find(left_win)
        # calculate position to place a winning symbol
        index_left_winning = index_left - 1
        # prepare new field
        new_field = prepare_field(field, index_left_winning, CML_symbol)
        return new_field
    
    # NO STRATEGY -> make random turn
    CML_turn = random.randint(1, 20) # CML = centralni mozek lidstva
    print(f'CML choice: {CML_turn}.')
    # prepare new field
    new_field = prepare_field(field, CML_turn, CML_symbol)
    return new_field

def set_player_symbol():
    '''
    Return symbol of player's choice obtained using input() method.
    Possible choices are 'x' and 'o'. If player selects symbol,
    remaining symbol is assigned to CML. Symbol selection does not affect
    starting player.

    INPUT
    
    OUTPUT
    symbol = player choice, string
    CML_symbol = CML symbol, remaining symbol
    '''
    player_symbol = input('Select your symbol ("x"/"o"): ')

    if player_symbol == 'x':
        print('You have selected "x", CML is being assigned "o".')
        CML_symbol = 'o'
    else:
        CML_symbol = 'x'
    
    return player_symbol, CML_symbol

def ticktacktoe():
    '''
    Create game field of size 20 for 1D tick tack toe game. 
    Call functions player_turn() and CML_turn() until winner is known.
    Check game status after each turn.
    '''
    
    # create game field
    game_field = '--------------------'

    # obtain player symbols
    player_symbol, CML_symbol = set_player_symbol()
    
    # turn counter
    turn_counter = 0

    # play the game in the cycle -> maintain turn changes
    while True:
        
        turn_counter = turn_counter + 1
        
        # view the game field
        print(f'Current view of game field: {game_field}')
        # vytiskni indexy pro prehlednost
        
        print(f'Turn number {turn_counter}.')
        
        if turn_counter % 2 == 1:    
            # HUMAN - updated game field after human player turn
            game_field = player_turn(game_field, player_symbol)
        
        else:
            # CML - updated game field after CML player turn
            game_field = CML_turn(game_field, CML_symbol, player_symbol)
        
        # evaluate game status
        status = evaluate(game_field)
        
        # game over condition
        if status != '-':
            print(game_field)
            print('End of game')
            break 

# RUNTIME
ticktacktoe()
