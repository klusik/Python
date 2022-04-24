'''
Výzva
Jednou z výhod použití objektů v programu, je ten, že určitý kód (často na
začátku nebo v prvních částech/úrovních) programu nezajímá, že objekt je 
konkrétního typu. Stačí, že je odvozen od třídy, která obsahuje danou 
funkci nebo atribut. Nám v tom případě stačí brát konkrétní objekt odvozený
od dané základní třídy. 

Vytvoř si tak třídu Obrazec, která bude definovat 
metody obvod(), obsah() a rozdil_obsahu(jiny_obrazec). Metody obvod(), 
obsah() nebudou dělat nic, protože to záleží na konkrétní implementaci daného
obrazce. Metoda rozdil_obsahu(jiny_obrazec) však naimplementovaná být může. 
Od třídy Obrazec pak odvoď třídy Ctverec, Trojuhlenik (rovnostraný), Kruh. 
Každá bude mít jeden atribut: délku strany pro Ctverec a Trojuhelnik, poloměr
pro Kruh a budou implementovat odpovídající výpočty obvodu a obsahu. Nezapomeň
u každé třídy naimplementovat i textovou reprezentaci, kterou dostaneš
po použítí proměnné s objektem v příkazu print().
'''

class Obrazec:
    def __init__(self, delka_strany):
        self.delka_strany = delka_strany
        
    def obvod():
        pass
    def obsah():
        pass
    def rozdil_obsahu(self, nova_strana):
        self.nova_strana = nova_strana
        
    
class Ctverec(Obrazec):
    pass

class Trojuhelnik(Obrazec):
    pass

class Kruh(Obrazec):
    pass