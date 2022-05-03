'''
Vygeneruj slovník s libovolným počtem čtverců a různou velikostí strany.
Klíčem slovníku bude velikost jeho strany. Všechny tyto čtverce vypiš
i s jejich obvody a obsahy.

Tato technika (cachování) se používá, když víme, že často budeme potřebovat
objekt se stejným nastavením (stejnými daty). Namísto toho, abychom takovýto
objekt vytvářeli pořád dokola, když ho potřebujeme použít, tak si jej uložíme
bokem a vytáhneme si jej ze slovníku pomocí klíče. Jednak tím ušetříme čas
potřebný k vytvoření objektu a často si ušetříme i paměť.
'''

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

cachedict = {}

for klic in range(100):
    instance = Ctverec(klic, 4)
    obvod = instance.obvod()
    obsah = instance.obsah()
    
    # ulozim si zjistene do dictu
    cachedict[klic] = (id(instance), obvod, obsah)
    
print(cachedict)