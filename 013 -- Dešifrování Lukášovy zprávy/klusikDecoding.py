# decoding Lukas's message
#

def shiftMessage(message, shift):
    
    shiftedMessage = list(message.strip(" "))
    
    for i in range(0, len(shiftedMessage)):
        if (shiftedMessage[i] == ' '):
            shiftedMessage[i] = ' '
        else:
            shiftedMessage[i] = chr((ord(shiftedMessage[i]) + shift) % 26 + ord('a'))
        
    newMessage = ""    

    for i in range(0, len(shiftedMessage)):
        newMessage += shiftedMessage[i]
    return newMessage


def main():
    message = "rfr afx wfi ad erwin"

    # The goal is trying to add or remove numbers from 1 to 26 
    # and one of the 25 outputs should make sense :-)

    for shift in range(0, 27):
        print(f"{shift} : {shiftMessage(message, shift)}")
        


if (__name__ == "__main__"):
    main()