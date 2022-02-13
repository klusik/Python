# create program, that will search the hard drive for given object (file, directory) and return match, type of object
# or returns error message if no match is found
import win32api
import os


class Search:

    def getAvailableHDDs(self):
        '''
        returns list of strings with all available drive letters.
        '''
        availableLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                            'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ]
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]  # returns ['C:', 'E:', 'F:', 'H:', 'V:', 'W:', 'X:', 'Z:']
        return drives

    def __init__(self,sInputText):  # metody s __xx__ se ihned vykonaji (__xx__ jsou v pythonu tzv magic methods)
        self.sInputText = sInputText
        self.drives = self.getAvailableHDDs()



    drives = getAvailableHDDs()

    def askUserForLetter(self):
        '''
        asks user to choose available drive letters on which the search will be performed
        '''

        print('This is list of available logical drives: ', self.drives)
        userChoice = input('Select any logical drive on which the search should run: ')
        print('Your choice is: ', userChoice)

    def searchForText(self):
        '''
        Searches for the text given as input on selected drive letters
        '''
        pass

    def returnMatch(self):
        '''
        Prints the result of the search
        '''
        pass
