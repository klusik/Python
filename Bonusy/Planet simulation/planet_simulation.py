"""
    Planet simulation

    Based on video: https://www.youtube.com/watch?v=WTLPmUHTPqo

"""

# IMPORTS #
import pygame

# CLASSES #
class Planet:
    # CONSTANTS

    # Astronomical unit
    AU = 149.6e6 * 1000 # In meters

    # Gravity constant
    G = 6.67428e-11

    # Scale
    SCALE = 250 / AU

    def __init__(self,
                 x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        # Velocities
        self.x_velocity = 0
        self.y_velocity = 0

        # Is the object a central star?
        self.sun = False
        self.distance_to_sun = 0

        # Orbits
        self.orbit = list()

# RUNTIME #
def main():
    """ Main function """

    # config
    WIDTH, HEIGHT = 800, 800
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    # Colours
    WHITE = (255, 255, 255)

    # Caption of the window
    pygame.display.set_caption("Planets")

    # Clock to regulate FPS
    clock = pygame.time.Clock()

    # Event loop
    run = True
    while run:
        # Clock stuff
        clock.tick(60)

        # Background of windows
        WIN.fill(WHITE)

        # Updating a windows
        pygame.display.update()

        # Quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()
