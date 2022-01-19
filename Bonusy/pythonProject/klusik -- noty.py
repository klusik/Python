# Codewars -- notes

# FUNCTIONS #
def toneShift(tone):
    """Returns a relative pitch shift from 'a' of given tone 'tone' """

# RUNTIME #
def main():
    """ Main function """

    while True:
        tone = str(input("Input any note in format TO, where T is tone, O is octave, "
                         "e.g. A#3 means A sharp, 3rd octave. Enter 'bye' for exit: "))

        if tone == "bye":
            break

if __name__ == "__main__":
    main()