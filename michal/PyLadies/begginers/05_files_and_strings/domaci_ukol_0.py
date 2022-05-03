'''
Napiš program, který se zeptá na příjmení uživatelky/uživatele a zkusí podle
něj uhodnout její/jeho pohlaví.
'''

def gender_detector(sSurename):
    '''
    If last three characters in given string are "ova", return female, 
    else male.

    INPUT
    sSurename - family name, string

    OUTPUT
    sGender - 'male'/'female', string
    '''

    sSurename = sSurename[-3:]

    if sSurename == 'ova' or sSurename == 'ová':
        return 'Female'
    else:
        return 'Male'

# RUNTIME
print(gender_detector('Tichonova'))
