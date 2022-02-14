class Ovoce:

    def __init__ (self, jablka, hrusky):
        self.jablka = jablka
        self.hrusky = hrusky
    
    def nastavJablka (self, pocetJablek):
        self.jablka = pocetJablek
        
    def nastavHrusky (self, pocetHrusek):
        self.hrusky = pocetHrusek
        
    def tisk (self):
        print("Pocet jablek :", self.jablka)
        print("Pocet hrusek :", self.hrusky)
        
    def prictiOvoce(self, jineovoce):
        self.jablka = self.jablka + jineovoce.jablka
        self.hrusky = self.hrusky + jineovoce.hrusky

    def __add__(self, other):
        return Ovoce(
            jablka = self.jablka + other.jablka,
            hrusky = self.hrusky + other.hrusky,
        )
        
p = Ovoce (4, 6)
p.tisk()

p2 = Ovoce (4, 6)
p.prictiOvoce(p2)
p.tisk()

(p + p2).tisk()
