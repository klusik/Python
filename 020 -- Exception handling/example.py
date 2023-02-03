# example for trainingn of exception handling in python

'''
Author: Michal Sykora
Year: 2022
License: Lol
'''

# open a non existing file
from typing import final


file = r'c:/pypi.py'
try:
    with open(file) as f:
        print("nic se nedeje")
except FileNotFoundError:
    # will be used when code in try is corrupt
    print('neexistujici soubor')
    #raise FileNotFoundError
except Exception as Unhandled:
    # general unhandeled exception
    print(Unhandled.args,"neco se pokakalo")
    
finally:
    # will be used after all excepts clauses
    # will be triggered always
    print("vytisteno z finally")