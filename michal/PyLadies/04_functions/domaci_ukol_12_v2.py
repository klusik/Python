'''
12.

Výzva   
Napiš program, který simuluje tuto hru: První hráč hází kostkou (t.j. 
vybírají se náhodná čísla od 1 do 6), dokud nepadne šestka. Potom hází další 
hráč, dokud nepadne šestka i jemu. Potom hází hráč třetí a nakonec čtvrtý. 
Vyhrává ten, kdo na hození šestky potřeboval nejvíc hodů. (V případě shody
vyhraje ten, kdo házel dřív.)

Program by měl vypisovat všechny hody a nakonec napsat, kdo vyhrál.

Nápověda: průběžně stačí ukládat jen údaj, kdo vede.

Vytka lektora k v1:
Jako vtip dobrý, a teď opravit :D Probrali jsme na teamsech.
'''

import random

# generate throws and attempts
def roll_the_dice():
    '''
    Rolls the dice => choose random number from 1 to 6 until 6 is choosen. 
    Keep track of needed attempts
    Print the progress info - value of dice and number of attempts

    INPUT
    no input needed

    RETURN
    counter - needed number of attempts, integer
    '''
    iPlayer_counter = 0        
    #     
    while True:
        iPlayer_dice = random.randint(1,6)
        print(f'Dice has value of {iPlayer_dice}')
        iPlayer_counter = iPlayer_counter + 1
        print(f'Attempt number {iPlayer_counter}.')
        if iPlayer_dice == 6:
            return iPlayer_counter



# evaluate
def eval():
    '''
    Roll the dice for four players. Based on needed rolls evaluate winner
    using following key:

    1) Player with greatest amount of throws wins
    2) In case of a tie order of players take precedence
        if player1_attempts == player2_attempts 
            and player1_attempts == player3_attempts
                and player1_attempts == player4_attempts:
                    winner = player1_attempts
    '''

    # generate throws and attempts for four players
    # roll_the_dice() returns integer with number of attempts, prints progress
    print('Player 1 rolls the dice:')
    iPlayer1 = roll_the_dice()

    print('Player 2 rolls the dice:')
    iPlayer2 = roll_the_dice()
    
    print('Player 3 rolls the dice:')
    iPlayer3 = roll_the_dice()
    
    print('Player 4 rolls the dice:')
    iPlayer4 = roll_the_dice()    

    # find greatest amount of attempts => winning number of attempts
    iWinningCounter = max(iPlayer1, iPlayer2, iPlayer3, iPlayer4)

    # to avoid refence before assigment
    bP1win = 0
    bP2win = 0
    bP3win = 0
    bP4win = 0

    # every player with winning number of attempts
    if iPlayer1 == iWinningCounter:
        bP1win = True
    if iPlayer2 == iWinningCounter:
        bP2win = True
    if iPlayer3 == iWinningCounter:
        bP3win = True
    if iPlayer4 == iWinningCounter:
        bP4win = True

    # winning order 
    if bP1win == True:
        print(f'Player 1 wins with {iPlayer1} attempts.')
    elif bP2win == True and bP1win == False:
        print(f'Player 2 wins with {iPlayer2} attempts.')
    elif bP3win == True and bP2win == False and bP1win == False:
        print(f'Player 3 wins with {iPlayer3} attempts.')
    else:
        print(f'Player 4 wins with {iPlayer4} attempts.')

# start the game
eval()
