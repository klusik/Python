"""
    Guess what's it doing (run it and try it) :-)

    Author: klusik@klusik.cz
"""

# CLASSES #
class Values:
    numbers = {
        '0': 1,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0,
        '6': 1,
        '7': 0,
        '8': 2,
        '9': 1,
    }


# RUNTIME #
if __name__ == "__main__":
    input_value = str(input("Enter the natural number (n>=1): "))

    counter = 0

    for character in input_value:
        counter += int(Values.numbers[character])

    print(f"Result: {counter}")


