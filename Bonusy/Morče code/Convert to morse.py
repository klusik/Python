"""
    Just a main program
"""

# IMPORTS #
import morse

# RUNTIME #
def main():
    """ Main function """
    message = str(input("Enter the message in ASCII: "))

    m = morse.Morse(message)

    print(m.encode())

if __name__ == "__main__":
    main()