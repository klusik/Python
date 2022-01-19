# Codewars -- notes

# FUNCTIONS #
def toneShift(pitch, octave):
    """Returns a relative pitch shift from 'a' of given tone 'tone' """
    tones = dict({
        "A"     : 0,
        "A#"    : 1,
        "Bb"    : 1,
        "B"     : 2,
        "C"     : -9,
        "C#"    : -8,
        "D"     : -7,
        "D#"    : -6,
        "E"     : -5,
        "F"     : -4,
        "F#"    : -3,
        "G"     : -2,
        "G#"    : -1,
    })

    exponent = tones.get(pitch) + (octave-1)*12

    return 440 * ( 2 ** (exponent/12))



def parseTone(tone):
    """ Returns pitch, octave """

    alreadyInNumbers = False
    pitch = list()
    octave = list()

    for charIndex, character in enumerate(str(tone)):
        if str(character).isdigit():
            # We are in the realm of octaves
            alreadyInNumbers = True

        # If not number, assume it's a pitch value
        if not alreadyInNumbers:
            pitch.append(character)
        else:
            octave.append(character)


    return "".join(pitch), int("".join(octave))

# RUNTIME #
def main():
    """ Main function """

    while True:
        tone = str(input("Input any note in format TO, where T is tone, O is octave, "
                         "e.g. A#3 means A sharp, 3rd octave. Enter 'bye' for exit: "))

        if tone == "bye":
            break

        pitch, octave = parseTone(tone)

        print(f"We have a tone {pitch} with octave {octave}.")

        print(f"Frequency of that tone is {toneShift(pitch, octave)}.")



if __name__ == "__main__":
    main()