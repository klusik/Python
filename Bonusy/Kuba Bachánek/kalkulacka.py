def main():

    print("Ahoj, jsem program na operace s čísli, postupuj dle mých pokynu a dostaneme se ke zdárnému cíli")

#vložení čísel, metoda while True zajistí znovupoužitelnost programu
    while True:
        a = int(input("Zadej první číslo: "))
        b = int(input("Zadej druhé číslo: "))

#operace, které se budou provádět
        soucet = a+b
        rozdil = a - b
        nasobek = a * b
        deleni = a/b

#výpis výsledku
        print(f"Součet: {soucet}")
        print(f"Rozdíl: {rozdil}")
        print(f"Násobek: {nasobek}")
        print(f"Dělenec: {deleni}")

#program se zeptá zda pokračovat, odpověď převede na malé písmena kvůli podmínce
        pokracovani = input("Chceš pokračovat v zadávání čísel? (Ano/Ne) ")
        if pokracovani.lower() != "ano":
            print("Děkuji za použití kalkulačky")
            break

#program jede od začátku
if __name__ == "__main__":
    main()