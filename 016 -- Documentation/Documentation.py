import math

for n in range(1,11):
    if n <= 9:
        print(n, end=',')
    else:
        print(n, end=' :-) \n')


someList = [x for x in range(1, 11)]
print(someList)

a = 'f'
someList2 = a * 10
for i in range(1, len(someList2)+1):
    print(i)

randomString = 'Ahoj Lukasi'
if 'Ahoj' in randomString:
    print('Je to tam')

def myAverage(*kwargs):
    addition = 0
    for i in kwargs:
        addition += i
  
    if len(kwargs) == 0:
        return None

    else:
        return addition/len(kwargs)

print(myAverage(1,2,5,9,25))

# multiplicatione table
def multiplicationTable(row,column):
    for a in range(row):
        for b in range(column):
            #print ((a+1)*(b+1), end=' ')
            print("{:6.3f}".format((a+1)*(b+1)), end = ' ')
        print(' ')
multiplicationTable(5,10)

# zadame cislo a funkce vrati to x, n.
# se da vyjadrit jako x^n, kde x > 1 a n > 1,

def testFunkce():
    x = 1
    y = 2

    return x, y 

a, b = testFunkce()
print (a)

def isBeautiful(inputNumber):
    maximumBase = math.floor(math.sqrt(inputNumber))+1

    for base in range(2,maximumBase+1):
        power = 1
        while True:
            if base ** power == inputNumber:
                return base, power
            if base ** power > inputNumber:
                break
            power += 1
    return False, False

base, power = isBeautiful(4)
print(f'{base} to {power} is {base**power}')