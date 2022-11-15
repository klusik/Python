"""
    Chci list (seznam) nějakých uživatelů, uživatelé budou slovníky.
    Uživatelé budou mít jména, příjmení a počet psů, které mají doma.

    Na konci budu chtít nějak hezky vypsat ve smyslu
    "uživatel X má doma Y psů"
    nebo "uživatel F doma nemá bohužel žádného psa." atd.
"""

# Vytvoříme lidi
clovek1 = {
    "jmeno" : "Karel",
    "prijmeni" : "Šrámek",
    "pocet_psu" : 1,
}

clovek2 = {
    "jmeno" : "Jindrich",
    "prijmeni" : "Zakl",
    "pocet_psu" : 0,
}

clovek3 = {
    "jmeno" : "Marie",
    "prijmeni" : "Zachová",
    "pocet_psu" : 7,
}

# Prázdný seznam, do kterého přijdou lidé se psy
seznam_lidi_a_psu = []

# Naplnění seznamu lidmi se psy
seznam_lidi_a_psu.append(clovek1)
seznam_lidi_a_psu.append(clovek2)
seznam_lidi_a_psu.append(clovek3)


# Soucet psu
soucet_psu = 0

for clovek in seznam_lidi_a_psu:
    # Tuten for prolézá celý seznam, položku po položce.
    # Do proměnné 'člověk' mi to ukládá položky seznamu,
    # v tutom případě samotné slovníky s uživateli.

    soucet_psu += clovek["pocet_psu"] # Připočítám počet psů

    if clovek["pocet_psu"]: # Pokud je počet psů 0, skočí do else
        # Pokud je psů alespoň 1, skočí to sem.

        print(f"Uzivatel {clovek['jmeno']} {clovek['prijmeni']} "
              f"ma doma {clovek['pocet_psu']} psu.")
    else:
        # Pokud uživatel nemá psa, jsem tady
        print(f"Uzivatel {clovek['jmeno']} {clovek['prijmeni']}"
              f"doma bohuzel nema zadneho psa")

print(f"Celkový počet nalezených psů je {soucet_psu}.")

print(seznam_lidi_a_psu)

a = 10

slovnik = {
    "navev_promenne" : "a",
    "hodnota_promenne" : 10,
}