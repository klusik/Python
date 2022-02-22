# here i will keep record of code teacher is showing
'''
# toying with print()

# float numbers are using .
from re import A


print(100-2.5)
print(100-2,5)

# showing some errors, advising to use them to user's advantage

# explaining idea of variable

strana_a = 5
print("delka strany a je", strana_a)

plocha_ctverce = strana_a**2

print(f"plocha ctverce o delce strany {strana_a} je", plocha_ctverce)

# showing multi line comments using tripe quotes

# task: calculate obvod

obvod = 4* strana_a

print(f'obvod ctverce o delce strany {strana_a} je', obvod)

# read user input

strana_a = int(input('zadej stranu:'))
print(f'zadal jsi delku strany {strana_a}')

plocha_ctverce = strana_a ** 2
print(f"plocha ctverce o delce strany {strana_a} je", plocha_ctverce)

# self.work: plocha obdelnika v desetinych cislech

strana_a = float(input("zadej delku strany 'a':"))
strana_b = float(input('zadej delku strany "b":'))

plocha_obdelnika = strana_a * strana_b
obvod_obdelnika = 2*(strana_a+strana_b)

print(f'plocha obdelnika o strane a {strana_a} a strane b {strana_b} cini', plocha_obdelnika)
print(f'obvod obdelnika o strane a {strana_a} a strane b {strana_b} cini', obvod_obdelnika)

# showing constant pi
from math import pi # do not fancy this way of import
print(pi)

# showing how to re-write the value of pi constant

pi = 3.14

print(pi)

# re-typing pi to str

print(str(pi))
'''
# following: the break

# continuing after the break

# operatory

# +,-,*,/,-(napr -5),//,%, **, --, !=, <, >, <=, >=, 

from ast import ExtSlice


pravda = 1 < 3
print(pravda)

pravda = 1 == 3
print(pravda)


# conditions: IF, elif, else

# example: program na ohver vody v bazenu (rizeno cerpadlem)
# napajeno ze solaru -> sviti/nesviti
# mezni teplota vody
# vnejsi teplato vzduchu

svetlo = input("je den nebo noc? zadejte 'den', nebo 'noc'")
print(f'zadal jste, ze je {svetlo}')
target_temp = int(input('zadejte teplotu, na kterou chcete nahrat vodu'))
actual_temp = int(input('zadejte realnou teplotu vody: '))

if svetlo == "den":
    onOff = True
    print('napajeni solarnich panelu je k dispozici')
    if actual_temp <= target_temp:
        print(f'teplota vody v bazenu je {actual_temp}. natapim')
    else:
        print(f'teplota vody je {actual_temp}, nenatapim')
elif svetlo == "noc":
    onOff = False
    print('slunce nesviti. je mala doba ledova')+
    
elif svetlo == "mlha":
    onOff = False
    print('je mlha, dneska to na koupani neni')
else:
    onOff = False
    print("nesplnena zadna podminka, pocasi leda pro otuzilce")



'''
# my own code
target_temp = int(input('zadejte teplotu, na kterou chcete nahrat vodu'))
actual_temp = int(input('zadejte realnou teplotu vody: '))

if actual_temp < target_temp & onOff == True:
    print(f'natapime vodu na {target_temp}')
elif actual_temp < target_temp & onOff == False:
    print(f'teplota vody je nizka, nenatapime protoze je {svetlo}')
else:
    print(f'pozadovana teplota vody {target_temp} byla dosazena, vypinani natapeni')
'''