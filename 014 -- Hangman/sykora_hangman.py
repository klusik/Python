# hangman game
# michal sykora
# freeware
# 22.9.2021

# imports
from math import trunc
import random

# functions
def hangman():
    '''
    function chooses random string from list of word
    user is guessing letters in the word
    user has 3 lives (can make 3 mistakes)
    '''
    # choose random word for guessing
    sWordForGuess = randword()

    # define number of lives
    iNumOfLives = 3

    # variable to store the progress in a game
    sUserProgress = ''
    
    # the main game while cycle
    while True:
    # GAME LOST
        if iNumOfLives == 0:
            return print('You have lost the game, LOOSER! You were not able to guess the word ' + sWordForGuess + '. I hope your mother is proud of you...')

        # GAME WON
        if sUserProgress == sWordForGuess: # sem dopln promenou, do ktere budes ukladat uzivateluv progress
            return print('You have defeated the great Lizzard Wizzard. The guessed word was: ' + sWordForGuess + '. Please leave me mourn...')
        
        # ask user for a guess
        sUserGuess = input('Please choose a letter, not a number (exceptions not handled):')
        sUserGuess = sUserGuess.lower()

        # is user's guess in sWordForGuess?
        if sUserGuess in sWordForGuess:
            print('Great! Your choosen letter is in guessed word. Number of remaining lives is: ' + iNumOfLives)
            # show user succesfull letter in sWordForGuess
            
        else:
            iNumOfLives = iNumOfLives - 1
            print('This is bad. Your choosen letter is not in guessed word. You have lost one life. You have ' + iNumOfLives + ' lives!')
    
    


    # find each occurence of users guess in sWordForGuess


def randword():
    # defined list of words for guess
    lwords = ['bake', 'rolls', 'garlic', 'bread', 'crisp',
            'ingredient', 'wheat', 'flour', 'oil', 'salt', 'sugar',
            'yeast', 'bean', 'emulsifier', 'agent', 'cysteine',
            'starch', 'allergy', 'advice', 'gluten', 'bold',
            'facility', 'milk', 'egg', 'peanut', 'hazelnut',
            'almond', 'pistachio', 'sesame', 'celery']
    # define range for random integers
    ranglen = len(lwords)
    
    # find random word
    sRwordIndex = random.randint(0, ranglen)
    sRword = lwords[sRwordIndex]
    return sRword

# calls
#print (randword())