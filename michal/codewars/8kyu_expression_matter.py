def expression_matter(a, b, c):
    # overeni hodnot
    overeni_hodnot = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    while True:
        try:
            a = int(a)
            b = int(b)
            c = int(c)
        except ValueError:
            print("vyjimka: nebylo zadano cislo")
            break

        if a not in overeni_hodnot or b not in overeni_hodnot or c not in overeni_hodnot:
            print("nektere ze zadanych hodnot nejsou v rozmezi 1 az 10")
            break
        else:
            break

    prvni = a * (b + c)
    # print(prvni)

    druhy = a * b * c
    # print(druhy)

    treti = a + (b * c)
    # print(treti)

    ctvrty = (a + b) * c
    # print(ctvrty)

    paty = a + b + c
    # print(paty)

    seznam = [prvni, druhy, treti, ctvrty, paty]
    seznam_serazen = sorted(seznam)
    # print('seznam:', seznam, 'seznam_serazen:', seznam_serazen)

    nejvetsi = seznam_serazen[4]
    # print('nejvetsi:', nejvetsi)

    return nejvetsi  # highest achievable result


print(expression_matter('10', '10', '2'))

# efektivnejsi verze, kterou jsem nenapsal :(
# def expression_matter(a, b, c):
#  return max(a + b + c, (a + b) * c, a * (b + c), a * b * c)
