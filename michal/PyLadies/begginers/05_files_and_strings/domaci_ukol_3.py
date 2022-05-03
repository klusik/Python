'''
Výzva  Napiš funkci, která v zadaném řetězci zamění první písmeno za velké.
Obdobně můžeš zkusit jiné záměny, např. poslední písmeno, třetí písmeno, atd.
'''

def Uppermaker(sStrng, iPosition):
    '''
    Split given string at defined index into three parts, convert middle
    part using upper(), concatenate all three parts. Return result. If
    given position is too big or too low, return error message.

    INPUT
    strng - input user defined string, string
    iPosition - index number of string to be converted to upper, integer

    sResult - output string, string
    '''

    # handle exception :)
    if iPosition > len(sStrng) \
        or iPosition < -len(sStrng):
        print('given iPosition is too small/big')

    sBefore_position = sStrng[:iPosition]
    sThe_string = sStrng[iPosition].upper()
    # EXAMPLE:           position
    # len(s) = 10 -> 10 - 7 = 3 => -3 +1 >>> sAfter_position[-3:]
    sAfter_position = sStrng[-(len(sStrng) - iPosition)+1:]

    sResult = sBefore_position + sThe_string + sAfter_position

    return sResult

# RUNTIME
print(Uppermaker('Bleeding me', 9))