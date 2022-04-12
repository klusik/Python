""" Napiš třídu čtverec """

class Ctverec:
    def __init__(self,
                 delka_strany):
        self.delka_strany = delka_strany

    def vypocti_obvod(self):
        return self.delka_strany * 4

    def vypocti_obsah(self):
        return self.delka_strany ** 2


ctv = Ctverec(10)

print(ctv.vypocti_obvod())
print(ctv.vypocti_obsah())
