'''Na srazu jsme vytvářeli cvičné třídy pro koťátka/čtverce
vytvoř seznam alespoň pěti ruzných koťátek/čtverců. 
Dokážeš to udělat v cyklu? Jak ověříš, 
že jde skutečně o různé objekty?
'''
import random

class Ctverec:
    def __init__(self, delka_strany, pocet_stran):
        self.delka_strany = delka_strany
        self.pocet_stran = pocet_stran
        
    def obvod(self):
        print(f'obvod ctverce je {self.pocet_stran * self.delka_strany}')
        return self.pocet_stran * self.delka_strany

    def obsah(self):
        print(f'obsah ctverce je {self.delka_strany * self.delka_strany}')
        return self.delka_strany * self.delka_strany
    
    def rozdil_obsahu(self, jiny_ctverec):
        obsah1 = self.obsah()
        obsah2 = jiny_ctverec.obsah()
        rozdil = obsah1 - obsah2
        print(f'rozdil obsahu je: {rozdil}')
        return rozdil
    
a = Ctverec(3,4)
b = Ctverec(2, 4)
print(a.rozdil_obsahu(b))
    