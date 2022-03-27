'''
12.

Výzva   
Napiš program, který simuluje tuto hru: První hráč hází kostkou 
(t.j. vybírají se náhodná čísla od 1 do 6), dokud nepadne šestka. Potom hází 
další hráč, dokud nepadne šestka i jemu. Potom hází hráč třetí a nakonec 
čtvrtý. Vyhrává ten, kdo na hození šestky potřeboval nejvíc hodů. (V případě 
shody vyhraje ten, kdo házel dřív.)

Program by měl vypisovat všechny hody a nakonec napsat, kdo vyhrál.

Nápověda: průběžně stačí ukládat jen údaj, kdo vede.

Vytka lektora:
O hodně lepší.
Ještě tam vidím prostor pro určité vylepšení.
Když se podíváš, hodně věcí se ti tam 4x opakuje. To si vyloženě říká o cyklus.
Třeba vzít nějakou inspiraci ze cvičení, kdy jsme si měli zapamatovat nejnižší
číslo z deseti pokusů?.. 
Koukneme kdyžtak na cvičení.
'''

# IMPORTS
import random

def throw_the_dice():
    '''
    Generate throws on the dice until 6 is present. Keep track of number
    of throws. Return number of throws.
    
    INPUT
    None
    
    OUTPUT
    iPlayer_counter - number of throws until 6 is present, integer
    console prints - value on the dice, number of throw
    '''
    
    # declarations
    iThrow = 0              # generated number on the dice
    iPlayer_counter = 0     # number of throws
        
    while True:
        # generate the value on the dice
        iThrow = random.randint(1,6)
        
        # raise the counter with throws of the dice
        iPlayer_counter = iPlayer_counter + 1
        
        print(f'Dice value is {iThrow}, throw number {iPlayer_counter}.')
        
        # if desired number is present on the dice, return number of throws
        if iThrow == 6:
            return iPlayer_counter

        
def play_the_game(iNumber_of_players):
    '''
    Call throw_the_dice() for each player, evaluate number of throws, therefore
    the winner. Winner is the player with the highest amount of throws. 
    In case of a tie scenario, winner is the player who reached the highest
    number of throws first.

    INPUT
    iNumber_of_players - number of players, integer

    OUTPUT
    console prints - turn of actual player, winning number of throws, winning
                     player.
    '''

    # declarations
    iPlayer_throws_counter = 0       # keep track of throws for each player
    iWinning_throws_counter = 0      # winning throws number
    iWinning_player_number = 0       # winning player number
    
    # range 1 to number of players + 1 used to avoid player 0 situation
    for iPlayer_number in range(1,iNumber_of_players+1):
        # get the number of throws
        iPlayer_throws_counter = throw_the_dice()
        
        print(f'It was player {iPlayer_number} turn.')
        
        # winning condition = highest throws number occurs
        # tie situation is handled via > operator instead of >=
        if iPlayer_throws_counter > iWinning_throws_counter:
            iWinning_throws_counter = iPlayer_throws_counter
            print(f'Winning number of attempts: {iWinning_throws_counter}')
            
            # re-write also winning player number 
            iWinning_player_number = iPlayer_number

    print(f'Winning player number is {iWinning_player_number}'
          f' with {iWinning_throws_counter} throws.')            

# RUNTIME    
play_the_game(5)

    
# standard modules
import logging
import sys

# standard platform specific modules
import win32com.client

# third party
import markdown 

# project
import MujModul
    
