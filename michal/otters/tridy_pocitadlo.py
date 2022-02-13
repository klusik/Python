#-------------------------------------------------------------------------------
#Implementace

class NajdiSlovo:

#nejdrive si ulozim prohledavany soubor a hledane slovo do promennych
    def __init__(self, soubor, slovo):
        self.file = soubor
        self.word = slovo

        #ted otevru textak a ulozim ho do promenne
        self.textak = open(self.file, 'r')
        #zaloha - bytecne
        self.txt = self.textak
        #pocitadlo
        self.counter = 0

#pak budu hledat slovo v souboru
    def hledej(self):
        while True:
            radek = self.txt.readline()
            if radek  == '':
                break
        while True:
            index = radek.find(self.word)
            if index == -1:
                break
            self.counter +=1
            radek = radek[index+len(word):]
            self.textak.close()

#nakonec vytisknu vysledek
    def tisk(self):
        print("Vyskyt slova: ", self.word, " je: ", self.counter)


#-------------------------------------------------------------------------------
#instance

munchlax = NajdiSlovo(r"C:\Users\Z0001932\Desktop\prace\python\tridy\pika.txt", "Munchlax")
munchlax.hledej()
munchlax.tisk()
