# cvicny program na koncepty OOP

class Stroj:
    print("tohle tiskne trida Stroj")
    # v konstruktoru definuji zakladni vlastnosti objektu
    def __init__(self, sirka, vyska, delka, hmostnost, jmeno):
        self.sirka = sirka
        self.vyska = vyska
        self.delka = delka
        self.hmostnost = hmostnost
        self.jmeno = jmeno

        constructor_message = f'''
        --==contructor message==--
        -- you have entered:
        -- name: {self.jmeno}
        -- width: {self.sirka}
        -- heigh: {self.vyska}
        -- length: {self.delka}
        -- weight: {self.hmostnost}
        '''
        print(constructor_message)

    def pohyb(self, mobility = 'yes'):
        if mobility == 'yes':
            print('bacha jedu!')        
        else:
            print('Together we stand, divided we fall')

    def dig(self, digging = 'yes'):
        if digging == "yes":
            print("ja jsem bagr!")
        else: 
            print("neumim kopat, nejsem rypadlo")
    










auto = Stroj(2000, 1600, 5500, 1450, "auto")
auto.dig("no")
auto.pohyb()

lod = Stroj(3000, 3000, 7000, 10000, "lod")
lod.pohyb()
lod.dig("no")

dulniVrtak = Stroj(50000, 1000000, 50000, 7000000000, "dulni vrtak")       
dulniVrtak.pohyb('No')
dulniVrtak.dig()
