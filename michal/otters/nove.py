#zadani:
#vypocitej, kolikrat se hledane slovo nachazi v textovem souboru
#vstup: hledane slovo, prohledavany soubor
#vystup: pocet vyskytu hledaneho slova

#nejdrive definuji funkci, ktera provadi cely program

def program (soubor, slovo):
    #promena pro nacitani vyskytu slova
    carka = 0
    
    #jako prvni nacteme soubor, se kterym budeme pracovat do promenne
    f_b = open(soubor, 'r')
    
    #cyklus, ktery bude probihat do konce souboru
    for radek in f_b:
        carka = carka + spocitej_vyskyt_na_radce(radek, slovo)   
           
    f_b.close()
    return carka


def spocitej_vyskyt_na_radce (radek, slovo):
    carka = 0
    while True:
        pozice = radek.find(slovo)
        
        if pozice == -1:
            return carka
            
        carka += 1
        radek = radek[pozice+len(slovo):]
