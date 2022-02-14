#dalsi pokus najit pokemona v textovem souboru
def pika(cesta, slovo):
    pocitadlo = 0
    txt = open(cesta, 'r')
    while True:
        radka = txt.readline()
        r_c = radka
        while True:
            i = r_c.find(slovo)
          
            #slovo nenalezeno
            if i == -1:
                break
            else:
                pocitadlo +=1
                #novy r_c = r_c[pocatek nalezeneho slova + jeho delka : konec]
                r_c = r_c[i + len(slovo):]
        if r_c == '':
            break
        print pocitadlo
        txt.close()
