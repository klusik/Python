# Ukolem je:
# 1) zjistit, kolik ma dane slovo znaku
# 2) zjistit, kolikrat se dane slovo na radku vyskytuje
# 3) rozhodnout, zda zadane slovo je palindrom
# 4) uhledne vypsat ***uzivateli seznam vyse zjistenych inform

import os.path

class Pali:
    
    def __init__(self, sPath):
        self.sPath = sPath

    def readfile(sFilepath):
        # define file
        sFilepath = f'r{sFilepath}'

        # check that given file exist
        if not os.path.isfile(sFilepath):
            print('File does not exist'.)

        # open file, save content, split each line
        with open(sFilepath) as f:
            lFileContent = f.read().splitlines()

    def findWord(sFileline):
        pass

    def isPalindrome(sWord):
        pass

    def userOutput(sWord, sFileline):
        pass