"""Simulation of an ecosystem"""

# IMPORTS
import logging

# CLASSES

class Ecosystem:
    def __init__(self):
        pass

class Herbivore:
    pass

class Omnivore:
    pass

class Predator:
    pass

class Human:
    pass

# CONFIG
logging.basicConfig(level=logging.INFO)

# RUNTIME
def main():
    try:
        # Creating an ecosystem playground
        ecosystem = Ecosystem()
    except Exception as exception:
        logging.info(f"Ecosystem failed:\n{exception}")
    finally:
        print("That's all :-)")

if __name__ == "__main__":
    main()
