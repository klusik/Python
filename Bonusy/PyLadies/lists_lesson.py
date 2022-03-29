"""
Představ si, že ti uživatelé zadávají jména a příjmení a ty si je
ukládáš do seznamu pro další použití např. v evidenci studentů.
Ne všichni jsou ale pořádní, a tak se v seznamu sem tam objeví
i jméno s nesprávně zadanými velkými písmeny. Například:

zaznamy = ['pepa novák', 'Jiří Sládek', 'Ivo navrátil', 'jan Poledník']
Úkolem je:

Napsat funkci, která vybere jen ty správně zadané záznamy,
které mají správně jméno i příjmení s velkým počátečním písmenem.
Napsat funkci, která vybere naopak jen ty nesprávně zadané záznamy.
(Nepovinný) – Napsat funkci, která vrátí seznam s opravenými záznamy.
"""

# FUNCTIONS #
def select_correct(list_of_names):
    """ Selects and return only correct list items """

    # Empty list for correct names
    correct_names = []


    for name in list_of_names:
        # If name has upper() in all words, it's correct.
        correct_name = True # Assume a correct name
        splitted_name = name.split()

        for name_part in splitted_name:
            if name_part[0].islower():
                correct_name = False
                break # next name

        if correct_name:
            correct_names.append(name)

    return correct_names


def select_incorrect(list_of_names):
    pass

def repair_incorrect(list_of_names):
    pass

# RUNTIME #
if __name__ == "__main__":
    names = ['jan Novák', 'Michal Sýkora', 'Rudolf klusal', 'kuba červinka']
    print(select_correct(names))
