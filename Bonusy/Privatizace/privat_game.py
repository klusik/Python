"""
    Big privatisation

    Author: klusik@klusik.cz

    Description: A classic deskgame
"""

# IMPORTS
import logging

# CONFIG
#logging.basicConfig(level = logging.INFO)

# CLASSES
class GameConstants:
    """
        GameConstants contains basic setup
    """

    # Default gameboard size
    defaultGameboardXSize = 5
    defaultGameboardYSize = 5

    # Field constants
    fieldMaxValue   = 3
    edgeMaxValue    = 2
    cornerMaxValue  = 1

    # Player constants
    defaultPlayerName = "Player"

class Player:
    def __init__(self, name = GameConstants.defaultPlayerName, playerId = 0):
        self.name = name
        self.playerId = playerId
        self.accumulatedChips = 0

class GameField:
    """A one piece of field in the game"""
    def __init__(self, maxValue = GameConstants.fieldMaxValue):
        self.maxValue = maxValue
        self.value = 0
        self.playerId = 0

    def isStable(self):
        """ Returns True if stable """
        if self.value <= self.maxValue:
            return True
        else:
            return False

    def increaseValue(self):
        self.value += 1
        pass

    def clearValue(self):
        self.value = 0
        pass

    def lockValue(self):
        pass

    def unlockValue(self):
        pass

    def stabilize(self):
        self.value = self.value - self.maxValue - 1
        pass

    def assignToPlayer(self, playerId = 0):
        pass

class Gameboard:
    """
        Game board class
        Contains game field
    """
    def __init__(self, xSize = GameConstants.defaultGameboardXSize, ySize = GameConstants.defaultGameboardYSize):
        # basic setup

        #self.gameBoard = [ [GameField()] * xSize for row in range(ySize)]
        self.gameBoard = []
        for row in range(ySize):
            self.gameBoard.append([])
            for col in range(xSize):
                self.gameBoard[row].append(GameField())




        self.xSize = xSize
        self.ySize = ySize

        # maxValues tunning

        # edges and corners
        for rowIndex, row in enumerate(self.gameBoard):
            for colIndex, field in enumerate(row):
                """
                    edges are when colIndex == 0 xor colIndex == xSize - 1,
                    rowIndex == 0 xor rowIndex == ySize - 1.
                    
                    If both colIndex and colIndex == 0, maximum gameboard size
                    or one zero and other maximum size, it's a corner then
                """



                if  (rowIndex == 0 or rowIndex == (self.ySize - 1)) \
                    or (colIndex == 0 or colIndex == (self.xSize - 1)):
                    # edge
                    field.maxValue = GameConstants.edgeMaxValue
                    logging.info(f"E: Changing [{rowIndex}][{colIndex}] to {field.maxValue}")
                    pass


                if  (rowIndex == 0 and colIndex == 0) \
                    or (rowIndex == 0 and colIndex == (xSize-1)) \
                    or (rowIndex == (ySize - 1) and colIndex == 0) \
                    or (rowIndex == (ySize - 1) and colIndex == (xSize - 1)):
                    # corner
                    field.maxValue = GameConstants.cornerMaxValue
                    logging.info(f"C: Changing [{rowIndex}][{colIndex}] to {field.maxValue}")
                    pass



    def getGameBoard(self):
        # Header for cols:
        gameBoardFormatted = ""
        for col in range(self.xSize):
            gameBoardFormatted += "{:2}".format(col)

        gameBoardFormatted += "\n"

        # separator
        for col in range(self.xSize):
            gameBoardFormatted += "--"
        gameBoardFormatted += "\n"

        for rowNumber, row in enumerate(self.gameBoard):
            for field in row:
                gameBoardFormatted += "{:2}".format(field.value)
            gameBoardFormatted += f" | {rowNumber}\n"
        return gameBoardFormatted

    def isStable(self):
        """Returns true if the whole game is stable,
        meaning if there's not any unstable field in the game"""

        stability = dict()

        for rowIndex, row in enumerate(self.gameBoard):
            for colIndex, field in enumerate(row):
                if not field.isStable():
                    return {'stability':False, 'row':rowIndex, 'col':colIndex}
        return {'stability': True}

    def gameOver(self):
        """If game over conditions met, return True, else False"""
        return False

    def userInput(self):
        """
            Let the user do the input (play the game) :-)
            default input is 0,0

        """
        while True:
            # logging
            for rowIndex, row in enumerate(self.gameBoard):
                for colIndex, field in enumerate(row):
                    logging.info(f"[{rowIndex}][{colIndex}] maxValue = {field.maxValue}")

            # input values
            inputCoordinates = str(input(f"Input the coordinates in format row(0--{self.ySize-1}),col(0--{self.xSize-1}): "))
            # Default input
            if inputCoordinates == "":
                inputCoordinates = "0,0"

            # Normal inputs
            try:
                rowInput, colInput = inputCoordinates.split(",")
                rowInput = int(rowInput)
                colInput = int(colInput)
            except:
                continue

            if rowInput < 0 or rowInput >= self.xSize:
                continue
            if colInput < 0 or colInput >= self.ySize:
                continue
            break

        return rowInput, colInput

    def putChip(self, row, col):
        self.gameBoard[row][col].increaseValue()

    def allowableWaysToExpand(self, row, col):
        """Returns a list of x,y vectors in which is possible to expand"""
        allowableWays = list()

        # check right
        if col < self.xSize - 1:
            allowableWays.append('right')
        if col > 0:
            allowableWays.append('left')
        if row > 0:
            allowableWays.append('up')
        if row < self.ySize - 1:
            allowableWays.append('down')

        if len(allowableWays):
            return len(allowableWays), allowableWays
        else:
            return 0, False

    def expand(self, row, col):
        # depends on location, if on edge or corner, it expands
        # in different manner than if inside the field

        numAllowableWays, allowableWays = self.allowableWaysToExpand(row, col)

        if allowableWays:
            for way in allowableWays:
                if way == 'up':
                    self.gameBoard[row-1][col].increaseValue()
                if way == 'down':
                    self.gameBoard[row+1][col].increaseValue()
                if way == 'left':
                    self.gameBoard[row][col-1].increaseValue()
                if way == 'right':
                    self.gameBoard[row][col+1].increaseValue()


    def stabilizeBoard(self, stability):
        # First find all unstable fields
        row = stability['row']
        col = stability['col']

        # GameField.stabilize()
        self.gameBoard[row][col].stabilize()

        # Expand to neighbours
        self.expand(row, col)

        pass

# FUNCTIONS
def main():

    # Creating a gameboard
    gameBoard = Gameboard()

    # Gameloop
    while not gameBoard.gameOver():
        print(gameBoard.getGameBoard())

        stability = gameBoard.isStable()
        if stability['stability']:
            # user input
            rowInput, colInput = gameBoard.userInput()

            # Play
            gameBoard.putChip(rowInput, colInput)

        else:
            # stabilize the game field
            gameBoard.stabilizeBoard(stability)
            pass


def dummyFunction():

    someList = ['Michal', 'Rudolf', 'Lukas', 'Ivan', 'Mirousek']
    for name in someList:
        print(f"Name: {name}")

    for index, name in enumerate(someList):
        print(f"{index}: {name}")

    return True

    pass


# RUNTIME
if __name__ == "__main__":
    main()