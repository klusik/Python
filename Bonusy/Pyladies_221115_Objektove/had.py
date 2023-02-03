"""
    Had objektově
"""


# CLASSES #
class GameBoard:
    """ Square game board for the snake game """

    def __init__(self,
                 board_size: int = 10,
                 ):
        # PROPERTIES #
        self.board_size = board_size

        # Prepare an empty object
        self.game_board = str()

        # INIT #
        self.snake = Snake()

        self.create_game()

    def create_game(self) -> list:
        """ Creates a game board """
        self.game_board = '.' * (self.board_size ** 2)

        # Placing the snake
        # Snake head

        # Snake body
        for snake_part in self.snake.get_body():
            pass

    def show_game_board(self) -> str:
        """ Shows a game board """
        for cell_index, cell in enumerate(self.game_board):
            # Display a line
            print(cell, end=' ')

            # New line
            if not ((cell_index + 1) % self.board_size):
                print()

        return self.game_board

    def move(self) -> str:
        """ """
        while True:
            move_direction = input("Which way [wsad/exit]? ")

            if move_direction in ['w', 's', 'a', 'd', 'exit']:
                if move_direction == 'w':
                    pass
                elif move_direction == 's':
                    pass
                elif move_direction == 'a':
                    pass
                elif move_direction == 'd':
                    pass
                else:
                    break

    def recompute(self):
        """ Recompute a game board (apply snake changes etc.) """


class Snake:
    """ Snake itself """

    def __init__(self):
        # PROPERTIES #
        self.direction = 'w'
        self.body = [(0, 1), (0, 2)]
        self.head = (5, 5)

    @property
    def length(self) -> int:
        """ Returns length of a snake """
        return len(self.body)

    def change_direction(self,
                         direction: str,
                         ):
        self.direction = direction
        return direction

    def get_body(self):
        return self.body


# RUNTIME #
def main():
    # Create a game board
    game = GameBoard()

    game.show_game_board()


if __name__ == "__main__":
    main()
