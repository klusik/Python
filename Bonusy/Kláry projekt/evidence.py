from pojistena_osoba import PojistenaOsoba

class EvidencePojistenych:
    """
    Třída sloužící k evidenci pojištěných osob.
    Umožňuje přidání, zobrazení všech záznamů a vyhledávání podle jména.
    """

    def __init__(self):
        """
        Inicializuje evidenci jako prázdný seznam pojištěných osob.
        """
        self.seznam_osob = []

    def pridat_osobu(self, osoba: PojistenaOsoba):
        """
        Přidá novou pojištěnou osobu do evidence.

        :param osoba: Objekt třídy PojistenaOsoba, který se přidá do seznamu.
        """
        self.seznam_osob.append(osoba)
        print(f"Pojištěná osoba {osoba.jmeno} byla přidána.")

    def zobrazit_vsechny(self):
        """
        Vypíše seznam všech pojištěných osob.
        Pokud je seznam prázdný, informuje uživatele.
        """
        if not self.seznam_osob:
            print("Seznam pojištěných je prázdný.")
        else:
            for osoba in self.seznam_osob:
                print(osoba)

    def vyhledat_osobu(self, jmeno: str):
        """
        Vyhledá osobu v evidenci podle jména (bez ohledu na velikost písmen).

        :param jmeno: Jméno hledané osoby.
        :return: Vypíše nalezené osoby nebo informuje o nenalezení.
        """
        nalezeni = [osoba for osoba in self.seznam_osob if osoba.jmeno.lower() == jmeno.lower()]
        if nalezeni:
            for osoba in nalezeni:
                print(osoba)
        else:
            print(f"Pojištěná osoba se jménem {jmeno} nebyla nalezena.")
