#
# Hangman -- guess the word letter by letter or the whole word
#
# Author: Rudolf Klusal
#

import random



# Random words (not so random :-D) from which we will guess just one
words =     {'bake', 'rolls', 'garlic', 'bread', 'crisp', 'ingredient', 'wheat', 'flour', 'oil', 'salt', 
            'sugar', 'yeast', 'bean', 'emulsifier', 'agent', 'cysteine', 'starch', 'allergy', 'advice', 
            'gluten', 'bold', 'facility', 'milk', 'egg', 'peanut', 'hazelnut', 'almond', 'pistachio', 'sesame', 'celery'}

# count number of '_' chars in word
def countDashes(word):
    count = 0
    for i in range(0, len(word)):
        if word[i] == '_':
            count = count + 1

    return count

# displays a guessed word
def displayGuessed(word):
    result = ''
    for i in range(0, len(word)):
        result = result + word[i] + ' '

    return result


def makeAGuess(userWord, guessedWord, randomWord):
    # if user enters just one letter, whole word or empty
    if len(userWord) == 1:
        # user enters one character
        # need to find all characters from userWord in randomWord and if not guessed previously in guessedWord
        # (that's a reason we need all 3)
        count = 0
        for i in range(0, len(randomWord)):
            if randomWord[i] == userWord:
                if randomWord[i] != guessedWord[i]:
                    guessedWord[i] = randomWord[i]
                    count = count + 1

        return[guessedWord, count]

    elif len(userWord) > 1:
        if str(userWord) == str(randomWord):
            guessedWord = randomWord
            count = 1
            return  [guessedWord, count]
        else:
            return [guessedWord, -1]
        
    else: 
        return [guessedWord, -1]

def game(randomWord, lives):

    guessedWord = []
    for i in range(0, len(randomWord)):
        guessedWord.append('_')


    while lives > 0:
        remains = countDashes(guessedWord)

        if remains == 0:
            return 1

        # user input
        print(f"Guess the word, so far you have: {displayGuessed(guessedWord)} and {lives} lives.")
        userWord = input('Insert a letter to fill or whole word, if you think you know: ')

        [guessedWord, hits] = makeAGuess(userWord, guessedWord, randomWord)

        if hits == 0:
            # missed a letter
            lives = lives - 1
        
        if hits == -1:
            # missed a word
            return -1

    if lives > 0:
        return(lives)
    else:
        return(0)


def main():
    lives = 3

    # Change type from 'set' to 'list' 
    # In a set I can't index things.
    listOfWords = list(words)

    # Select random word from list listOfWords
    # random.randrange(0,10) generates random numbers from 0 to 9 (e.g.)
    # len(words) returns number of items in list
    randomWord = listOfWords[random.randrange(0, len(words))]

    result = game(randomWord, lives)

    if result == 1:
        print("You won!")
    
    if result == 0:
        print("You lost, not enough lives.")
    if result == -1:
        print("You lost, the word wasn't this word.")
    

if __name__ == "__main__": main()