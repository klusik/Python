""" Vyhledavanai v rezetzi """

retezec = input("Zadej retezec: ")


""" Retezec == String """

def vitezny(retezec):
    """ Rozhodni, jestli je vyhráno """
    pass

def vyhralo_kolecko(retezec):
    """ Vyhrál ten s kolečkem """
    pass

def remiza(retezec):
    """ Zjisti remizu """



while True:
    if vitezny(retezec):
        """ Delej to, co se dela po vyhre """
        if vyhralo_kolecko(retezec):
            print("Vyhralo kolecko")
        else:
            print("Vyhral krizek")
    
    if remiza(retezec):
        print("Uz se neni kam hnout.")
        

def je_liche(cislo):
    print(cislo % 2) # 145847375
    return bool(cislo % 2) # boolean George Boole

# None, 0, False => False


""" Lepší algoritmus """
"""
    1.  zjistím, jestli jsou někde protihráčova pole
        po jedné, tzn. někde třeba samostatné 'x'
    1b.	Pokud je někde osamostatněný znak, ale ob jednu
        je též a mezi nimi nic není, riziko => vyřešit
    2.	Pokud ano, dám svůj znak (kolečko) vedle
        (vpravo či vlevo, pokud to jde)
    3.	Pokud najdu hráčova dvě pole, v dalším kole už
        může vyhrát, takže počítač musí táhnout vedle.
        Tak, aby zabránil výhře.
        
"""

if "x-x" in retezec:
    print(retezec.index("x-x"))
    
    
operace = input('Zvol operaci: (tj. vyber znaménko:*,/,+ nebo -)')
operace = int(operace)
operace_je_spravne = operace > 0

if operace == '+':
    print("Počítáme:", prvni_číslo , operace,  druhé_cislo, "=" , prvni_cislo + druhe_cislo)
    print(f"Počítáme {prvni_cislo} {operace} {druhe_cislo} = {prvni_cislo + druhe_cislo}")

a > 7

print(("xxx" in retezec) or ("ooo" in retezec))