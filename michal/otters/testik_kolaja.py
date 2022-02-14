class zvire:
    def __init__(self, vaha, vyska):
        '''tohle je konstruktor, po zavolani tridy se postara o vytvoreni instance'''
        self.vaha = vaha
        self.vyska = vyska
        
    def vypisVahu(self):
        print(f'vaha: {self.vaha}')
        
    def vypisVysku(self):
        print(f"vyska: {self.vyska}")
    
    
# vytvor instanci
slon = zvire(1200, 100)

slon.vypisVahu()
slon.vypisVysku()     

krecek = zvire(5, 15)

krecek.vypisVahu()
krecek.vypisVysku()
    
    
        
#class krecek(zvire):
    