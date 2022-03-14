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
    Generate throws on the dice untile 6 is present. Keep track of number
    of throws until 6 is present. Return number of throws.
    
    INPUT
    None
    
    OUTPUT
    iPlayer_counter
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
        
        # desired number is present on the dice, return number of throws
        if iThrow == 6:
            return iPlayer_counter

        
def play_the_game(iNumber_of_players):
    iPlayer_atttempts_counter = 0
    iWinning_attempts_counter = 0
    iWinning_player_number = 10
    
    
    for iPlayer_number in range(1,iNumber_of_players+1):
        iPlayer_atttempts_counter = throw_the_dice()
        
        print(f'It was player {iPlayer_number} turn.')
        
        if iPlayer_atttempts_counter > iWinning_attempts_counter:
            iWinning_attempts_counter = iPlayer_atttempts_counter
            print(f'Winning number of attempts: {iWinning_attempts_counter}')
            iWinning_player_number = iPlayer_number

    print(f'Winning player number is {iWinning_player_number}')            
    
play_the_game(4)
    
    
    
    
    