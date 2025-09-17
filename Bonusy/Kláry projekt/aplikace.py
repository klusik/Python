from evidence import EvidencePojistenych
from validace import validuj_vek, validuj_telefon, validuj_email
from pojistena_osoba import PojistenaOsoba

def hlavni_menu():
    """
    Hlavní menu aplikace pro evidenci pojištěných osob.
    Umožňuje uživateli přidat novou osobu, zobrazit všechny osoby,
    vyhledat osobu podle jména nebo ukončit program.
    """
    evidence = EvidencePojistenych()  # Vytvoření instance evidence

    while True:
        # Výpis možností hlavního menu
        print("\n--- Evidence pojištěných osob ---")
        print("1. Přidat novou pojištěnou osobu")
        print("2. Zobrazit všechny pojištěné osoby")
        print("3. Vyhledat pojištěnou osobu")
        print("4. Konec")

        # Výběr uživatele
        volba = input("Zadejte číslo akce: ")

        if volba == "1":
            # Zadání údajů nové pojištěné osoby
            jmeno = input("Zadejte jméno: ")
            vek = validuj_vek("Zadejte věk: ")
            telefon = validuj_telefon("Zadejte telefonní číslo: ")
            email = validuj_email("Zadejte email: ")

            # Vytvoření objektu a přidání do evidence
            osoba = PojistenaOsoba(jmeno, vek, telefon, email)
            evidence.pridat_osobu(osoba)

        elif volba == "2":
            # Zobrazení všech pojištěných osob
            evidence.zobrazit_vsechny()

        elif volba == "3":
            # Vyhledání osoby podle jména
            jmeno = input("Zadejte jméno pro vyhledání: ")
            evidence.vyhledat_osobu(jmeno)

        elif volba == "4":
            # Ukončení programu
            print("Ukončuji program.")
            break

        else:
            # Ošetření neplatné volby
            print("Neplatná volba, zkuste to znovu.")

# Spuštění programu pouze při přímém spuštění souboru
if __name__ == "__main__":
    hlavni_menu()
