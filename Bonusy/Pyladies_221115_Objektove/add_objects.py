"""
    Objekty se dají třeba sčítat
"""


# CLASSES #
class Mesec:
    def __init__(self,
                 obsah: int,
                 ):
        self.__obsah = obsah

    @property
    def obsah(self):
        return self.__obsah

    def __str__(self):
        return f"Mesec obsahuje {self.obsah} penez."

    def __call__(self):
        print(f"Mesec obsahuje {self.obsah} penez.")

    def __add__(self, mesec):
        return Mesec(int(self.obsah) + int(mesec.obsah))


# RUNTIME #
mesec_1 = Mesec(100)
mesec_2 = Mesec(200)

# Objekty se dají i volat (metoda __call__)
mesec_1()
mesec_2()

# A i sčítat (metoda __add__) :-D

mesec_3 = mesec_1 + mesec_2
mesec_3()
