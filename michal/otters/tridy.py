class Bod:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def posun(self, x_plus, y_plus):
        self.x += x_plus
        self.y += y_plus

    def vytiskni(self):
        print("Bod: X = ", self.x, " Y = ", self.y)


def f():
    a = 1
    def g():
        def h():
            return a
        return h()
    return g()

print (f())

b1 = Bod(0, 0)
b2 = Bod(5, 8)
b3 = Bod(9, 4)

b1.vytiskni()
b2.vytiskni()
b3.vytiskni()

b1.posun(-3, 4)
b2.posun(8, 7)
b3.posun(1, 0)

b1.vytiskni()
b2.vytiskni()
b3.vytiskni()
