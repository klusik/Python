# Privat -- old board game

# Cofig

gameBoardResolution = 5


# Game array initialization
gameBoard = []
for i in range (0, gameBoardResolution):
    gameBoardRow = []
    for j in range(0, gameBoardResolution):
        gameBoardRow. append(0)
    gameBoard.append(gameBoardRow)


# Printing the game board
def renderGameBoard():
    for row in range(0, gameBoardResolution):
        for column in range(0, gameBoardResolution):
            print(f"{gameBoard[row][column]} ", end='')
        print("")

# Checking if nothin is explodable
def checkExplosiveness():
    for row in range(0, gameBoardResolution):
        for column in range(0, gameBoardResolution):
            pass

# Gameloop
while True:
    renderGameBoard()
    while True:
        playerColumn = int(input("Sloupec: "))
        if playerColumn < 1: continue
        if playerColumn > gameBoardResolution: continue
        break

    while True:
        playerRow = int(input("Radek: "))
        if playerRow < 1: continue
        if playerRow > gameBoardResolution: continue
        break


    # add a stone to that address
    gameBoard[playerRow-1][playerColumn-1] = gameBoard[playerRow-1][playerColumn-1] + 1

    # check


