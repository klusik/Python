"""
    Čeho bych chtěl dosáhnout v budoucnu
"""

if __name__ == "__main__":
    # Vstup od uživatele
    vstup = input("Napiš nějaké slovo či krátkou větu: ")

    # Rozhodnutí o tom, jestli je prázdný řetězec či nikoliv
    if not vstup:
        print("Tento řetězec je prázdný.")

        # Dál nemá program dělat, protože není
        # s čím pracovat, ukončuji program.
        exit()

    # Pokud tedy vstup není prázdný, můžeme s řetězcem dále pracovat

    # Nejdříve zjistíme počet mezer:
    pocet_mezer = vstup.count(' ')

    # Pak zjistíme počet písmenek 'a' nebo 'A'
    # (na velikosti nebude záležet, takže Maruška a MAruška mají obě 2 áčka)
    # Spočteme to tak, že nejdříve pomocí .lower() změníme jméno na vše malými,
    # poté spočteme áčka.
    pocet_acek = vstup.lower().count('a')

    # Nakonec zjistíme nejčastější písmenko, to už je trošku složitější :-)
    nejcastejsi = max(vstup.lower().replace(' ', ''), key=lambda x: vstup.lower().count(x))

    # Vypíšeme výstup:
    print(f"Zadal jsi výraz '{vstup}'.\nTento výraz obsahuje {pocet_mezer} mezer, "
          f"{pocet_acek} áček a nejčastější znak je '{nejcastejsi}'.")
