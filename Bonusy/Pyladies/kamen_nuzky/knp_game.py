"""
    Hra kámen nůžky papír trošku rozepsaněji :-P

    Author: Rudolf Klusal
"""

# IMPORTS #
import random  # For random things


# CLASSES #
class Game:
    """
        Individual games
    """

    def __init__(self):
        # Game moves history
        self.game_moves_history = []  # List containing tuples as (user_move, ai_move, winner)

        # Game statistics
        self.user_wins = 0
        self.ai_wins = 0
        self.draws = 0

    def add_game(self, user_move, ai_move, winner):
        self.game_moves_history.append(
            (user_move, ai_move, winner)
        )

        if winner == "u":
            self.user_wins += 1
        elif winner == "p":
            self.ai_wins += 1
        else:
            self.draws += 1

    def get_statistics(self, end_game: bool = False):
        """
        Outputs a staistics.

        If end_game is True, displays more detailed statistics
        @return: String containing statistics
        """

        output = ""

        if end_game:
            output += f"Detailní statistika:\n{60 * '#'}\n"
            for game_round, game in enumerate(self.game_moves_history):
                output += f"Kolo: {game_round + 1}: {game[0]} proti {game[1]}, {'vyhrál uživatel' if game[2] == 'u' else 'remíza' if game[2] == 'd' else 'vyhrál počítač'}\n"

            output += f"{60 * '#'}\n"

            output += f"Vítězných her: {self.user_wins}\n"
            output += f"Proher:        {self.ai_wins}\n"
            output += f"Remízy:        {self.draws}\n"
        else:
            output += f"Vítězných her: {self.user_wins}\n"
            output += f"Proher:        {self.ai_wins}\n"
            output += f"Remízy:        {self.draws}\n"

        return output


class App:
    """
        Main app class
    """

    def __init__(self):
        # Possible game moves
        self.game_moves = [
            # first column is an object, second column is what this object wins over to
            ["kámen", "nůžky"],
            ["nůžky", "papír"],
            ["papír", "kámen"],
        ]

        # Games history
        self.game_history = Game()

    def _ai_move(self) -> str:
        """
        Computer move
        @return: One of valid words from a list of valid words
        @rtype: str

        """
        return random.choice([word[0] for word in self.game_moves])

    def _winning_logic(self, user_input: str, ai_move: str) -> str:
        """

        @param user_input:
        @param ai_move:
        @return: "u" for user won, "p" for pc won, "d" for a draw
        @rtype: str
        """
        for moves in self.game_moves:
            if user_input == moves[0]:
                if ai_move == moves[1]:
                    # User win
                    return "u"
                elif ai_move == user_input:
                    # Draw
                    return "d"
                else:
                    # PC win
                    return "p"

    def play(self):
        """
        Play the game
        @return: None
        """

        # Main game loop
        try:
            while True:
                # User input
                user_input = input("Zadej kámen, nůžky nebo papír jako tvůj tah (konec pro konec): ")

                # Checking if valid options
                if not any(user_input == move[0] for move in self.game_moves):
                    if user_input == "konec":
                        # Ending the game
                        print("Končím hru.")

                        # Outuput some good info
                        print(self.game_history.get_statistics(end_game=True))

                        # Exit the app
                        exit()
                    else:
                        # Invalid move
                        print("Neplatný tah, zkus znovu.")
                        continue

                # If valid user input, let the computer play
                ai_move = self._ai_move()

                # Decide about winning
                winner = self._winning_logic(user_input, ai_move)

                # Print a winner and save to history of games
                if winner == "p":
                    print(f"Vyhrál počítač, tvůj tah {user_input} proti počítače {ai_move}.")
                elif winner == "u":
                    print(f"Vyhrál jsi nad počítačem s tahem {user_input} proti počítače {ai_move}.")
                else:
                    print(f"Je to remíza, oba jste hádali {user_input}.")

                # Print some statistics
                self.game_history.add_game(user_input, ai_move, winner)
                print(f"Stav her je po této hře:\n{self.game_history.get_statistics()}")


        except KeyboardInterrupt as kb_err:
            print("\n\nNatvrdo ukončuji.\n", kb_err)
            exit()


# RUNTIME #
if __name__ == "__main__":
    # Create a game
    game = App()

    # Play the game
    game.play()
