class Ctverec:
    def __init__(self, a):
        self.strana = a

    def obvod(self):
        return self.strana * 4

    def obsah(self):
        return self.strana ** 2

    def rozdil(cizi_ctverec, self):
        return cizi_ctverec.obsah() - self.obsah()


prvni = Ctverec(4)
druhy = Ctverec(2)

rozdil = prvni.rozdil(druhy)
print(rozdil)
rozdil = druhy.rozdil(prvni)
print(rozdil)
print(druhy.obsah())
print(druhy.obvod())