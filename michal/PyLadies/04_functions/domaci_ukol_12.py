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

'''

# IMPORTS
import random

def biutiful_soup():
    '''
    Vygeneruj hrace podle poctu hracu, hazej kostkou, dokud nepadne 6.
    Sleduj pocet hodu potrebnych na dosazeni 6. Srovnej hrace podle
    potrebnych hodu. Shoda hodu = vede poradi hracu.
    '''
    player1_counter = 0
    player2_counter = 0
    player3_counter = 0
    player4_counter = 0

# zyklus pro player 1    
    while True:
        player1_dice = random.randint(1,6)
        player1_counter = player1_counter + 1
        print(f'Player 1 ma na kostce {player1_dice}. Hod cislo {player1_counter}.')
        if player1_dice == 6:
            print(f'Konec hodu player 1, protoze padla {player1_dice}, pocet hodu je {player1_counter}.')
            break
            
# zyklus pro player 2
    while True:
        player2_dice = random.randint(1,6)
        player2_counter = player2_counter + 1
        print(f'Player 2 ma na kostce {player2_dice}. Hod cislo {player2_counter}.')
        if player2_dice == 6:
            print(f'Konec hodu player 2, protoze padla {player2_dice}, pocet hodu je {player2_counter}.')
            break
        
# zyklus pro player 3
    while True:
        player3_dice = random.randint(1,6)
        player3_counter = player3_counter + 1
        print(f'Player 1 ma na kostce {player3_dice}. Hod cislo {player3_counter}.')
        if player3_dice == 6:
            print(f'Konec hodu player 3, protoze padla {player3_dice}, pocet hodu je {player3_counter}.')
            break
# zyklus pro player 4
    while True:
        player4_dice = random.randint(1,6)
        player4_counter = player4_counter + 1
        print(f'Player 4 ma na kostce {player4_dice}. Hod cislo {player4_counter}.')
        if player4_dice == 6:
            print(f'Konec hodu player 4, protoze padla {player4_dice}, pocet hodu je {player4_counter}.')
            break           
      
# evaluate
    
    # pokud je player1_counter nejmensi
    if player1_counter <= player2_counter \
        and player1_counter <= player3_counter \
            and player1_counter <= player4_counter:
                print(f'Player 1 potreboval nejmensi pocet pokusu na hozeni 6. Pocet pokusu byl {player1_counter}.')
                
    # pokud je player2_counter nejmensi
    if player2_counter <= player1_counter \
        and player2_counter <= player3_counter \
            and player2_counter <= player4_counter:
                print(f'Player 2 potreboval nejmensi pocet pokusu na hozeni 6. Pocet pokusu byl {player2_counter}.')

    # pokud je player3_counter nejmensi
    if player3_counter <= player1_counter \
        and player3_counter <= player2_counter \
            and player3_counter <= player4_counter: 
                print(f'Player 3 potreboval nejmensi pocet pokusu na hozeni 6. Pocet pokusu byl {player3_counter}.')
                
    # pokud je player4_counter nejmensi
    if player4_counter <= player1_counter \
        and player4_counter <= player2_counter \
            and player4_counter <= player3_counter:
                print(f'Player 4 potreboval nejmensi pocet pokusu na hozeni 6. Pocet pokusu byl {player4_counter}.')
        
biutiful_soup()        
