"""
    New computer, new Pythong, just a test :-)
"""

# CLASSES #
class User:
    def __init__(self,
                 name,
                 ):
        self._name = name

    def __str__(self):
        return(f"Player: {self._name}")


class Game:
    def __init__(self):
        player = User("klusik")

        print(player)

    def __str__(self):
        return(f"The Game")

# RUNTIME #
if __name__ == "__main__":
    game = Game()
    print(game)