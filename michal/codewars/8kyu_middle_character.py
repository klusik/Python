# zadani je, ze program musi najit prostredni znak ve slove.
# Pokud ma slovo lichy pocet znaku, vypise se prostredni znak
# Pokud ma slovo sudy pocet znaku, vypisou se oba prostredni znaky
# je to z ranku 7kyu a jmenuje se to 'get the middle character'

def get_middle(s):
    # your code here
    delka = len(s)
    odd = int((delka / 2) + 0.5)
    even1 = int((delka / 2) - 0.5)
    even2 = int((delka / 2) + 0.5)
    zbytek = delka % 2
    lichy_znak = s[odd]
    sudy_znak1 = s[even1]
    sudy_znak2 = s[even2]
    sudy_vystup = sudy_znak1 + sudy_znak2
    # print(odd, 'je odd', lichy_znak,'je lichy_znak')
    # print(even1,even2)
    if zbytek == 0:
        print('delka zadaneho retezce je', delka)
        return sudy_vystup
    else:
        print('delka zadaneho retezce je', delka)
        return lichy_znak
