"""
1-D piškvorky se hrají na řádku s dvaceti políčky. Hráči střídavě přidávají kolečka (`o`) a křížky (`x`), třeba:
1. kolo: -------x------------
2. kolo: -------x--o---------
3. kolo: -------xx-o---------
4. kolo: -------xxoo---------
5. kolo: ------xxxoo---------
Hráč, která dá tři své symboly vedle sebe, vyhrál.
Pro usnadnění orientace v celém projektu jsme připravili kostru, kterou najdeš tady

7.☜

Napiš funkci vyhodnot, která dostane řetězec s herním polem 1-D piškvorek a vrátí jednoznakový řetězec podle stavu hry:

"x" – Vyhrál hráč s křížky (pole obsahuje "xxx")
"o" – Vyhrál hráč s kolečky (pole obsahuje "ooo")
"!" – Remíza (pole neobsahuje "-", a nikdo nevyhrál)
"-" – Ani jedna ze situací výše (t.j. hra ještě neskončila)

"""

# CLASSES #
class Config:
    # Default gameboard size
    default_game_size = 20

class Game:
    def __init__(self,
                 size = Config.default_game_size, # Default game size
                 ):
        # Game size
        self.size = size

# RUNTIME #
def game():
    pass

if __name__ == "__main__":
    game()