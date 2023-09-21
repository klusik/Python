#seznam čísel uložených do proměnné
cisla = []

#program bude opakovat podmínku dokud uživatel neukončí cyklus příkazem "konec"
while True:
    vstup = (input("Zadej čísla, které budeme srovnávat, až budeš hotov, napiš konec: "))

#konec podmínky
    if vstup.lower() == "konec":
        break

#ošetření programu pro případ, že uživatel nezadá celé číslo
    try:
        cislo = int(vstup)
        cisla.append(cislo)
    except ValueError:
        print("Neplatný znak, zadávej pouze celá čísla, pokud si přeješ skončit zadej 'konec'")

#program seřazuje 3 nejvvyšší hodnoty
cisla.sort(reverse=True)
nejvyssi_cisla = cisla [:3]

print("Tři nejvyšší zadané čísla jsou: ", nejvyssi_cisla)