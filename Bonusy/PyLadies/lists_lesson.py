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

        if not len(splitted_name) == 2:
            correct_name = False
            continue # next name

        for name_part in splitted_name:
            if name_part[0].islower():
                correct_name = False
                break # next name

        if correct_name:
            correct_names.append(name)

    return correct_names


def select_incorrect(list_of_names):
    """ Returns a list of all incorrect names """
    correct_names = select_correct(list_of_names)

    incorrect_names = []
    for name in list_of_names:
        # Just using existing function :-D
        if name not in correct_names:
            incorrect_names.append(name)

    return incorrect_names


def repair_incorrect(list_of_names):
    """ Repair names """

    incorrect_names = select_incorrect(list_of_names)

    corrected_names = []

    for name in list_of_names:

        if name in incorrect_names:
            if not len(name.split()) == 2:
            # Correcting by deleting all middle names
                name = f"{name.split()[0]} {name.split()[-1]}"

            # Split it by name & surname
            name_first, name_second = name.split()

            corrected_names.append(f"{name_first.capitalize()} {name_second.capitalize()}")
            continue # next name

        # If not incorrect, add that name as is
        corrected_names.append(name)

    return corrected_names


# RUNTIME #
if __name__ == "__main__":
    names = ['jan Novák', 'Michal Sýkora', 'Rudolf klusal', 'kuba červinka', 'Jakub Jan Ryba']
    print(f"Original names: {names}")
    print(f"Correct names: {select_correct(names)}")
    print(f"Incorrect names: {select_incorrect(names)}")
    print(f"Corrected names: {repair_incorrect(names)}")
