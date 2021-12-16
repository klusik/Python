# https://www.codewars.com/kata/59175441e76dc9f9bc00000f/python

'''
You are a khmmadkhm scientist and you decided to play with electron 
distribution among atom's shells. You know that basic idea of electron 
distribution is that electrons should fill a shell untill it's holding 
the maximum number of electrons.

Rules:

Maximum number of electrons in a shell is distributed with a rule of 2n^2 
(n being position of a shell).
For example, maximum number of electrons in 3rd shield is 2*3^2 = 18.
Electrons should fill the lowest level shell first.
If the electrons have completely filled the lowest level shell, the other 
unoccupied electrons will fill the higher level shell and so on.
'''

# jelikoz jsem dement a nechapu zadani, tak po konzultaci jsem zjistil:
# uzivatel zada nejake cislo 'x'
# pak vypocitam 'z = 2*n^2', kde 'n' je cislo vrstvy ('z = kapacita vrstvy')
# vysledek 'z' odectu od uzivatelem zadaneho cisla 'x' a dostanu 'y'
# opakuji postup pro 'y', dokud 'kapacita vrstvy'  > 'y'
# 

def distributorOfPain(hausnumero):
    # iterator, = cislo vrstvy
    cisloVrstvy = 0
    vystup = []
    zbyleElektrony = hausnumero
    while True:
        cisloVrstvy += 1
        kapacitaVrstvy = 2*cisloVrstvy*cisloVrstvy
        if kapacitaVrstvy < zbyleElektrony:
            vystup.append(kapacitaVrstvy)
        else:
            vystup.append(zbyleElektrony)
            return vystup
            break
            
        
        zbyleElektrony = zbyleElektrony - kapacitaVrstvy
                
print(distributorOfPain(100))
