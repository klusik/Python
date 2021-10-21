# Hadej cislo

# Pro generovani nahodneho cisla je potreba nacist knihovnu 'random'
import random

# Je potreba inicalizovat generator nahodnych cisel, k seedovani si pak neco povime u tabule.
random.seed()

# Vytvorim random generovany cislo v rozsahu 1 az 10
hadaneCislo = random.randrange(1, 10)

while True:
    # Zeptame se uzivatele
    zadaneCislo = int(input("Zadej svuj tip: "))

    # Zkoumam, jak moc jsem se trefil
    if zadaneCislo > hadaneCislo:
        # Pokud jsem se trefil moc vysoko
        print("Zadals moc vysoke cislo.")
    
    elif zadaneCislo < hadaneCislo:
        # Pokud strilim moc nizko
        print("Zadals moc male cislo.")

    elif zadaneCislo == hadaneCislo:
        # Pokud strilim presne
        print("<Mirouskuv hlas> Preeeesne! </Mirouskuv hlas> :-) ")

        break # Ukoncim hadani
