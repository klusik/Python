"""
    Kód vysvětlující properties v objektovém programování.
"""


class Uzivatel:
    def __init__(self,
                 jmeno,
                 prijmeni,
                 ):
        """
        Vytváření uživatele
        :param jmeno: Jméno uživatele
        :param prijmeni: Příjmení uživatele
        """

        # Nastavíme hodnoty instance:
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.email = f"{jmeno}.{prijmeni}@klusik.cz"

    def cele_jmeno(self):
        """
            Vrátí celé jméno uživatele
        :return: str
        """
        return f"{self.jmeno} {self.prijmeni}"


# Vyrobíme tedy uživatele, který bude mít nějaké jméno:

pepa = Uzivatel("Josef", "Dvorak")

# Zobrazíme si informace o uživateli
print(f"Křestní jméno uživatele: {pepa.jmeno}")
print(f"Celé jméno uživatele: {pepa.cele_jmeno()}")
print(f"Email uživatele: {pepa.email}")

# Teď změníme jméno uživatele:
pepa.jmeno = "Jiri"

# Vypíšeme zase hodnoty
print(f"Křestní jméno uživatele: {pepa.jmeno}") # Vidíme, že jméno to změnilo
print(f"Celé jméno uživatele: {pepa.cele_jmeno()}") # Vidíme, že metoda se na to jméno odkazuje a změní to taky
print(f"Email uživatele: {pepa.email}") # Tady ale vidíme, že email se vyrobil už před tím a tohle ho nezměnilo

# A vidíme, že "to není ono" :-) Jak to tedy udělat, aby to 'bylo ono'?
# To se dozvíte v souboru properties_reseni.py