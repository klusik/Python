"""
    Zadání 5: Velmi pokročilé

    Vytvořte prográmek, který načte výrobky ze souboru a jejich ceny.

    Program se zeptá uživatele na počet kusů výrobku, který chce nakoupit
    a cenové rozmezí (miminální cena, maximální cena, stačí int() hodnoty).

    Prográmek poté vytvoří nákupní seznam, který bude obsahovat daný počet výrobků
    a celková cena bude v rozmezí zadaných hodnot.

    Pokud takový nákup nepůjde vytvořit, program vypíše, že takový nákup nelze vytvořit
    a nabídne uživateli, že může znovu zadat pravidla.

    Výsledný výstup pak bude vypadat třeba takto:

        PC: Kolik kusů výrobků nakoupit?
        U:  10
        PC: Jaká je minimální cena nákupu?
        U:  100
        PC: Jaká je maximální cena nákupu?
        U: 150

        Nákup bude obsahovat:
        6 × kaiserka po 4.5, celkem 27 Kč
        4 × mléko po 22, celkem 88 Kč

        Celková cena nákupu 115 Kč.
"""