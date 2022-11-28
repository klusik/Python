"""
    Kód vysvětlující properties v objektovém programování.

    Změny jsou okomentované :-)
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
        # self.email = f"{jmeno}.{prijmeni}@klusik.cz" # Proč je zakomentováno se dozvíte níže

    # Nejdříve k tomu emailu, aby se měnil v momentě, co potřebujeme
    # Jako první krok vyrobíme metodu, která se bude jmenovat tak, jako
    # hodnota (email), kterou chceme dostat.
    # Kdybychom však měli metodu, v programu bychom to museli volat
    # třeba jako pepa.email() ale chceme se odkazovat pouze na
    # pepa.email (bez závorek).
    #
    # K tomu slouží právě @property dekorátor! A samozřejmě
    # pak ani nebudeme potřebovat atribut self.email výše.
    @property
    def email(self):
        return f"{self.jmeno}.{self.prijmeni}@klusik.cz"

    # Stejným způsobem můžeme upravit i metodu cele_jmeno, v kodu pak
    # se neodkazujeme jako pepa.cele_jmeno(), ale jen pepa.cele_jmeno.
    @property
    def cele_jmeno(self):
        """
            Vrátí celé jméno uživatele
        :return: str
        """
        return f"{self.jmeno} {self.prijmeni}"

    @cele_jmeno.setter
    def cele_jmeno(self, cele_jmeno:str):
        """ Ano, vyrobím metodu, která se jmenuje stejně jako předchozí,
            jen ji dám dekorátor se jménem té metody """

        # Tím, že udělám "setter," říkám, že metoda nastavuje nějaké hodnoty.
        jmeno, prijmeni = cele_jmeno.split()
        self.jmeno = jmeno
        self.prijmeni = prijmeni

        # Program tedy nastaví tyto hodnoty a tím, že je to "property" se
        # pak všechno dynamicky počítá při volání a hodnoty nezůstávají na
        # starších verzích hodnot :-)

# Vyrobíme tedy uživatele, který bude mít nějaké jméno:

pepa = Uzivatel("Josef", "Dvorak")

# Zobrazíme si informace o uživateli
print(f"Křestní jméno uživatele: {pepa.jmeno}")
print(f"Celé jméno uživatele: {pepa.cele_jmeno}")
print(f"Email uživatele: {pepa.email}")

# Teď změníme jméno uživatele:
pepa.jmeno = "Jiri"

# Vypíšeme zase hodnoty
print(f"Křestní jméno uživatele: {pepa.jmeno}") # Vidíme, že jméno to změnilo
print(f"Celé jméno uživatele: {pepa.cele_jmeno}") # Vidíme, že metoda se na to jméno odkazuje a změní to taky
print(f"Email uživatele: {pepa.email}") # Tady ale vidíme, že email se vyrobil už před tím a tohle ho nezměnilo

# Dále budu chtít třeba použít atribut .cele_jmeno na změnění hodnoty!
pepa.cele_jmeno = "Rudolf Klusal" # Normálně by to nešlo, ale tím, jak to nastavíme ve třídě, už to půjde

# Nakonec opět zobrazím hodnoty:
print(f"Křestní jméno uživatele: {pepa.jmeno}") # Vidíme, že jméno to změnilo
print(f"Celé jméno uživatele: {pepa.cele_jmeno}") # Vidíme, že metoda se na to jméno odkazuje a změní to taky
print(f"Email uživatele: {pepa.email}") # Tady ale vidíme, že email se vyrobil už před tím a tohle ho nezměnilo
