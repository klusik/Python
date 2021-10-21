# caesar decipher
def decipher(message):
    '''
    deciphers given message
    '''
    
    result = {}
    vals = []
    
    # cycle through all possible characters of abc
    for i in range(1,27):
        abece = abc()
        ichar = abece[i]

        # returns following char
        shifted = shift(ichar)
        
        if ichar in result.keys():
            vals.append(shifted)
            result[ichar].append(vals)
        else:
            vals.append(shifted)
            result.update({ichar:vals})
    return result

def abc():
    '''
    defines characters in abc
    '''
    abeceda = ['a', 'b', 'c', 'd','e',
              'f', 'g', 'h', 'i', 'j',
              'k', 'l', 'm', 'n', 'o',
              'p', 'q', 'r', 's', 't',
              'u', 'v', 'w', 'x', 'y',
              'z']
    return abeceda 

def shift(char):
    '''
    takes character from abc() and returns next in line character
    '''
    abece = abc()
    if char in abece:
        out = abece.index('char')
        out = out + 1
        out = abece[out]
        return out
    if char == 'z':
        out = 'a'
        return out


print(decipher('kokot'))