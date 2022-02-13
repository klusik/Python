#implementace
class Bod:

    #do metody init si ulozim promenne, ktere budu v programu potrebovat
    #odkazovat se na ne budu pres instanci
    
    def __init__(self, x, y):
        self.x = x #promennou x ulozim jako metodu instance tridy
        self.y = y #stejne jako x

    def posun(self, posun_x, posun_y):
        self.x += posun_x #az bude spustena instance tridy bod, tak zadany parametr projde pres init az sem
        self.y += posun_y #viz x

    def tisk(self, nazevBodu):
        print (nazevBodu,"X: ", self.x, "Y: ", self.y)



#----------------------------------------------------
#instance

bod1 = Bod(10, 10)
bod1.tisk("bod1")

bod2 = Bod(20, 20)
bod2.tisk("bod2")

bod3 = Bod(30, 30)
bod3.tisk("bod3")
print ("a ted chci psat zmeny")
bod1.posun(4,2)
bod1.tisk("bod1")

bod2.posun(-115,3)
bod2.tisk("bod2")

bod3.posun (3,-3)
bod3.tisk("bod3")
