# ----------------------------------------------------------------------------------------------
# implementace
class Bod:

    # v init metode priradim parametry instance do promennych
    def __init__(self, osa_x, osa_y):
        self.x = osa_x  # parametr self musim zadat, aby promenna byla pristupna i mimo metodu
        self.y = osa_y

    # tim je hotova inicializace promennych a muzu x a y pouzivat v programu

    # budu menit pozici bodu
    def zmena(self, nove_x, nove_y):
        self.x = nove_x
        self.y = nove_y

    # kdyz umim zadat hodnoty x a y a umim je i menit, tak je chci taky vypsat
    # dulezite je si uvedomit, ze x a y nyni existuji jako promenne,
    # ktere lze volat z jinych metod
    def vypis(self, nazevBodu):
        print(nazevBodu, "X: ", self.x, "Y: ", self.y)


# ----------------------------------------------------------------------------------------------
# instance

# prvni instance tridy Bod
b1 = Bod(0, 0)  # tohle je prvni instance tridy, ktera vytvori bod se souradnicemi 0,0
b1.vypis("b1")  # tisknu, co je zapsano v promennych self.x a self.y (a ty hodnoty se tam dostali pres parametry ...
# ... metody __init__ osa_x a osa_y)

b1.zmena(1, 1)  # pouziju porad stejne promenne self.x a self.y, ktere dostanou hodnoty z parametru nove_x a nove_y
b1.vypis("b1_new")  # tisknu nove souradnice bodu x a y

# druha instance tridy Bod
b2 = Bod(10, 10)
b2.vypis("b2")
b2.zmena(9, 9)
b2.vypis("b2_new")
