# napis program, ktery nacte od uzivatele cislo
# pokud dane cislo je 0-9, vypise "male cislo"
# pokud dane cislo je 10-19, vypise "stredni cislo"
# pokud dane cislo je 20-inf, vypise "velke cislo"

the_number = input('zadej cislo: ')
the_number = int(the_number)

if the_number > 0 and the_number < 10:
    print('to je ale mrnave cislicko')
elif the_number >= 10 and the_number <= 19:
    print('prumerne cislo')
elif the_number > 19:
   print('to je ale poradne cislo!')

# test of range condition
elif 30 < the_number < 40:
    print('tvl, to je cislo')