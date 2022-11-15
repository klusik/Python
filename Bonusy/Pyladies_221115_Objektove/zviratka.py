"""
    Ukázka tříd
"""


class Zviratko:
    nohy = 4
    zvuk = "haf"
    pohyb = "ťap"

    def nastav_zvuk(self, nastavovany_zvuk):
        self.zvuk = nastavovany_zvuk

# Vyrobení našeho lokálního zvířátka
hafik = Zviratko()
fik = Zviratko()

# Kolik má nohou
print(f"Hafík má {hafik.nohy} nohy.")

# Jaký zvuk vydává
print(f"Hafík vydává zvuk {hafik.zvuk}.")

# Jaký pohyb vykonává
print(f"Hafík se hýbe pohybem, který známe jako {hafik.pohyb}.")

# Změna zvuku
hafik.nastav_zvuk("štěk")
print(f"Hafík změnil svůj zvuk na {hafik.zvuk}.")

print(hafik.zvuk, fik.zvuk)

# Pilíře:
# 1. Encapsulation (zapouzření, uzavření, ...)
# 2. Polymorphism (polymorfismus)
# 3. Abstraction (abstrakce)
# 4. Inheritance (dědičnost)

hafik.zvuk = "mňau"
print(hafik.zvuk)

""" Jiný jazyk, pozor """
"""
    class Zviratko() {
        private int nohy = 4
    }
"""


# Vytvoření třídy pro psa a kočku
class Pes(Zviratko):
    def zastekej(self):
        print("Haf")


class Kocka(Zviratko):
    def zamnoukej(self):
        print("Mnau")


alik = Pes()

micka = Kocka()

alik.zastekej()
micka.zamnoukej()
