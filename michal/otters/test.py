#tenhle soubor slozi vyhradne na testovani konkretnich funkcionality v pythonu

#vyzkokusim si, jestli si pamatuju, o cem jsou tridy - priklad se souradnicemi a body

class Bod:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def relocate (self, new_x, new_y):
         self.new_x = new_x
         self.new_y = new_y
    def print(self):
        print('initial values were: ', 'x=', self.x, 'y=', self.y, "new values are:", "x_new=", self.new_x, "y_new=", self.new_y)
