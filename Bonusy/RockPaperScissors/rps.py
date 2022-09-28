"""
    Basic RPS game
"""
# IMPORTS #
import random


# RUNTIME #
def match(winning_points,  # Number of points necessary to win
          ):
    """ Main game """

    points_ai = 0  # AI points
    points_user = 0  # User points

    # Valid moves
    moves = ['R', 'P', 'S']
    moves_d = {
        'R': 'rock',
        'P': 'paper',
        'S': 'scissors',
    }

    while abs(points_ai - points_user) < winning_points:
        """ Run the game rounds until the game is not won (or lost) """
        move_ai = random.choice(moves)
        str_move_user = ""

        print('\n')
        print('=' * 60)
        while str_move_user.upper() not in moves:
            str_move_user = input("(Case insensitive) R (Rock), P (Paper) or S (Scrissors)?: ").upper()

        print(f"AI played {moves_d[move_ai]}, player {moves_d[str_move_user]}.")

        # Point counts
        if move_ai == str_move_user:
            # NO points
            print("No points won.")
            continue

        if (move_ai == 'S' and str_move_user == 'P') \
                or (move_ai == 'P' and str_move_user == 'R') \
                or (move_ai == 'R' and str_move_user == 'S'):
            points_ai += 1
            print(f"AI won this round.\tScore {points_user}:{points_ai} (Player:AI)")
        else:
            points_user += 1
            print(f"Player won this round. \tScore {points_user}:{points_ai} (Player:AI)")

    print("\n")
    if points_user > points_ai:
        print(f"The winner is Player with {points_user}. AI lost with {points_ai}.")
    else:
        print(f"The winner is AI with {points_ai}. Player lost with {points_user}")


def rps():
    # Winning points necessary to win
    winning_points = 0

    # Input numbers until user put valid number
    while winning_points <= 0:
        winning_points = int(input("Target winning point difference: "))

    # The Game
    match(winning_points)


if __name__ == "__main__":
    rps()
