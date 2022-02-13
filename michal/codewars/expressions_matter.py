# task:
# Given three integers a, b, c
# return largest number obtained after inserting the following operators and brackets
# +, *, ()
# example:
# given numbers 1,2,3
# 1*(2+3)=5
# 1*2*3 = 6
# 1+2+3=7
# (1+2)*3 = 9

def expression_matter(a, b, c):
    prvni = a * (b + c)
    # print(prvni)

    druhy = a * b * c
    # print(druhy)

    treti = a + (b * c)
    # print(treti)

    ctvrty = (a + b) * c
    # print(ctvrty)

    seznam = [prvni, druhy, treti, ctvrty]
    seznam_serazen = sorted(seznam)
    # print('seznam:', seznam, 'seznam_serazen:', seznam_serazen)

    nejvetsi = seznam_serazen[3]
    # print('nejvetsi:', nejvetsi)

    return nejvetsi  # highest achievable result


expression_matter(5, 5, 5)
