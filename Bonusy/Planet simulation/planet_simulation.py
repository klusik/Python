"""
    Planet simulation

    Based on video: https://www.youtube.com/watch?v=WTLPmUHTPqo

"""

# IMPORTS #
import pygame

# RUNTIME #
def main():
    """ Main function """

    # config

    WIDTH, HEIGHT = 800, 800
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Planets")

    # Event loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()
