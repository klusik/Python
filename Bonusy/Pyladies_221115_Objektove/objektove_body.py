"""
    Další ukázka nějaké objektové logiky,
    která by vám mohla pomoci

    Tentokrát názvy a všechno v češtině
"""
# IMPORTY #
import random
import math

# TŘÍDY #
class Bod:
    """ Třída, která popisuje bod se souřadnicemi x a y """
    def __init__(self, souradnice: tuple):
        """
            Tuta metoda se zavolá automaticky hned poté,
            co se vytvoří objekt (někde v kódu třeba bod = Bod()).

            Vidíme, že voláme jménem třídy a závorkami (), funguje to
            velmi podobně jako u funkcí, to, co bude v závorkách jako
            argument bude jako parametr tady v této třídě.

            V našem případě bude mít souřadnice tuple (ntici) souřadnic
            x a y (každý bod bude mít v 2D souřadnice x a y) :-)

            Vidíte další využití dvojtečky -- vynutím nějaký datový typ (abych
            tam nemohl poslat nic jiného než tuple, kdybych tam poslal
            třeba string, tak aby to řvalo, že je to špatně).

            Stejným způsobme můžete napsat třeba hodnota: int -- tedy integer.
        """

        # Vezmu parametr souradnice a uložím přímo do instance, do jeho vlastních souřadnic
        self.souradnice = souradnice

    def vypis_souradnice(self):
        """ Tato metoda vypíše souřadnice daného bodu """
        print(f"[{self.souradnice[0]} ; {self.souradnice[1]}]")

class Usecka:
    """ Třída popisující úsečku založenou na dvou bodech """
    def __init__(self,
                 bod_1 : Bod, # Příjmá 2 argumenty jako parametry, oba typu Bod (ze třídy Bod)
                 bod_2 : Bod,
                 ):
        self.bod_1 = bod_1
        self.bod_2 = bod_2

    def delka_usecky(self):
        """ Metoda vrátí délku úsečky """

        # počítá se jako odmocnina z (x_2 - x_1)^2 + (y_2 - y_1)^2 (Pythagorova věta)
        return math.sqrt(
            # Takovýto zápis je naprosto možný pro přehlednost, aby řádek nebyl brutálně dlouhý,
            # zpětné lomítko \ znamená, že budu pokračovat na další řádce
            (self.bod_2.souradnice[0] - self.bod_1.souradnice[0]) ** 2\
            + (self.bod_2.souradnice[1] - self.bod_1.souradnice[1]) ** 2
        )


# PROGRAM #

# Cíl je vygenerovat dva body, takže hurá na to. Souřadnice budu generovat náhodně obě
# bez generování náhodně by to vypadlo třeba:
# bod_1 = Bod((2, 3))

bod_1 = Bod((random.randint(-10, 10), random.randint(-10, 10)))
bod_2 = Bod((random.randint(-10, 10), random.randint(-10, 10)))

# Dva body jsou vygenerované, pojďme zavolat metody v těchto bodech, které souřadnice vypíší:
bod_1.vypis_souradnice()
bod_2.vypis_souradnice()

# Vytvoříme usečku z tutěch dvou bodů
nejaka_usecka = Usecka(bod_1, bod_2)

# Zjistíme & vypíšeme délku takové úsečky
print(f"Délka úsečky je {nejaka_usecka.delka_usecky()}.")
