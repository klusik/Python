def isUpper(someString):
    """Returns True if all is uppercase"""
    isUpper = False

    aOrd = ord('a')
    zOrd = ord('z')

    for character in someString:
        charOrd = ord(character)

        if ord(character) >= aOrd and ord(character) <= zOrd:
            return(False)
        else:
            continue

    return(True)

someString = "ABD CAD #Đ[đĐ á F"
print(isUpper(someString))