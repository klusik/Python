"""
    Game of Farkle with 6 dices

    RULES:
        (TODO later)
"""

# IMPORTS #
import random


# CLASSES #
class Config(object):
    # Winning condition
    points_to_win = 4000

    # Points of different combinations
    points = {
        1: 100,
        5: 50,
        111: 1000,
        1111: 2000,
        11111: 3000,
        111111: 4000,
        555: 500,
        5555: 1000,
        55555: 1500,
        555555: 2000,
        222: 200,
        2222: 400,
        22222: 600,
        222222: 800,
        123456: 1000,
        333: 300,
        3333: 600,
        33333: 900,
        333333: 1200,
        444: 400,
        4444: 800,
        44444: 1200,
        444444: 1600,
        666: 600,
        6666: 1200,
        66666: 1800,
        666666: 2400,
    }


class Player(object):
    def __init__(self,
                 name=None,  # Name of player
                 points=0,  # Accumulated points
                 ):
        # Basic setup
        self.name = name
        self.points = points


class Game(object):
    def __init__(self):

        # Players pool
        self.players = []

        # Create players
        player_number = 1
        while len(self.players) < 2:
            player_name = input(f"Enter the player {player_number} name: ")
            self.players.append(Player(name=player_name))

            player_number += 1

        # Create game setup
        self.max_points = Config.points_to_win  # Read from Config

    @staticmethod
    def throw_dices(locked_dices=None,  # A list of locked dices (index)
                    previous_dices=None,  # A previous throw
                    ) -> list:  # Returns a list
        """ Throw dices, return a list of thrown dices """
        dices = []

        for dice_index in range(6):
            if dice_index not in locked_dices:
                # If an index is not locked
                dices.append(random.randint(1, 6))
            else:
                if previous_dices:
                    dices.append(previous_dices[dice_index])

        return sorted(dices)

    @staticmethod
    def display_dices(dices, locked_dices) -> None:
        """ Print out dices """
        print(locked_dices)
        print(f"Dices: ")
        for dice_index, dice in enumerate(dices):
            locked = "locked" if dice_index in locked_dices else ""
            print(f"{dice_index + 1}: {dice} {locked}")

    @staticmethod
    def input_lock_dices(dices, locked_dices) -> list:
        """ Let the user select the locked dices
        :param locked_dices: previously locked dices
        :param dices: a dices list
        :return: list of locked dices
        """
        locked_dices = input(
            "Write numbers (eg. 124) which you want to lock. "
            "\nLet it empty if you want to finish your move: "
            "\nLock dices: ")

        return [int(item) for item in list(locked_dices)]

    @staticmethod
    def another_throw_possible(dices) -> bool:
        """ Checks if there's another possible throw """

    def play(self) -> None:
        """ Main game """

        # Default setup
        active_player = 0  # Active player (0 || 1)

        locked_dices = []  # A local variable for saved dices for a throw

        # Game loop
        while True:
            # Generate dices throw or rethrow with non-locked dices
            dices = self.throw_dices(locked_dices)
            self.display_dices(dices, locked_dices)

            # Check if a throw is a fail or not

            # User input (locked dices)
            locked_dices = self.input_lock_dices(dices, locked_dices)


# RUNTIME #
def main():
    # Create a new game
    game = Game()

    # Play game
    game.play()


if __name__ == "__main__":
    main()
