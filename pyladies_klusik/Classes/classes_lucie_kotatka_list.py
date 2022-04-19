class Ctverec:
    def __init__(self, strana):
        self.strana = strana

    def obvod(self):
        obvod = self.strana * 4
        return obvod

    def obsah(self):
        obsah = self.strana ** 2
        return obsah

    def rozdil_obsahu(self, jiny_ctverec):
        rozdil_obsahu = self.obsah() - jiny_ctverec.obsah()
        return rozdil_obsahu

ctverec = Ctverec(5)

print("obvod je", ctverec.obvod())
print("obsah je", ctverec.obsah())
print("rozdil obsahu ctverců je", ctverec.rozdil_obsahu(Ctverec(4)))