rimske = input('Zadej rimske cislo: ')

ciselnyseznam = []
for pismeno in rimske:
    if(pismeno == 'I'):
        ciselnyseznam.append(1)
    elif(pismeno == 'V'):
        ciselnyseznam.append(5)
    elif(pismeno == 'X'):
        ciselnyseznam.append(10)
    elif(pismeno == 'L'):
        ciselnyseznam.append(50)
    elif(pismeno == 'C'):
        ciselnyseznam.append(100)
    elif(pismeno == 'D'):
        ciselnyseznam.append(500)
    elif(pismeno == 'M'):
        ciselnyseznam.append(1000)

predchozi = 0
vysledne = 0

for cislo in ciselnyseznam:
    if predchozi != 0:
        if cislo > predchozi:
            vysledne  = vysledne - predchozi
        else:
            vysledne = vysledne + predchozi
    predchozi = cislo


if cislo > predchozi:
    vysledne  = vysledne - predchozi
else:
    vysledne = vysledne + predchozi

print(vysledne)
