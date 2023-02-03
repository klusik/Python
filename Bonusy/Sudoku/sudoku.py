"""
    My attempt to do a sudoku :-)
"""


# IMPORTS #

# CLASSES #
class Game:
    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()

        print(self.player1, self.player2)


class Player:
    def __repr__(self):
        return str(self.__class__.__name__)


# RUNTIME #
if __name__ == "__main__":
    game = Game()
