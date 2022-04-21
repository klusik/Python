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


seznam_instanci = []

for poradi in range(10):
    instance = Ctverec(poradi, 4)
    obsah = instance.obsah()
    seznam_instanci.append(obsah)

print(seznam_instanci)

""" Super, a jak ověříš, že se jedná skutečně o různé objekty? :-) """

seznam_objektu = []

for poradi in range(10):
    ctverec = Ctverec(random.randrange(1,100), 4)
    seznam_objektu.append(ctverec)

for ctverec in seznam_objektu:
    print(ctverec.obsah())
    print(ctverec.obvod())
    print(id(ctverec))
