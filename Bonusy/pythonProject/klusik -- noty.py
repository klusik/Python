# Codewars -- notes

# FUNCTIONS #
def toneShift(tone):
    """Returns a relative pitch shift from 'a' of given tone 'tone' """
    tones = dict({
        "A"     : 0,
        "A#"    : 1,
        "B"     : 2,
        "C"     : 3,
        "C#"    : 4,
        "D"     : 5,
        "D#"    : 6,
        "E"     : 7,
        "F"     : 8,
        "F#"    : 9,
        "G"     : 10,
        "G#"    : 11,
    })

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