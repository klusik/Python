class PojistenaOsoba:
    """
    Třída představující pojištěnou osobu.
    Obsahuje základní údaje: jméno, věk, telefonní číslo a e-mail.
    """

    def __init__(self, jmeno: str, vek: int, telefon: str, email: str):
        """
        Inicializuje objekt pojištěné osoby.

        :param jmeno: Jméno a příjmení pojištěné osoby.
        :param vek: Věk pojištěné osoby.
        :param telefon: Telefonní číslo pojištěné osoby.
        :param email: E-mailová adresa pojištěné osoby.
        """
        self.jmeno = jmeno
        self.vek = vek
        self.telefon = telefon
        self.email = email

    def __str__(self):
        """
        Vrací textovou reprezentaci objektu pojištěné osoby.

        :return: Formátovaný řetězec obsahující jméno, věk, telefon a e-mail.
        """
        return f"{self.jmeno}, {self.vek} let, Tel: {self.telefon}, Email: {self.email}"
