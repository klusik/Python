"""
    Výzva   Napiš program, který simuluje tuto hru:
    První hráč hází kostkou (t.j. vybírají se náhodná čísla od 1 do 6),
    dokud nepadne šestka. Potom hází další hráč, dokud nepadne šestka i jemu.
    Potom hází hráč třetí a nakonec čtvrtý. Vyhrává ten, kdo na hození šestky
    potřeboval nejvíc hodů. (V případě shody vyhraje ten, kdo házel dřív.)

    Program by měl vypisovat všechny hody a nakonec napsat, kdo vyhrál.

    Nápověda: průběžně stačí ukládat jen údaj, kdo vede.

    Author: klusik@klusik.cz
"""

# IMPORTS #
import random


# CLASSES #
class Player:
    """ Player """
    def __init__(self,
                 name):

        # Name of the player
        self.name = name

        # List of throws for this player
        self.throws = list()

    def save_throw(self,
                   throw,  # Number from the dice
                   ):
        """ Saves a new throw to list for this player """
        self.throws.append(throw)


class Game:
    """ Main game """
    def __init__(self,
                 number_of_players,  # Number of players for the game
                 ):

        # Number of players for this game
        self.number_of_players = number_of_players

        # Creating players
        self.players = self.create_players()

    def create_players(self):
        """ Generate players """
        players = list()
        for player_number in range(self.number_of_players):
            # Creates every player

            # Player name is generated
            player = Player(f"Player {str(player_number + 1)}")

            # Player is appended to local list of players
            players.append(player)

        return players

    def display_players(self):
        """ Displays (prints) a list of players and saved throws """
        for player in self.players:
            print(f"Name of player: {player.name}")

            # I am sure there would be other output after that, so end="" is okay
            print("Throws: ", end="")

            # If there are any throws yet, it displays them, otherwise
            # it displays "no throws yet."
            if len(player.throws) > 0:
                for throw in player.throws:
                    print(f"{throw} ", end="")
                print("")
            else:
                print("No throws yet.")

        # Testing winner condition
        if self.all_players_done():
            # Creates a dict of players with name:number of throws
            players = dict()
            for player in self.players:
                players[player.name] = len(player.throws)

            # Sort via value
            sorted_players = sorted(players.items(), key=lambda item: item[1])

            # Language stuff, singular or plural
            if sorted_players[0][1] == 1:
                throws = "throw"
            else:
                throws = "throws"

            # Output message
            print(f"A winner is {sorted_players[0][0]} with {sorted_players[0][1]} {throws}. Player table below.")

            # Print a list of all players and their score
            for player in sorted_players:
                print(f"{player[0]}: {player[1]} throws")

    def all_players_done(self):
        """ Checks scores of all players and return True, if game finished, False otherwise """
        players_done = 0
        for player in self.players:
            if 6 in player.throws:
                players_done += 1

        # If there are all players done, returns True
        return players_done == len(self.players)

    def play(self):
        while not self.all_players_done():
            # Let's play :-)
            for player in self.players:
                # Make throws
                throw = 0
                while throw < 6:
                    throw = random.randint(1, 6)
                    player.save_throw(throw)


# RUNTIME #
if __name__ == "__main__":
    """ Main runtime """

    # Initial value of player count
    number_of_players = 0

    # Ask user until enters valid number
    while number_of_players < 2:
        try:
            number_of_players = int(input("Enter the number of players: "))
        except ValueError:
            print("Bad format of number.")
            number_of_players = 0

    # Creates a new game
    game = Game(number_of_players)

    # Playing the game
    game.play()

    # Showing results
    game.display_players()
