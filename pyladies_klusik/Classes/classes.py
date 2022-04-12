""" Napiš třídu čtverec """

class Ctverec:
    pocet_stran = 4
    def __init__(self,
                 delka_strany):
        self.delka_strany = delka_strany

    def vypocti_obvod(self):
        return self.delka_strany * 4

    def vypocti_obsah(self):
        return self.delka_strany ** 2


ctv = Ctverec(10)
Ctverec.pocet_stran = 5

print(ctv.pocet_stran)

print(ctv.vypocti_obvod())
print(ctv.vypocti_obsah())
