"""

    A library containing encode and decode methods

"""

# IMPORTS #

# CLASSES #
class ConversionTable:
    table = {
        'a':'.-',
        'b':'-...',
        'c':'-.-.',
        'd':'-..',
        'e':'.',
        'f':'..-.',
        'g':'--.',
        'h':'....',
        'i':'..',
        'j':'.---',
        'k':'-.-',
        'l':'.-..',
        'm':'--',
        'n':'-.',
        'o':'---',
        'p':'.--.',
        'q':'--.-',
        'r':'-.-',
        's':'...',
        't':'-',
        'u':'..-',
        'v':'...-',
        'w':'.--',
        'x':'-..-',
        'y':'-.--',
        'z':'--..',
    }

    @staticmethod
    def get_morse(ascii):
        """ Returns a morse code """
        if ConversionTable.table[ascii]:
            return ConversionTable.table[ascii]
        else:
            return 'X'

    @staticmethod
    def get_ascii(morse):
        """ Returns ascii character """
        if ConversionTable.table.keys()[morse]:
            return ConversionTable.keys()[morse]
        else:
            return 'X'

class Morse:
    """ Morse class """
    def __init__(self,
                 message, # A message to encode or decode
                 ):
        self.message = message

    def encode(self):
        """ Encoding a message to Morse, returns a morse code """
        output = list()
        for character in self.message:
            output.append(ConversionTable.get_morse(character))

        return " ".join(output)

    def decode(self):
        """ Decoding a message in Morse, returns a string """
        output = list()
        encoded = str(self.message).split()
        for morse in encoded:
            output.append(ConversionTable.get_ascii(morse))

        return "".join(output)

    # sdlůfkja sůldf 




# RUNTIME #