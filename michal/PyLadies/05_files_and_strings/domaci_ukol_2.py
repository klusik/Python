'''
Napiš funkci, která vrátí počet znaků (bez mezer) v řetězci, který je zadaný 
jako argument funkce. Výsledek funkce vypiš v těle hlavního programu pomocí print.
'''

def whitespace_hate(StringToBeCleansed):
    '''
    Remove every single whitespace in given string. Print result to console.

    INPUT
    StringToBeCleansed - any string possible, string

    OUTPUT
    console print - original string cleansed of withespaces
    '''

    print(StringToBeCleansed.replace(' ', ''))

whitespace_hate('I really really loath the whitespaces!')