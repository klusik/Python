import re


def validuj_vek(vstup):
    """
    Opakovaně požaduje zadání platného věku, dokud uživatel nezadá správný vstup.

    :param vstup: Výzva pro uživatele (text zobrazený při zadávání).
    :return: Platné celé číslo představující věk (kladné číslo).
    """
    while True:
        try:
            vek = int(input(vstup))
            if vek > 0:
                return vek
            else:
                print("Věk musí být kladné číslo.")
        except ValueError:
            print("Neplatný vstup. Zadejte číslo.")


def validuj_telefon(vstup):
    """
    Opakovaně požaduje zadání telefonního čísla, dokud uživatel nezadá pouze číslice.

    :param vstup: Výzva pro uživatele (text zobrazený při zadávání).
    :return: Platné telefonní číslo jako řetězec.
    """
    while True:
        telefon = input(vstup)
        if telefon.isdigit():
            return telefon
        else:
            print("Telefonní číslo musí obsahovat pouze číslice.")


def validuj_email(vstup):
    """
    Opakovaně požaduje zadání platné e-mailové adresy.

    :param vstup: Výzva pro uživatele (text zobrazený při zadávání).
    :return: Platná e-mailová adresa jako řetězec.
    """
    while True:
        email = input(vstup)
        if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            return email
        else:
            print("Neplatný formát emailu. Zadejte správný email.")
