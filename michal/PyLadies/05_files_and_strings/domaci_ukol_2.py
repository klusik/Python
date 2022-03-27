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
    strng = len(StringToBeCleansed.replace(' ', ''))
    print(f'number of chars without withespaces: {strng}')
    return strng

whitespace_hate('I really really loath the whitespaces!')