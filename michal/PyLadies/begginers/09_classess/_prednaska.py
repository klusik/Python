'''
Topic: classes
this file is intended as a lecture record 
date: 05.04.2022 (DD.MM.YYYY)
prednasejici: vaclav fiala
'''

# pravidlo LEGB
# L - local
# E = enclosing
# G - global
# B - built in

# L - local
a = 'global'

def funkce():
    a = "local"
    print(a)

funkce()
# co se vytiskne? -> 'local'

# E = enclosing
a = 'global'
def funkce():
    a = 'enclosing'
    def vnitrni_funkce():
        print(a)

    vnitrni_funkce()
funkce()

# G - global
a = 'global'


# B - built in
def funkce():
    print(None)
funkce()


# nepouzivat:
a = 'global'
def funkce():
    global a
    a = 'local'
    print(a)

funkce()

'''

python se ridi pravidlem LEGB. Nejprve prohledava na lokalni urovni, pokud nic nenajde,
pak na 'enclosing' urovni, potom na global, nakonec v built-in.
pokud mluvime o pythonu, lze rici, ze promennou hleda na stejne urovni odsazeni
'''

class Tridajedna():
    x = 10
    def __init__(self, param1, param2) -> None:
        self.param1 = param1
        self.param2 = param2

    def prvni_metoda(self):
        print(self.param1)


Instance = Tridajedna(0,1)
Instance.prvni_metoda()

class Kotatko():
    def zamnoukej(self):
        print('mnau')

kote = Kotatko()

kote.zamnoukej()

# atributy instance, toto neni optimalni zpusob, jak s nimi pracovat
# je to jen ukazka, ze instance ma nejake atributy
kote.jmeno = 'mourek'
dalsi_kote = Kotatko()
dalsi_kote.jmeno = 'hugo'

class Kotakto():
    def zamnoukej(self):
        print(f'{self.jmeno}: Mnau!')

kote = Kotakto()
kote.jmeno = 'Mourek'
kote.zamnoukej()

# kvuli self neni definovane jmeno pro kote2
# kote2.jmeno = 'hugo'

'''
trida ma atributy, ktere rikaji, jaka je instance (velke, male, etc)
metody jsou v podstate funkce, ale v ramci tridy
'''

# __init__ metoda = pouziva se na atributy tridy

# UKOL <3

# napiste tridu ctverec s atributem delka strany
# a metodou vypocti obvod

class Ctverec:
    # tohle je promenna, kterou bude znat kazda instance = konstanta
    pocet_stran = 4
    def __init__(self, delka_strany):
        self.delka_strany = delka_strany

    def obvod(self):
        print(f'obvod ctverce je {self.pocet_stran * self.delka_strany}')

    def obsah(self):
        print(f'obsah ctverce je {self.delka_strany * self.delka_strany}')

malej = Ctverec(3)
malej.obvod()
malej.obsah()

velkej = Ctverec(5)
velkej.obvod()
velkej.obsah()

# DEDICNOST
class Zvire():
    def __init__(self):
        print('Zvire vytvoreno')

    def jez(self):
        print('jim')

class Pes(Zvire):
    def __init__(self):
        print('Pes vytvoren')

z = Zvire()
z.jez()
# moznost pouziti metod z jine tridy
p = Pes()
p.jez()

# Prepisovani metod


# zmena v metode __init__  v Parent class


