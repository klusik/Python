soubor = open('souborovac.py', encoding ='utf-8')
obsah = soubor.read()

pocet_znaku = len(obsah) - obsah.count(" ") - obsah.count("\n")

pocet_radku = len(obsah.split("\n"))
#print("Počet znaků:", pocet_znaku)
#print("Počet řádků:", pocet_radku)
soubor.close()

soubor = open("souborovac_stats.txt", "w", encoding ='utf-8')
soubor.write(f"Počet znaků:{pocet_znaku}\nPočet řádků:{pocet_radku}")
soubor.close()