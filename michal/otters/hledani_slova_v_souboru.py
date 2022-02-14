#program slouzi k vyhledani slova zadaneho uzivatelem v textovem souboru



#funkce, ktera provede cely program
def cti(cesta, slovo):
    #nacteme soubor do promenne, zamerne neuvadim rezim prace se soubore - default je 'r'
    textak = open(cesta, 'r')

    #zaloha promenne textak
    txt = textak

    #promena pro pocet nalezenych slov
    counter = 0

    #cyklus na prohledavani souboru
    while True:
        radek = txt.readline()
        if radek  == '':
            break
        while True:
            index = radek.find(slovo)
            if index == -1:
                break
            counter +=1
            radek = radek[index+len(slovo):]
    textak.close()
    print ('počet výskutů slova ', slovo, ' je ', counter)
    

