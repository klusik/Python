# zde deklaruji novou tridu
# slouzi jako blueprint pro vsechna zvirata
# = vsechna zvirata jsou vyrobena podle teto tridy
class Zvire:
    # zde muzu psat konstanty, tedy zakladni nemenne vlastnosti potomku tridy
    barva = 'zelena'
    # jako prvni vytvorim specialni metodu, rikejme ji konstruktor
    # v teto metode si urcim promenne, ktere budou znami napric tridou Zvire
    # self je odkaz na instanci tridy, vysvetlim dale
    def __init__(self, sirka, vyska, delka, vaha, zvuk):
            # diky self se z parametru funkce __init__
            # stane promenna instance tridy
            # self tedy priradi zadanou promenou pri runtimu instanci tridy
            # instance znamena, ze se z blueprintu stane nejake realne zvire
            # a instancni promenna se priradi diky self ke konretni instanci
            # jina instance odvozena od zvirete pak muze mit jinou hodnotu
            # instancnich promennych
            self.sirka = sirka
            print(f'byla zadana sirka {sirka} cm')
            
            self.vyska = vyska
            print(f'byla zadana vyska {vyska} cm')
            
            self.delka = delka
            print(f'byla zadana delka {delka} cm')
            
            self.vaha = vaha
            print(f'byla zadana hmotnost {vaha} kg')
            
            self.zvuk = zvuk
            print(f'byl zadan zvuk zvirete {zvuk}')
    
    # zde si definuji metody
    # ty davaji tride schopnosti
    def roste (self, koeficient_rustu):
        self.sirka = self.sirka * koeficient_rustu
        self.vyska = self.vyska * koeficient_rustu
        self.delka = self.delka * koeficient_rustu
        self.vaha = self.vaha * koeficient_rustu
        print(f' zvire ztloustlo\n nova sirka je {self.sirka}cm\n nova vyska je {self.vyska}cm\n nova delka je {self.delka}cm\n nova hmotnost je {self.vaha}kg')

    def vymesuje(self, exkrement_hmotnost):
        new_hmotnost = self.vaha - exkrement_hmotnost
        print(f'zvire se pokakalo, nova hmotnost je {new_hmotnost}')

    def delaZvuk(self):
        print(self.zvuk)

    def zmenBarvu():
        barva = Zvire.barva
        
        print(f'nova barva {barva}')
# =============================================================================
# v teto chvili jsem hotov s bluepritnem
# tedy chci, aby moje trida vratila svoji instanci = konkretni zvire, nikoliv nejake obecne zvire

# vystup si musim ulozit, jinak program vykona instrukce a vystup zahodi
pes = Zvire(20,45,30,10,'Wuf')

pes.roste(1.1)
pes.DelaZvuk()
pes.vymesuje(1)

medved = Zvire(200, 330, 90, 880, 'Wrrrrrrrrr')
medved.roste(1.3)
medved.DelaZvuk()
medved.vymesuje(5)

