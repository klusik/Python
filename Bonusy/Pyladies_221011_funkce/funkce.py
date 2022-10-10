"""
    Ukázkový prográmek na Pyladies 11. 10. 2022
    ===========================================

    Předmět ukázky: FUNKCE

    Cíl ukázky:
        Vytvořit hru za pomocí funkcí a věcí, co jsme
        dosud probrali, tedy proměnné a cykly.

    Princip aplikace:
        Uživatel si v 1. kroku vybere obtížnost (úrovně nechám na vás).
        Jakmile si vybere správnou obtížnost (kontrolu též přenechám na vás),
        uživatel začne hrát.

        Samotná hra tkví v uhádnutí počítačem "myšleného" čísla (počítač nemyslí, ale
        víte, jak to myslím :-D), počítač pak radí, jak se trefit (přidej, uber etc.)

        Výsledkem hry je počet špatných odhadů. Později hru můžeme vylepšit třeba
        o tabulku vítězů a podobné věci, se současnými znalostmi je toto pouze první krok.

        Hlavní hra začíná až úplně dole (funkce game()) :-)
"""

# IMPORTS #
import random


# FUNCTIONS #
def select_difficulty():
    """ Funkce vrátí hodnotu odpovídající složitosti hry.
        V budoucnosti to pak budeme moci řešit i trošku sofistikovanějším
        způsobem, až se naučíme další zajímavé datové typy, ale pro zatím
        vyřešme takto, není to nic proti ničemu. """

    # Úvodní nastavení hodnoty výběru na nulu. V naší hře budu chtít 3 úrovně složitosti:
    #   1   -   Lehká hra   (hádám mezi 1--10 včetně)
    #   2   -   Střední hra (hádám mezi 1--1000 včetně)
    #   3   -   Těžká hra   (hádám mezi 1--1.000.000 včetně)
    selection = 0

    while selection not in [1, 2, 3]:
        """ Už jste dělali cykly, takže víte, jak funguje while(). Pro zopakování,
            co se děje zde.
            
            while(podminka) bude dělat cyklus (bude chodit pořád dokola), dokud
            podmínka v jeho argumentu bude pravdivá.
            
            Zde bude podmínka pravdivá, dokud uživatel bude vybírat jiná 
            čísla než povolená ze seznamu 1, 2, 3.
            """

        selection = int(input("Zadej úroveň:\n"
                              "1 - lehka (1--10)\n"
                              "2 - stredni (1--1000)\n"
                              "3 -- tezka (1--1000000)\n"
                              "Tvoje volba? > "))

        # Funkce musí nějak komunikovat se světem, zde vrátíme vybranou hodnotu.
        return selection


def game():
    """ Hlavní hra, tedy funkce, která obsahuje samotnou hru jako takovou. """

    # Nejdříve potřebujeme vybrat složitost hry, zavolejme proto
    # funkci, která toto obslouží.
    difficulty = select_difficulty()

    # Na základě vybrané složitosti vybereme číslo, které si počítač bude 'myslet'
    if difficulty == 1:
        # Budeme losovat mezi 1 -- 10
        number_to_guess = random.randint(1, 10)
    elif difficulty == 2:
        # Budeme losovat mezi 1 -- 1000
        number_to_guess = random.randint(1, 1000)
    elif difficulty == 3:
        # Budeme losovat mezi 1 -- 1000000
        number_to_guess = random.randint(1, 1000000)
    else:
        # Sem bychom se nikdy neměli dostat, takže pokud tu jsme, něco je špatně.
        print("Neco se hodne nepovedlo :-)")


    # Nyní si počítač úspěšně myslí číslo a my můžeme začít hádat. 


# Tuhle konstrukci vysvětlíme později, až se dostaneme k modulům, importům a tak podobně.
if __name__ == "__main__":
    game()
