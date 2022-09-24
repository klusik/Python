"""
    How wine & water dilutes together

    Go from Water to Wine and back
"""

# CONSTANTS #
initial_wine_volume = 1000 # in ml
initial_wine_clarity = 1 # Ratio

initial_water_volume = 1000 # in ml
initial_water_clarity = 1 # Ratio

spoon_size = 10 # in ml
no_of_tries = 10 # 1 means 1 transfer (using spoon twice)


if __name__ == "__main__":
    """ Do stuff """

    water_clarity = initial_water_clarity
    wine_clarity = initial_wine_clarity

    water_volume = initial_water_volume
    wine_volume = initial_wine_volume

    for counter in range(no_of_tries):
        # 1st step -- go from water to wine
        water_volume -= spoon_size

        # Wine is diluted
        wine_volume += spoon_size
        wine_clarity = wine_clarity * (spoon_size/(water_clarity * spoon_size))

        # And back
        wine_volume -= spoon_size
        water_volume += spoon_size

        water_clarity = water_clarity * (spoon_size/(wine_clarity * spoon_size))

        print(f"{counter+1}. try: Water clarity: {water_clarity}, Wine clarity: {wine_clarity}")