"""
    Ukázka tříd
"""


class Zviratko:
    nohy = 4
    zvuk = "haf"
    pohyb = "ťap"

    def nastav_zvuk(self, nastavovany_zvuk):
        self.zvuk = nastavovany_zvuk


hafik = Zviratko()

# Kolik má nohou
print(f"Hafík má {hafik.nohy} nohy.")

# Jaký zvuk vydává
print(f"Hafík vydává zvuk {hafik.zvuk}.")

# Jaký pohyb vykonává
print(f"Hafík se hýbe pohybem, který známe jako {hafik.pohyb}.")

# Změna zvuku
hafik.nastav_zvuk("štěk")
print(f"Hafík změnil svůj zvuk na {hafik.zvuk}.")
