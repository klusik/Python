class Ctverec():
    def __init__(self, strana):
        self.strana = strana
    def obvod(self):
        print(f"{self.strana*4 }")
    def obsah(self):
        print(f"{self.strana**2 }")
    def rozdil_obsahu(self, jiny_ctverec):
        self.jiny_ctverec = jiny_ctverec
        print(f"{self.strana**2 - self.jiny_ctverec}")
ctverecek = Ctverec(8)
ctverecek.obvod()
ctverecek.obsah()
ctverecek.rozdil_obsahu(36)

ctverecek2 = Ctverec(10)
ctverecek2.obsah()

ctverecek2.rozdil_obsahu(ctverecek)