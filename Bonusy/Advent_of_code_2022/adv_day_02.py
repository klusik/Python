"""
Advent of Code[About][Events][Shop][Settings][Log Out]Rudolf Klusal 2*
  {year=>2022}[Calendar][AoC++][Sponsors][Leaderboard][Stats]
Our sponsors help make Advent of Code possible:
Kotlin by JetBrains - Trees, lists, packages - it's Advent of Code time! Get ready to solve puzzles in Kotlin. Watch us livestream our discussions about the solutions for the first few puzzles, join our leaderboard, win prizes. Happy holidays!
--- Day 2: Rock Paper Scissors ---
The Elves begin to set up camp on the beach. To decide whose tent gets to be closest to the snack storage, a giant Rock Paper Scissors tournament is already in progress.

Rock Paper Scissors is a game between two players. Each game contains many rounds; in each round, the players each simultaneously choose one of Rock, Paper, or Scissors using a hand shape. Then, a winner for that round is selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock. If both players choose the same shape, the round instead ends in a draw.

Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) that they say will be sure to help you win. "The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.

The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors. Winning every time would be suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score. Your total score is the sum of your scores for each round. The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you, you should calculate the score you would get if you were to follow the strategy guide.

For example, suppose you were given the following strategy guide:

A Y
B X
C Z
This strategy guide predicts and recommends the following:

In the first round, your opponent will choose Rock (A), and you should choose Paper (Y). This ends in a win for you with a score of 8 (2 because you chose Paper + 6 because you won).
In the second round, your opponent will choose Paper (B), and you should choose Rock (X). This ends in a loss for you with a score of 1 (1 + 0).
The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.
In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

What would your total score be if everything goes exactly according to your strategy guide?

To begin, get your puzzle input.

Answer:


You can also [Share] this puzzle.
"""


# RUNTIME #
def main():
    # Input file handling
    try:
        with open('adv_day2_elves.txt', 'r') as f_elves:
            elves = f_elves.read()
    except FileNotFoundError as err:
        print(f"File doesn't exist: {err}")
        exit(1)

    # Game points
    rock = 1
    paper = 2
    scissors = 3

    # Win/lose points
    win = 6
    lose = 0
    draw = 3

    # Possible outcomes
    scores = {
        'A X': rock + draw,
        'A Y': paper + win,
        'A Z': scissors + lose,
        'B X': rock + lose,
        'B Y': paper + draw,
        'B Z': scissors + win,
        'C X': rock + win,
        'C Y': paper + lose,
        'C Z': scissors + draw,
    }

    things = {
        'A': rock,
        'B': paper,
        'C': scissors,
    }

    wins = {  # for key wins value over key,
        'A': 'B',  # paper packs rock
        'B': 'C',  # scissors cut paper
        'C': 'A',  # rock dull scissors
    }

    loses = {  # loses are 'vopáčně' :-D
        'B': 'A',  # rock loses to paper
        'C': 'B',  # paper loses to scissors
        'A': 'C',  # scrissors loses to rock
    }

    # PART 1 #
    # Counter init
    my_score = 0

    # Go through all games
    for game in elves.split('\n'):
        my_score += scores[game]

    # Pring a result of PART 1 #
    print(my_score)

    # PART 2 #
    my_score = 0
    for game in elves.split('\n'):
        opponent, you = str(game).split()[0], str(game).split()[1]

        # X means you need to lose, Y means you need to end
        # the round in a draw, and Z means you need to win.

        if you == 'X':  # lose
            your = loses[opponent]
            my_score += lose + things[your]
        elif you == 'Y':  # draw
            your = opponent
            my_score += draw + things[your]
        else:  # win
            your = wins[opponent]
            my_score += win + things[your]

    print(my_score)
    return my_score


if __name__ == "__main__":
    main()
