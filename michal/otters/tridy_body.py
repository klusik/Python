#implementace
class Bod:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def movement(self, x_new, y_new):
        self.x += x_new
        self.y += y_new
        
    def print(self, nazevBodu):
        print(nazevBodu,"X: ", self.x, "Y: ", self.y)

    def usecka():
        print("Blah")

#instance
b1 = Bod(0, 0)
b1.print("b1")
#nove souradnice
b1.movement(4,4)
b1.print("b1")

b2 = Bod (10,10)
b2.print ("b2")
#nove souradnice
b2.movement(7,2)
b2.print("b2")

b3 = Bod(8,-3)
b3.print("b3")
#nove souradnice
b3.movement(-4,-10)
b3.print("b3")
