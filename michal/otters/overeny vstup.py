def overeny_vstup(self):
    while True:
        try:
            vstup = int(input('vyjimka: prosim zadejte cislo v rozmezi 1 - 3000: '))
        except ValueError:
            print('vyjimka: nebylo zadano cislo')
            continue
        

        if vstup <= 0 or vstup > 3000:
            vstup = input('podminka: prosim zadejte cislo v rozmezi 1 - 3000: ')
        else:
            print('zadano spravne cislo')
            break
