# this file is supposed to help me understand conditions

vstup1 = input('dle libosti zadejte hodnotu 0 nebo 1 ')
vstup1 = int(vstup1)

vstup2 = input('dle libosti zadejte druhou ciselnou hodnotu ')
vstup2 = int(vstup2)

soucet = vstup2+vstup1
soucin = vstup1 * vstup2
if vstup1 == 0 and soucin == 0:
    print('zadali jste ' + str(vstup1))
    print('bylo nasobeno nulou')
elif vstup1 == 1:
    print('zadali jste ' + str(vstup1))
else:
    print('nezadali jste ani 0 ani 1')

if not vstup1 == 0 and soucin == 0:
    print('druha zadana hodnota byla nula')
    
