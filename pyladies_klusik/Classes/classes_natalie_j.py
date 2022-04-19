class Ctverec():
    def __init__(self, strana):
        self.strana = strana

    def obvod(self):
        return self.strana * 4

    def obsah(self):
        return self.strana ** 2

    def rozdil_obsahu(self, jiny_ctverec):
        return self.obsah() - jiny_ctverec.obsah()


ctverecek = Ctverec(4)
ctverecek.obvod()
ctverecek.obsah()

ctverecek2 = Ctverec(2)

rozdil = ctverecek.rozdil_obsahu(ctverecek2)

ctverecek2 = Ctverec(6)
ctverecek2.obsah()
ctverecek2.rozdil_obsahu(8)