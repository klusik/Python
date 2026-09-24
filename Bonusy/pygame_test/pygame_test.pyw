"""
    Pygame test, I need to learn this module


"""
from typing import Optional

import pygame


class Config:
    # screen
    screen_width = 700
    screen_height = 600

    # basic titles
    window_title = "This is my first game"

    # Window time limit in ms
    window_time_limit = 5000
    clock_tick = 60

    # Fonts
    default_font = None
    default_font_size = 80

    # Colours
    bg_col = (
        50, 50, 50,
    )

    fg_col = (
        100, 150, 100,
    )


class Game:
    """Main game"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (Config.screen_width, Config.screen_height),
            vsync=1,
        )
        pygame.display.set_caption(
            Config.window_title
        )

        self.font = pygame.font.Font(
            Config.default_font, Config.default_font_size
        )

        self.clock = pygame.time.Clock()
        self.start_time: Optional[int] = None
        self.running: bool = True

        self.run()

    def run(self):
        """Main method"""

        # resetting the timer
        self.start_time = pygame.time.get_ticks()


        # Main loop
        while self.running:
            elapsed_time = pygame.time.get_ticks() - self.start_time
            remaining_time = max(0, Config.window_time_limit - elapsed_time)

            # Exit event
            for pygame_event in pygame.event.get():
                if pygame_event.type == pygame.QUIT:
                    self.running = False

            # Setting up the window background
            self.screen.fill(Config.bg_col)

            # Draw text
            fg_text = self.font.render(
                str(round(remaining_time / 1000, 1)),
                True,
                Config.fg_col,

            )
            self.screen.blit(
                fg_text,
                (Config.screen_width // 2, Config.screen_height // 2),
            )

            pygame.display.flip()
            self.clock.tick(Config.clock_tick)

            # Modify remaining time
            if remaining_time <= 0:
                self.running = False


def main():
    game = Game()


if __name__ == "__main__":
    main()
