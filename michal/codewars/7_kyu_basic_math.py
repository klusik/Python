# this program will add or subtract based on imput given as string
# input in following format:
# "1plus2plus3plus4"  --> "10"
# "1plus2plus3minus4" -->  "2"

# in order to be able to recognise a number and operation, for cycle must be run on give string
def calculate(s):
    # your code here
    items = []

    for i in s:
        if i == '1':
            items.append(1)
        elif i == '2':
            items.append(2)
        elif i == '3':
            items.append(3)
        elif i == '4':
            items.append(4)
        elif i == 'p':
            items.append('+')
        elif i == 'm':
            items.append('-')

    print(items)
    # now sorting is finished and items contains
    # formula, which need to be reconstructed
    # let's iterate over items. if + is found, add
    # item before with item after
    # if - is found subtract item before with item
    # after
    # a is item before
    # b is item after
    a = 0
    b = 0
    for i in items:
        if i == '+':
            add = a+b
        elif i == '-':
            sub = a-b
    return items



calculate("1plus2plus3minus4")
