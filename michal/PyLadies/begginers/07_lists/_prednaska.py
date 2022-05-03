'''
Topic: lists
this file is intended as a lecture record 
date: 29.3.2022 (DD.MM.YYYY)
prednasejici: jakub cervinka
'''

# list se zapisuje do hranatych zavorek
# pridat neco do listu se da pomoci append()
# da se pouzivat slicovani
# a mame tady metody pop, remove, sort
# isinstance() ukazuje datovy typ promenne

zaznamy = ['pepa novak', 'Jiri Sladek', 'Ivo navratil', 'jan Polednik']

def vyber_chybne(seznam_jmen):
    vysledek = []
    for jmeno in seznam_jmen:
        krestni_a_prijmeni = jmeno.split()
        krestni = krestni_a_prijmeni[0]
        prijmeni = krestni_a_prijmeni[1]
        if krestni.islower():
            krestni = krestni.capitalize()
        if prijmeni.islower():
            prijmeni = prijmeni.capitalize()
        vysledek.append(str(krestni + ' ' + prijmeni))
    return vysledek

print(vyber_chybne(zaznamy))