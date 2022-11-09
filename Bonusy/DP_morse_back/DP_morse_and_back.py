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


vyraz = "Bylo nás 5."
vysl = do_morse(vyraz)
print(vysl)