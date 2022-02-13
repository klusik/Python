#chci jenom otevrit soubor
def blb(cesta, slovo):
    pocitadlo = 0
    txt = open(cesta, 'r')


    
    radka = txt.readline()


    
    r = radka.find(slovo)

    
    if r == -1:
        print ('slovo nenalezeno na radce')
        
    else:
        
        pocitadlo +=1
        print pocitadlo
        #print r
        #print r+len(slovo)
        new_string = radka[r+len(slovo):] #nefunguje slicing notace
        return radka
        
