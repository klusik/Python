# program pro vypocet ciste mzdy
# jak se cista mzda pocita:
# cista mzda = (hruba mzda - (zdravotni pojisteni + socialni pojisteni + zaloha na dan) + (slevy na dani + danova zvyhodneni))
# dan z prijmu fyzickych osob = 15% ze superhrube mzdy
# sleva na poplatnika = 2070CZK
# danove zvyhodneni prvni dite = 1267CZK
# danove zvyhodneni druhe dite = 1617CZK
# danove zvyhodneni treti dite az nekonecno = 2017CZK
# dite ZTP = zvyhodneni x2
# sleva na studenta = 335CZK
# sleva invalida I a II = 210CZK
# sleva invalida III = 420CZK
# ZTP = 1345CZK
# sleva na manzu = 24840CZK / rok
# solidarni dan = 7% z hrube mzdy, kdyz tva mzda > 139340CZK



# program pro vypocet ciste mzdy

def Calculate():
    # Hruba mzda = soucet veskerych polozek nalezicich zamestnanci (dovolena, odpracovane hodiny, etc)
    gross = input('Zadejte hrubou mzdu:')
    gross = int(gross)
    if gross < 14600:
        gross = 14600
    print('byla zadana hruba mzda ' + str(gross) + 'CZK')



    # superhruba mzda = hruba mzda + nepenezni prijem + socialni pojisteni (24.8% [plati zamestnavatel]) + zdravonti ...
    # ... (9% [plati zamestnavatel]) X nebo hruba mzda x 133.8%  ; zaokrouhluje se nahoru na stokoruny
    superGross = gross * 1.338
    print('superhruba mzda cini ' +str(superGross) + 'CZK')
    


    # zaloha na dan z prijmu = 15% ze superhrube mzdy
    tax = superGross * 0.15
    print('dan cini 15% ze superhrube mzdy. Vas prispevek statu je :' + str(tax) + 'CZK')
      


    # slevy na dani:
    # sleva na poplatnika = 2070CZK
    pinkForm = input('Zadate o slevu na poplatnika (Vyplnen ruzovy formular?)? Odpovezte "Y" nebo "N" ')
    pinkForm.upper()

    if pinkForm == 'Y':
        pinkForm = 2070
        print('sleva na dani = ' + str(pinkForm) + 'CZK')
    else:
        pinkForm = 0
        print('sleva na dani = ' + str(pinkForm) + 'CZK')
    
    # invalidka I a II = 210CZK
    slevaKripl = input('Mate invaliditu I. nebo II. stupne? Odpovezte "Y" nebo "N" ')
    slevaKripl.upper()

    if slevaKripl == 'Y':
        slevaKripl = 210
        print('sleva na invalidu = ' + str(slevaKripl) + 'CZK')
    else:
        slevaKripl = 0
        print('sleva na invalidu = ' + str(slevaKripl) + 'CZK')

    # invalidka III = 420CZK
    slevaKripl3 = input('Mate invaliditu III. stupne? Odpovezte "Y" nebo "N" ')
    slevaKripl3.upper()

    if slevaKripl3 == 'Y':
        slevaKripl3 = 420
        print('sleva na invalidu level 3 = ' + str(slevaKripl3) + 'CZK')
    else:
        slevaKripl3 = 0
        print('sleva na na invalidu level 3 = ' + str(slevaKripl3) + 'CZK')

    # ztp = 1345CZK
    ztp = input('Jste drzitelem prokazu ZTP? Odpovezte "Y" nebo "N"')
    ztp.upper()

    if ztp == 'Y':
        ztp = 1345
        print('sleva na ZTPcka = ' + str(ztp) + 'CZK')
    else:
        ztp = 0
        print('sleva na ZTPcka = ' + str(ztp) + 'CZK')
          
    # sleva na studenta = 335CZK
    student = input('Mate v domacnosti studenta? Odpovezte "Y" nebo "N"')
    student.upper()

    if student == 'Y':
        student = 335
        print('sleva na studenta = ' + str(student) + 'CZK')
    else:
        student = 0
        print('sleva na studenta = ' + str(student) + 'CZK')
          
        # rocni sleva na vyzivovaneho manzela = 24840 -> 24840/12=2070
    prizivnik = input('Mate v domacnosti prizivnika (manzel bez prijmu)? Odpovezte "Y" nebo "N"')
    prizivnik.upper()

    if prizivnik == 'Y':
        prizivnik = 2070
        print('sleva na manzu = ' + str(prizivnik) + 'CZK')
    else:
        prizivnik = 0
        print('sleva na manzu = ' + str(prizivnik) + 'CZK')


    # danove zvyhodneni:
        # dite I = 1267CZK
        # dite II = 1617CZK
        # dite III + = 2017
        # dite ZTP = 2x dite n

    dite = input('Zadejte pocet deti. Odpovezte "0", "1", "2" nebo "3"')
    ditelist = ("0", "1", "2", "3")

    if dite not in ditelist:
        print('zadana neplatna hodnota, danove zvyhodneni na dite nebude pouzito')
        dite = 0

    if dite == "0":
        dite == 0
        print('danove zvyhodneni na dite = ' + str(dite) + 'CZK')

    if dite == "1":
        dite = 1267
        print('danove zvyhodneni na dite = ' + str(dite) + 'CZK')

    if dite == "2":
        dite = 1617
        print('danove zvyhodneni na dite = ' + str(dite) + 'CZK')

    if dite == "3":
        dite = 2017
        print('danove zvyhodneni na dite = ' + str(dite) + 'CZK')

    diteZTP = input('Je vase dite zdravotne postizene? Odpovezte "Y" nebo "N"')
    diteZTP.upper()

    if diteZTP == "Y":
        diteZTP = 2
        dite = dite * diteZTP
        print('danove zvyhodneni na dite = ' + str(dite) + 'CZK')


    # socialni pojisteni = 6.5% z hruba mzda
    socPoj = gross * 0.065
    print('prispevek na cikany = ' + str(socPoj) + 'CZK')


    # zdravotni pojisteni = 4.5% z hruba mzda
    zdravPoj = gross * 0.045
    print('prispevek na commy doktory = ' + str(zdravPoj) + 'CZK')


    #solidarni dan = 7% z 130796 (4x celorepublikovy prumer)
    commyTax = 0
    if gross > 130796:
        commyTax = 130796 * 0.07
        print('dan z blahobytu = ' + str(commyTax) + 'CZK')
    else:
        commyTax = 0
        print('dan z blahobytu = ' + str(commyTax) + 'CZK')


    # srazky ze mzdy
    srazky = input('Uvedte, zda mate srazky ze mzdy. Odpovezte ciselnou hodnotu')

    if srazky != "0":
        srazky = int(srazky)
        print('srazky ze mzdy cini = ' + str(srazky) + 'CZK')
    else:
        srazky = 0
        print('srazky ze mzdy cini = ' + str(srazky) + 'CZK')


    # nepenezni prijem
    nepenezniPrijem = input('Mate nepenezni prijem (obvykle sluzebni vozidlo pro soukrome ucely). Odpovezte "Y" nebo "N"')

    if nepenezniPrijem == "Y":
        print("mate nepenezni prijem")
        print("""
    Mezi nepenezni prijme patri napr. bezplatne poskytnute sluzebni vozidlo pro soukrome ucely.
    Prijem zamestance je pak 1% vstupni ceny vozidla (min. 1000CZK)
    za kazdy zapocaty kalendarni mesic poskytnuti vozidla.

    V pripade, ze poplatnik vyuziva vice motorovych vozidel postupne za sebou,
    pouzije se 1% z nejvyssi vstupni ceny vozidla.

    Pokud poplatik pouziva vice vozidel soucasne,
    plati se 1% ze souctu vstupnich cen vsech vozidel.
    """)

        multivehicle = input('Pouzivate vice sluzebnich vozidel pro soukrome ucely? Odpovezte "Y" nebo "N"')

        if multivehicle == "Y":
            print('pouzivate vice sluzebnich vozidel')

            multi = []

            multivehicleserial = input('Pouzivate vice sluzebnich vozidel soucasne, nebo postupne? Odpovezte "soucasne" nebo "postupne"')

            if multivehicleserial == 'postupne':
                print('pouzivate vice sluzebnich vozidel postupne')

                nejdrazsi = input('Zadejte cenu nejdrazsiho vozidla')
                nejdrazsi = int(nejdrazsi)

                nepenezniPrijem = nejdrazsi * 0.01
                print('vas nepenezni prijem je ' + str(nepenezniPrijem) + 'CZK')

                if nepenezniPrijem < 1000:
                    nepenezniPrijem = 1000
            else:
                print('pouzivate vice sluzebnich vozidel soucasne')
                while True:
                    vozidlo = input('Zadejte cenu vozu')
                    multi.append(int(vozidlo))
                    end = input('Chcete pokracovat v zadavani dalsiho vozu? Odpovezte "Y" nebo "N"')

                    if end == "N":
                        break

                soucet = 0

                for i in multi:
                    soucet = soucet + i
                nepenezniPrijem = soucet * 0.01
                print('vas nepenezni prijem je ' + str(nepenezniPrijem) + 'CZK')
            
        else:
            print('pouzivate pouze jedno sluzebni vozidlo pro soukrome ucely')
            vehicle = input('Zadejte hodnotu vozidla')
            vehicle = int(vehicle)
            if vehicle > 0:
                nepenezniPrijem = vehicle * 0.01
                print('vas nepenezni prijem je ' + str(nepenezniPrijem) + 'CZK')
    

    # cista mzda = (hruba mzda +(slevy na dani + danova zvyhodneni) - (zdravotni pojisteni + socialni pojisteni ...
    # ... + zaloha na dan z prijmu + + solidarni dan +srazky ze mzdy)

    netSalary = (gross + (pinkForm+slevaKripl+slevaKripl3+ztp+student+prizivnik+dite) - (zdravPoj+socPoj+tax+commyTax+srazky))

    print('Super Hruba mzda = ' +str(superGross))
    print('hruba mzda = ' +str(gross))
    print('cista mzda = ' +str(netSalary))

Calculate()

