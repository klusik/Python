"""
1-D piškvorky se hrají na řádku s dvaceti políčky. Hráči střídavě přidávají kolečka (`o`) a křížky (`x`), třeba:
1. kolo: -------x------------
2. kolo: -------x--o---------
3. kolo: -------xx-o---------
4. kolo: -------xxoo---------
5. kolo: ------xxxoo---------
Hráč, která dá tři své symboly vedle sebe, vyhrál.
Pro usnadnění orientace v celém projektu jsme připravili kostru, kterou najdeš tady

7.☜

Napiš funkci vyhodnot, která dostane řetězec s herním polem 1-D piškvorek a vrátí jednoznakový řetězec podle stavu hry:

"x" – Vyhrál hráč s křížky (pole obsahuje "xxx")
"o" – Vyhrál hráč s kolečky (pole obsahuje "ooo")
"!" – Remíza (pole neobsahuje "-", a nikdo nevyhrál)
"-" – Ani jedna ze situací výše (t.j. hra ještě neskončila)

"""
# IMPORTS #
import random

# CLASSES #
class Config:
    # Default gameboard size
    default_game_size = 20

class Game:
    def __init__(self,
                 size = Config.default_game_size, # Default game size
                 ):
        # Game size
        self.size = size

        # Player pool
        self.players = list()

    def finished(self):
        """ Checks if the game is finished or not.
            Returns True if it is, False if not. """
        return False

    def add_player(self,
                   name=None,  # set up a name if you want
                   count_of_players=1,  # Append more players (batch adding)
                   ):
        """ Adds players (default 1) """
        for _ in range(count_of_players):
            self.players.append(Player(name))

    def play(self):
        """ Player plays his/her turn """
        turn = random.randrange(0, 20)


class Player:
    def __init__(self,
                 name=None, # Define own name if you want
                 ):
        self.name = name

# RUNTIME #
def game():
    """ Main runtime """

    # Create a gameboard
    game_board = Game(size=20)

    # Create players
    game_board.add_player(count_of_players=2)


    while not game_board.finished():
        """ Do game :-) """



if __name__ == "__main__":
    game()