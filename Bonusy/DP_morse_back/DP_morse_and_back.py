"""
    Založeno na kódu Daniela z Pyladies
"""
morse = {
    '0': '-----',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '...',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..'
}


def do_morse(string):
    string = string.upper()
    vysl = ""

    for char in string:

        if char == ' ':
            continue
        elif char == '.':
            vysl += "STOP"
        elif char not in morse:
            vysl += '?'
        else:
            vysl += morse[char]

        vysl += "|"

    return vysl[:len(vysl) - 1]


def do_ascii(morse_convert):
    """ Converts it back to ascii """

    # Check if there's only valid characters
    if not (morse_convert.count("|") + morse_convert.count(".") + morse_convert.count("-") + 4 * morse_convert.count(
            "STOP")) == len(morse_convert):
        print("Divné znaky, přerušuji převod.")

        return False

    # Let's convert
    ascii = ""

    # Split by '|'
    morse_list = morse_convert.split("|")

    # Conversion
    for char in morse_list:
        if char != "STOP":
            ascii += str(list(morse.keys())[list(morse.values()).index(char)])
        else:
            ascii += "."
        
    return ascii


vyraz = "Bylo nas 5."
vysl = do_morse(vyraz)
asci = do_ascii(vysl)

print(vysl)
print(asci)
