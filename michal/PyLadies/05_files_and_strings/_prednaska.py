'''
Topic: files and strings
this file is intended as a lecture record 
date: 17.3.2022 (DD.MM.YYYY)
prednasejici: jakub cervinka
'''

# rekli jsme si neco o escape chars
# zapis unicode znaku pomoci unicode kodu

# ted si ukazujeme slicing

# ted neco o string metodach

# napis program, ktery se uzivatele zepta na jmeno a prijmeni, kazde zvlast a 
# vypise inicialy

def inicialy(sJmeno, sPrijmeni):
    sJmeno = sJmeno[0].upper()
    #sJmeno = sJmeno.upper()
    sPrijmeni = sPrijmeni[0].upper()
    #sPrijmeni = sPrijmeni.upper()
    return sJmeno + '.' +  sPrijmeni + '.'

print(inicialy('Michal', 'Sykora'))

# neco o praci se souborama
# napiste soubor basnicka.txt
file = open(r'C:\python.repo\michal\PyLadies\05_files_and_strings\basnicka.txt', mode='r', encoding='utf-8')
print(file)
file_content = file.read()
print(file_content)
file.close()

# konece, context manager! :D

with open(r'C:\python.repo\michal\PyLadies\05_files_and_strings\basnicka.txt') as file:
    file_content = file.read()
    print(file_content)

# nacitani souboru po radku
with open(r'C:\python.repo\michal\PyLadies\05_files_and_strings\basnicka.txt') as file:
    for radek in file:
        print(radek)

with open(r'C:\python.repo\michal\PyLadies\05_files_and_strings\basnicka.txt') as file:
    file_content = file.readlines()
    for line in file_content:
        print(line)

# the hell, my si klidne do toho souboru neco zapiseme!

with open(r'C:\python.repo\michal\PyLadies\05_files_and_strings\basnicka.txt') as file:
    file_content = file.read()

content_UPPER = file_content.upper()

with open(r'C:\python.repo\michal\PyLadies\05_files_and_strings\basnicka_upper.txt', mode='w') as file_upper:
    file_upper.write(content_UPPER)
    print('saved')

with open(r'C:\python.repo\michal\PyLadies\05_files_and_strings\basnicka_upper.txt') as file:
    file_content = file.read()
    print(file_content)


# append upper content to original file

with open(r'C:\python.repo\michal\PyLadies\05_files_and_strings\basnicka.txt', mode = 'a') as file_append:
    file_content = file_append.read()
    file_content_upper = file_content.upper()
    file_append.write(file_content_upper)
