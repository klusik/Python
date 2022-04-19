from random import randint

class Ctverec:
    def __init__(self, a):
        self.strana = a
    def __str__(self):
        return f'Toto je čtverec o délce hrany {self.strana} m, obvodem {self.obvod()} m a obsahem {self.obsah()} m^2.'
    def obvod(self):
        return self.strana*4
    def obsah(self):
        return self.strana**2


# vytvoření slovníku čtverců
pocet_ctvercu = 5
ctverce = {}
for i in range(1,pocet_ctvercu):
    rand_strana = randint(1,20)
    ctverce[rand_strana] = Ctverec(rand_strana)

# vypisování slovníku čtverců
for ctverec in ctverce.values():
    print(ctverec)