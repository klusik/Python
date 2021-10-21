# zadani: https://www.codewars.com/kata/53f0f358b9cb376eca001079
# zadani2: https://www.codewars.com/kata/56cd44e1aa4ac7879200010b
# zadani3: https://www.codewars.com/kata/568018a64f35f0c613000054

class MyClass:
    i = 12345
  
    def f():
        return 'hello world'


class Complex:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart

x = MyClass

print(x.f())

class Ball:
    def __init__(self, value):
        self.b = value

    def g(a = "regular"):
        print(a)


x = Ball.g("abc")
y = Ball.g()



class Upper:
    def is_uppercase(a):
        if a.isupper():
            print( "True")
        else: print("False")

x = Upper.is_uppercase("ABC")
x = Upper.is_uppercase("ABCa")


class Game:
    

    def pokus():
        
        pokusy = 3
        hadanecislo = 10

        while pokusy != 0:
            
            a = int(input("zadej cislo"))

            if hadanecislo > a:
                print("jsi nizko")
                pokusy = pokusy -1
                

            elif hadanecislo < a:
                print("jsi vysoko")
                pokusy = pokusy -1
               

            elif hadanecislo == a:
                print("yes")
                pokusy = pokusy-1
               
                


x = Game.pokus()



