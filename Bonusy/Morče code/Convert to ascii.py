"""
    Just a decoding stuff
"""

# IMPORTS #
import morse

# RUNTIME #
def main():
    """ Main runtime """
    message = str(input("Enter the morse code message: "))

    m = morse.Morse(message)

    print(m.decode())
    
if __name__ == "__main__":
    main()