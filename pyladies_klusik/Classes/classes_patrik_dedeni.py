from math import sqrt, pi


class Obrazec:
    def __init__(self, a):
        self.strana = a

    def __str__(self):
        return f'Moje strana je {self.strana} m, můj obvod {self.obvod()} m a obsah {self.obsah()} m^2.'

    def obvod(self):
        pass

    def obsah(self):
        pass

    def rozdil(self, jiny_obrazec):
        return jiny_obrazec.obsah() - self.obsah()


class Ctverec(Obrazec):
    def obvod(self):
        return self.strana * 4

    def obsah(self):
        return self.strana ** 2


class Trojuhelnik(Obrazec):
    def obvod(self):
        return self.strana * 3

    def obsah(self):
        return self.strana ** 2 * sqrt(3) / 4


class Kruh(Obrazec):
    def obvod(self):
        return self.strana * 2 * pi

    def obsah(self):
        return self.strana ** 2 * pi


novy_kruh = Kruh(3)
novy_ctverec = Ctverec(3)
print(novy_kruh.rozdil(novy_ctverec))
print(novy_ctverec)
print(novy_kruh)