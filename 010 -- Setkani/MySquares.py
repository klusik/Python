mySquares = [i*i for i in range(1,10) if i %2==0]
print(mySquares)

mySentence = "Russiaisabigcountry"
myVowels = ["a", "e", "i", "o", "u", "y"]
myConsonants = [i for i in mySentence if i not in myVowels]
print(myConsonants)

def isprvocislo(cislo):
    import math
    b=0

    for i in range(2, int(math.sqrt(int(cislo)))+1):
        if cislo%i==0:
            b+=1
            break
    if b==0:
        return(cislo)
    return