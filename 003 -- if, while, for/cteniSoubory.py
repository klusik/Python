# Precteme hromadu cisel ze souboru a zjistmie nejake krasne vlastnosti

soubor = r"C:\Users\klusi\OneDrive\Python\003 -- Seznamy etc\seznamNahodnychCisel.kls"

linkNaSoubor = open(soubor, "r")

while True:
    radek = linkNaSoubor.readline()
    
    # Konec souboru, prazdný soubor etc.
    if radek == '':
        break

    print(radek)
    print(type(radek))


linkNaSoubor.close

