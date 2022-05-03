'''
Nakonec trošku delší projekt. Budeme na něm stavět dál; nedokončíš-li ho teď, 
budeš ho muset dodělat před příští sadou projektů.

    1-D piškvorky se hrají na řádku s dvaceti políčky. Hráči střídavě přidávají
    kolečka (`o`) a křížky (`x`), třeba:

    1. kolo: -------x------------
    2. kolo: -------x--o---------
    3. kolo: -------xx-o---------
    4. kolo: -------xxoo---------
    5. kolo: ------xxxoo---------

    Hráč, která dá tři své symboly vedle sebe, vyhrál. 
'''
'''
Napiš funkci vyhodnot, která dostane řetězec s herním polem 1-D piškvorek
a vrátí jednoznakový řetězec podle stavu hry:

    "x" – Vyhrál hráč s křížky (pole obsahuje "xxx")
    "o" – Vyhrál hráč s kolečky (pole obsahuje "ooo")
    "!" – Remíza (pole neobsahuje "-", a nikdo nevyhrál)
    "-" – Ani jedna ze situací výše (t.j. hra ještě neskončila)

'''
def vyhodnot(pole):
    """Vstupmen funkce je řetezec herního pole.
    Funkce vyhodnotí stav hry. Jenou z možností jak stav hry sledovat, je 
    ověření výskyu rozhodující sekvence znaku (např. "xxx" nebo "ooo")
    """
    if ('xxx' in pole):
        print('vyral hrac s krizky')
        return 'x'
    elif ('ooo') in pole:
        print('vyhral hrac s kolecky')
        return 'o'
    elif('-' not in pole):
        print('remiza')
        return '!'
    else:
        print('hra jeste neskoncila')
        return '-'



def tah_hrace(pole, hrac):
    """Vstupem funkce je řetězec s herním polem a znak hráče. 
    Funkce se dotáže uživatele na číslo pozice na kterou chce umístit svůj znak. 
    Funkce následně ověří, zda-li pozice není  obsazená
    a lze na ni znak umístit.Pokud ano, vrátí upravené herní pole se zaznamenaným
    tahem hráče.
    """
    pass


def tah_pocitace(pole, hrac):
    """Vstupem funkce je řetězec s herním polem a znak hráče. 
    Funkce vygeneruje náhdné čísli pole, na které počítač bude hrát
    a vrátí upravené herní pole se zaznamenaným tahem počítače
    """
    pass


def znak_hrace():
    """Funkce, která má za úkol vrátit znak, který si hráč zvolí."""
    pass


def piskvorky():
    """Funkce vytvoří pole a přiřadí znak hráči a počítači. 
    K přiřazení zanku hráči je využita funkce "znak hráče". Střídavě jsou 
    volány funkce tah_hrace a tah_pocitacem s průběžnou kontrolou stavu hry.
     """
    pass


piskvorky()
